from modules.utils import catch_exception, StaticticsCollector, ConfigLoader
from datetime import datetime, timedelta
from modules.logicEngine.map_controllers.loader import MapLoader
from modules.physEngine.predictor.PredictorController import TrajectoryPredictor_controller
from modules.physEngine.core import lBodies, CrossDistancePool
from modules.logicEngine.gameObjects.gameObjects import lObjects, hObjects
import traceback
import multiprocessing as mp
from multiprocessing import Process, Manager, freeze_support
import time
import asyncio
from random import randrange
from math import *
from loguru import logger
from enum import Enum
from modules.CommandController import Command
# обертка для процесса, в котором работает сервер.
# in_queue - очередь для команд: спавн, передвижение
# контекст менеджер передается из базового процесса и создается в __main__


class EngineSector_interactor:
    _instance = None  # Приватное поле для хранения единственного экземпляра

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(EngineSector_interactor, cls).__new__(cls)
        return cls._instance

    # ==========================ИНИЦИИРОВАНИЕ=====================================

    def init_server(self):

        
        ctx_manager = Manager()
        self.server = None
        self.in_queue = mp.Queue()
        self.out_sector_data = ctx_manager.dict()
        self.out_sector_data["lObjects"] = {}
        self.out_sector_data["hObjects"] = {}
        self.out_sector_data["cShips"] = {}
        self.out_sector_data["admin"] = {}

    def start(self):
        self.p = mp.Process(target=self.run_instance, args=(
            self.in_queue, self.out_sector_data,))
        self.p.start()

    def run_instance(self, in_queue, out_sector_data):
        instance = EngineSector(in_queue, out_sector_data)
        instance.start()
    # ==============================================================================================

    # ============================КОМАНДЫ ДЛЯ CЕРВЕРА=============================================
    # просто транслируются на сервер as it is
    def proceed_command(self, command):
        self.in_queue.put(command)

    # =============ИСХОДЯЩИЙ ПОТОК================================================================
    # key -- идентификатор объекта, от которого ведется наблюдение
    # None -- админский взгляд.
    # карта передается на клиент по протоколу http
    def get_sector_map(self, key=None):
        data = {}
        try:
            # информация о всех астероидах
            return self.out_sector_data["hObjects"]
        except Exception as e:
            return {}
    # состояние игровых объектов передается по tcp

    def get_entities(self, key=None):
        data = {}
        try:
            # информация о всех "легких" объектах, загруженных в оперативную память рендера карты
            # т.е. о тех, которые могут в ближайшее время повзаимодействовать с игроком. Объем ~10-20
            return self.out_sector_data["lObjects"]
            # информация об актуальном состоянии каждого корабля. Содержит информацию о состоянии систем корабля.
        except Exception as e:
            return {}

    def get_admin_data(self):
        data = {}
        try:
            # информация о всех "легких" объектах, загруженных в оперативную память рендера карты
            # т.е. о тех, которые могут в ближайшее время повзаимодействовать с игроком. Объем ~10-20
            return self.out_sector_data["admin"]
            # информация об актуальном состоянии каждого корабля. Содержит информацию о состоянии систем корабля.
        except Exception as e:
            return {}

    # актуальное состояние кораблей
    def get_ships(self, key=None):
        pass


# from modules.logicEngine.map_controllers.editor import MapEditor
from modules.logicEngine.ship.shipPool import cShips

class EngineSector:
    @catch_exception
    def __init__(self, in_queue: mp.Queue, out_sector_data):
        self.in_queue = in_queue
        self.out_sector_data = out_sector_data

        TrajectoryPredictor_controller().launch()

        MapLoader().load_basic_test_map()
        self.update_hObjects()

        self.event_loop = asyncio.new_event_loop()
        self.event_loop.create_task(self.command_loop())
        self.event_loop.create_task(self.main_loop())
        # self.event_loop.create_task(self.update_quest_poits_state())
        # self.event_loop.create_task(self.update_ships_state())
        # self.event_loop.create_task(self.update_station_state())
        # self.event_loop.create_task(self.map_autosaver())

    def start(self):
        self.event_loop.run_forever()

    # ===========================РАЗДЕЛ ДЛЯ КОРУТИН В ЦИКЛЕ ДВИЖКА СЕКТОРА============================================
    async def command_loop(self):
        while True:
            await asyncio.sleep(0.02)
            while not self.in_queue.empty():
                command = Command(self.in_queue.get())
                self.proceed_command(command)

    def proceed_command(self, command: Command):
        try:
            if command.contains_level("ship"):
                cShips().proceed_command(command)
        except Exception as e:
            print("SectorServer Command Execution", repr(e))

    # ==========ФИЗИКА===============================================================================================
    # основной цикл событий сервера

    async def main_loop(self):
        fps = ConfigLoader().get("world.fps", float)
        frame_duration_sec = 1.0/fps
        while True:
            # контроль гладкости кадров идет по частоте системного времени,
            # поэтому используется datetime
            start_frame_timestamp = datetime.now()
            try:
                StaticticsCollector().clear()
                StaticticsCollector().begin_time_track("dt_frame")

                # очистить кэш сохраненных дистанция между объектами
                CrossDistancePool().clear()

                # итерация физического движка по всем динамическим телам
                lBodies().next_step()

                # итерация поведенческого движка по всем активным объектам(кораблям, станциям и ракетам)
                lObjects().next_step()

                #итерация систем управляемых кораблей
                #!! НЕ СТАВИТЬ В ЭТИ ФУНКЦИИ ФИЗИКУ И ЛОГИКУ ПРИМИТИВОВ!!
                #cShips().next_step()

                # обновили описание объектов
                lObjects().update_description()


                

                # выгрузили в буфер обмена с классом-контейнером
                self.out_sector_data["lObjects"] = lObjects().get_description()

                StaticticsCollector().end_time_track("dt_frame")
                TrajectoryPredictor_controller().update_predictors_avg_stats()
                admin_data = {
                    "performance": StaticticsCollector().get()
                }

                self.out_sector_data["admin"] = admin_data

            except Exception as e:
                logger.exception(
                    f"EngineSector.main_loop: {traceback.format_exc()}")

            end_frame_timestamp = datetime.now()
            frame_exec_realtime: timedelta = end_frame_timestamp-start_frame_timestamp
            free_time = frame_duration_sec-frame_exec_realtime.seconds
            await asyncio.sleep(free_time)

    # ===============================================================================================================

    def update_hObjects(self):
        self.out_sector_data["hObjects"] = hObjects().get_description()
