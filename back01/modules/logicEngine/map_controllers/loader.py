

import json
import numpy as np

from modules.utils import catch_exception

from modules.logicEngine.gameObjects.gameObjects import hObjects, lObjects
from modules.logicEngine.gameObjects.objAsteroids import ObjectAsteroid
from modules.logicEngine.gameObjects.objShips import ObjectShip
from modules.physEngine.core import lBodies, hBodies
from modules.physEngine.predictor.PredictorController import TrajectoryPredictor_controller
from modules.logicEngine.ship.ship import Ship
from modules.logicEngine.ship.shipPool import cShips


class MapLoader:
    _instance = None # Приватное поле для хранения единственного экземпляра
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MapLoader, cls).__new__(cls)
        return cls._instance

    @catch_exception
    def load_basic_test_map(self):
        obj1 = ObjectAsteroid("zero_aster",None, 10, 200)
        hObjects().add(obj1)

        obj1.set_position(np.array([-200,0]))

        obj1 = ObjectAsteroid("primo_aster",None, 10, 200)
        hObjects().add(obj1)

        obj1.set_position(np.array([200,0]))

        obj1 = ObjectAsteroid("tertio_aster",None, 10, 200)
        hObjects().add(obj1)

        obj1.set_position(np.array([0,350]))

        obj1 = ObjectAsteroid("quatro_aster",None, 10, 200)
        hObjects().add(obj1)
        obj1.set_position(np.array([0,-350]))




        ship1 = Ship("Nia")
        cShips().add(ship1)
        lBodies()[ship1.mark_id].set_position_and_velocity(np.array([120,0]), np.array([0,11]))


        hBodies().update_supplementary()
        TrajectoryPredictor_controller().update_hbodies()

            
