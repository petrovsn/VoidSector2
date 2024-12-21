

from modules.utils import Command
from loguru import logger
import traceback
from modules.logicEngine.ship.systems.core_sm import GlobalShipSystemController
from modules.logicEngine.ship.systems.engine_sm import EngineSystem


            
class Ship:
    def __init__(self, mark_id = None):
        self.mark_id = mark_id if mark_id else str(id(self))
        GlobalShipSystemController().add(self.mark_id, "engine_sm", EngineSystem(mark_id))

    def get_system(self, system_name):
        return GlobalShipSystemController().get(self.mark_id, system_name)

    def proceed_command(self, command:Command):
        GlobalShipSystemController().proceed_command(self.mark_id, command)

    def next_step(self):
        GlobalShipSystemController().next_step(self.mark_id)

    def get_description(self):
        result = {"mark_id":self.mark_id, "type": self.__class__.__name__, "systems":{}}
        system_list = GlobalShipSystemController().get_systems_list(self.mark_id)
        for system_name in system_list:
            result["systems"][system_name] = self.get_system(system_name).get_description()
        return result

    def put_description(self, descr):
        system_list = GlobalShipSystemController().get_systems_list(self.mark_id)
        for system_name in system_list:
            try:
                self.get_system(system_name).put_description(descr["systems"][system_name])
            except Exception as e:
                logger.exception(f"Ship.put_description:{traceback.format_exc()}")


                    
