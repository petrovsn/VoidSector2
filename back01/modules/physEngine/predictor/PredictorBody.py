import numpy as np
import multiprocessing as mp
from modules.physEngine.core import hBodies, dynamic_Body, CrossDistancePool
from modules.physEngine.WorldPhysConstants import WorldPhysConstants
from modules.utils import ConfigLoader, Command, StaticticsCollector
import time
import os

from modules.utils import catch_exception


class PredictorBody(dynamic_Body):
    @catch_exception
    def __init__(self):
        super().__init__("predictor", np.zeros(2), np.zeros(2))
        predictions_count = ConfigLoader().get("world.prediction_max_length", int)
        self.positions = np.zeros([predictions_count, 2], dtype=np.float32)
        self.velocities = np.zeros([predictions_count, 2], dtype=np.float32)
        self.iterations_limit = predictions_count
        self.actual_iteration = 0
        self.timestep = WorldPhysConstants().timestep

    # depth - длительность предсказания в секундах
    @catch_exception
    def set_predictors_depth(self, depth):
        self.iterations_limit = ConfigLoader().get("world.prediction_max_length", int)
        self.timestep = WorldPhysConstants().timestep

        depth_ticks = int(depth*WorldPhysConstants().fps)

        if depth_ticks > self.iterations_limit:
            #увеличение шага по времени в симуляции пропорционально тому,
            #насколько планируемая длина трека больше лимита по расчётной сетке
            timescale = depth_ticks*1.0/self.iterations_limit
            self.timestep = self.timestep*timescale

        
        elif depth_ticks<self.iterations_limit:
            self.iterations_limit = depth_ticks

    def calcualte_trajectory(self):
        for i in range(1, self.iterations_limit):
            self.actual_iteration = i-1
            #StaticticsCollector().begin_time_track(f"predictor.get_natural_acceleration")
            acceleration = self.get_natural_acceleration(self.positions[i-1])
            #StaticticsCollector().end_time_track(f"predictor.get_natural_acceleration")

            #StaticticsCollector().begin_time_track(f"predictor.iteration")
            self.velocities[i] = self.velocities[i-1] + \
                self.timestep*acceleration
            self.positions[i] = self.positions[i-1] + \
                self.timestep*self.velocities[i]

            
            #StaticticsCollector().end_time_track(f"predictor.iteration")

    def get_predictions(self):
        return self.positions[:self.iterations_limit][::-15][::-1].tolist()

    @catch_exception
    def run_prediction(self, mass, start_position, start_velocity, hbody_idx, last_hbody_idx, depth) -> list:
        CrossDistancePool().clear()
        # установить стартовые условия
        #StaticticsCollector().begin_time_track(f"predictor.init_data")
        self.mass = mass
        self.positions[0] = np.array(start_position)
        self.velocities[0] = np.array(start_velocity)


        

        self.hbody_idx = hbody_idx
        self.last_hbody_idx = last_hbody_idx
        #StaticticsCollector().end_time_track(f"predictor.init_data")

        # рассчитать длину расчитываемого массива
        #StaticticsCollector().begin_time_track(f"predictor.set_predictors_depth")
        self.set_predictors_depth(depth)
        #StaticticsCollector().end_time_track(f"predictor.set_predictors_depth")
        # рассчитать траекторию

        #StaticticsCollector().begin_time_track(f"predictor.calcualte_trajectory")
        self.calcualte_trajectory()
        #StaticticsCollector().end_time_track(f"predictor.calcualte_trajectory")

        #StaticticsCollector().begin_time_track(f"predictor.get_predictions")
        results = self.get_predictions()
        #StaticticsCollector().end_time_track(f"predictor.get_predictions")


        

        return results
