
import numpy as  np


from modules.logicEngine.gameObjects.gameObjects import GameObject, hObjects
from modules.physEngine.core import hBody, lBodies, hBodies, dynamic_Body
from modules.physEngine.CalculationUtilites import CalculationUtilites
from modules.utils import ConfigLoader
from modules.logicEngine.triggers.collector import TriggerQueue
from modules.physEngine.predictor.PredictorController import TrajectoryPredictor_controller

class ObjectShip(GameObject):
    def __init__(self, mark_id=None, position_np=None, mass = 10, radius = 100):
        super().__init__(mark_id, position_np)
        self.body:dynamic_Body = dynamic_Body(mark_id)
        self.predition_depth = 10

        self.direction = 0
        self.acceleration = 0

        lBodies().add(self.body)

    def next_step(self):
        super().next_step()
        current_acceleration = self.get_acceleration_vector()
        self.body.set_artificial_acceleration(current_acceleration)
        TrajectoryPredictor_controller().request_predictions(self.mark_id, self.body.mass, 
                                                             self.body.get_position_np(), self.body.get_velocity_np(), 
                                                             self.body.hbody_idx, self.body.last_hbody_idx, self.predition_depth)

         


    def get_acceleration_vector(self):
        if self.acceleration:
            acc_vector = np.array([0,self.acceleration])
            acc_vector = CalculationUtilites.rotate_vector(acc_vector, self.direction)
            return acc_vector
        return np.zeros(2)

    def set_direction(self, direction):
        self.direction = direction

    def set_acceleration(self, acceleration):
        self.acceleration = acceleration

    def set_prediction_depth(self, prediction_depth):
        self.predition_depth = prediction_depth

    def get_description(self):
        descr = super().get_description()
        descr["predictions"] = TrajectoryPredictor_controller().get_predictions(self.mark_id)
        descr["direction"] = self.direction
        descr["acceleration"] = self.acceleration
        return descr

    

    def put_description(self, descr):
        super().put_description(descr)
        self.direction = descr["direction"]
        self.acceleration = descr["acceleration"]

    
    def set_position_and_velocity(self, position = None, velocity=None):
        self.body.set_position_and_velocity(position,velocity)


    
