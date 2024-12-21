from datetime import datetime
import numpy as np
from modules.utils import Command, ConfigLoader

from modules.logicEngine.gameObjects.gameObjects import lObjects
from modules.logicEngine.gameObjects.objShips import ObjectShip
from modules.logicEngine.ship.systems.core_sm import GlobalShipSystemController, BasicShipSystem
from modules.physEngine.WorldPhysConstants import WorldPhysConstants



class EngineSystem(BasicShipSystem):
    def __init__(self, mark_id):
        super().__init__(mark_id, "engine_sm")
        self.body:ObjectShip = ObjectShip(mark_id=mark_id)
        lObjects().add(self.body)
        self.rotation_speed = 2
        self.engine_thrust = 10


    def next_step(self):
        pass

    def get_description(self):
        return super().get_description()

    
    def put_description(self, descr):
        return super().put_description(descr)


    def set_rotation(self, value):
        rot_modificator = -1 if value=='right' else 1
        current_direction = self.body.direction
        self.body.set_direction(current_direction+rot_modificator*self.rotation_speed)


    def get_engine_thrust(self, value_perc):
        return self.engine_thrust*value_perc

    def proceed_command(self, command:Command):
        super().proceed_command(command)
        action = command.get_action()
        params = command.get_params()

        match action:
            case 'set_prediction_depth':
                self.body.set_prediction_depth(params["value"])
            case 'set_acceleration':
                self.body.set_acceleration(self.get_engine_thrust(params["value"]))
            case 'set_rotation':
                #left or right
                self.set_rotation(params["value"])
            case "exhaust_heat":
                pass





    
