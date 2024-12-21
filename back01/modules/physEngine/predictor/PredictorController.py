import numpy as np
import multiprocessing as mp
from modules.physEngine.core import hBodies, lBodies, dynamic_Body
from modules.physEngine.WorldPhysConstants import WorldPhysConstants
from modules.utils import ConfigLoader, Command
import time
import os
from loguru import logger
from collections import Counter

class TrajectoryPredictor_controller:
    _instance = None # Приватное поле для хранения единственного экземпляра

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TrajectoryPredictor_controller, cls).__new__(cls)
            try:
                ctx_manager = mp.Manager()
                cls._instance.shared_dict = ctx_manager.dict()
                cls._instance.predictors = {}
            except Exception as e:
                print(repr(e))
        return cls._instance

    def launch(self):
        for i in range(ConfigLoader().get("world.predictors_counter",int)):
            self.predictors[i] = PredictorProcessController_serverside(i, self.shared_dict)
            self.predictors[i].run()

    def update_predictors_avg_stats(self):
        summary_avg_stats = {}
        for i in self.predictors:
            predictor_stats = self.predictors[i].get_stats()
            xx = Counter(summary_avg_stats)
            yy = Counter(predictor_stats)
            xx.update(yy)
            summary_avg_stats = dict(xx)


        
        for k in summary_avg_stats:
            summary_avg_stats[k] = summary_avg_stats[k]/len(self.predictors)
            StaticticsCollector().set(k, summary_avg_stats[k])

    def get_predictor_with_less_workload(self):
        workload = None
        predictor_id = None
        for i in self.predictors:
            if predictor_id:
                if self.predictors[i].task_counter < workload:
                    predictor_id = i
                    workload = self.predictors[i].task_counter
            else:
                predictor_id = i
                workload = self.predictors[i].task_counter
        return predictor_id

    
    def update_hbodies(self):
        hBodies().update_description()
        for i in self.predictors:
            self.predictors[i].update_hbodies()

    def is_prediction_completed(self, mark_id):
        prediction_readyness_mark = f"{mark_id}_ready"
        prediction_data_mark = f"{mark_id}_predictions"
        if prediction_readyness_mark in self.shared_dict:
            return self.shared_dict[prediction_readyness_mark]
        else:
            self.shared_dict[prediction_data_mark] = []
            self.shared_dict[prediction_readyness_mark] = True
            return True

        
    def mark_prediction_as_calculating(self, mark_id):
        prediction_readyness_mark = f"{mark_id}_ready"
        self.shared_dict[prediction_readyness_mark] = False

    def request_predictions(self, mark_id, mass, start_position, start_velocity, hbody_idx, last_hbody_idx, depth):
        if not self.is_prediction_completed(mark_id): return
        predictor_id = self.get_predictor_with_less_workload()
        command = {
            "action":"predict",
            "params":{
                "mark_id":mark_id,
                "mass":mass,
                "pos":start_position.tolist(),
                "vel":start_velocity.tolist(),
                "hbody_idx":hbody_idx,
                "last_hbody_idx":last_hbody_idx,
                "depth":depth,
            }
        }
        self.predictors[predictor_id].add_task(command)
        self.mark_prediction_as_calculating(mark_id)

    def get_predictions(self, mark_id):
        prediction_readyness_mark = f"{mark_id}_ready"
        prediction_data_mark = f"{mark_id}_predictions"
        if prediction_readyness_mark in self.shared_dict:
            return self.shared_dict[prediction_data_mark]
        return []



    



class PredictorProcessController_serverside:
    def __init__(self, predictor_id, shared_dict):
        self.predictor_id = predictor_id
        self.task_counter = 0
        self.in_queue = mp.Queue()
        self.shared_dict = shared_dict
        self.shared_dict[f"{predictor_id}_stats"] = {}

    def get_stats(self):
        return self.shared_dict[f"{self.predictor_id}_stats"]

    def run(self):
        self.predictor_process = mp.Process(target=self.launch_predictor_controller, args=(self.predictor_id, self.in_queue, self.shared_dict))
        self.predictor_process.start()

        
    def update_hbodies(self):
        descr = hBodies().get_description()
        command = {
            "action":"update_hbodies",
            "params":descr,
        }
        self.add_task(command)


    def add_task(self, command):
        self.task_counter=self.task_counter+1
        self.in_queue.put(command)

    
    def launch_predictor_controller(self, predictor_id, in_queue, shared_dict):
        predictor_controller = PredictorProcessController(predictor_id, in_queue, shared_dict)
        predictor_controller.start()





# получает на вход обновление скорости в моменте,
# возвращает в контекстный словарь вектор из предсказаний с
# N+1й точки.
from modules.utils import StaticticsCollector
from datetime import datetime, timedelta
from modules.physEngine.predictor.PredictorBody import PredictorBody
import traceback
class PredictorProcessController:
    def __init__(self, predictor_id, in_queue, out_dictionary):   
        self.predictor_id = predictor_id  
        self.predictor_body = PredictorBody()
        lBodies().add(self.predictor_body)
        self.in_queue = in_queue
        self.out_dictionary = out_dictionary

    #за каждое полученное сообщение в очереди, он считает траекторию с заданных координат
    #каждое сообщение промаркировано mark_id. Пока один запрос не обработан, не стоит
    #присылать другой с тем же mark_id
    def start(self):
        try:
            not_stopped = True
            while not_stopped:
                if not self.in_queue.empty():
                    command_json =self.in_queue.get()
                    command = Command(command_json)
                    action = command.get_action()
                    params = command.get_params()

                    match action:
                        case "predict":  
                            StaticticsCollector().clear()
                            mark = params["mark_id"]


                            
                            mass = params["mass"]
                            pos = params["pos"]
                            vel = params["vel"]
                            hbody_idx = params["hbody_idx"]
                            last_hbody_idx = params["last_hbody_idx"]
                            depth = params["depth"]


                            timestep = datetime.now()

                            StaticticsCollector().begin_time_track(f"predictor.run_prediction")

                            predictions = self.predictor_body.run_prediction(mass, pos, vel, hbody_idx, last_hbody_idx, depth)

                            StaticticsCollector().end_time_track(f"predictor.run_prediction")
                            dt = datetime.now()-timestep

                            self.out_dictionary[f"{mark}_predictions"] = predictions #выгрузка результатов
                            self.out_dictionary[f"{mark}_ready"] = True #освобождение мьютекса для следующей итерации
                            self.out_dictionary[f"{self.predictor_id}_stats"] = StaticticsCollector().get()


                            

                        case "stop":
                            logger.info("PredictorProcessController termination")
                            not_stopped = False

                        case "update_hbodies":
                            description = params
                            hBodies().put_description(description)

                            

                #self.generate_prediction()
        except Exception as e:
            logger.exception(f"PredictorProcessController: {traceback.format_exc()}")

