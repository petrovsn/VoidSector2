from modules.abstract.GameObjectsPool import GameObjectsPool
import math as m
import copy
from modules.utils import Command, StaticticsCollector
import sys
import traceback
import numpy as np
from modules.physEngine.WorldPhysConstants import WorldPhysConstants
from modules.utils import ConfigLoader
# Астероиды, прибиты гвоздями к небу
import random
import numpy as np
from modules.physEngine.WorldPhysConstants import WorldPhysConstants
import math
from modules.physEngine.CalculationUtilites import CalculationUtilites
import traceback
from loguru import logger


class basic_Body:
    def __init__(self, mark_id=None, mass=1):
        self.mark_id = mark_id if mark_id else str(id(self))
        self.mass = mass

    def get_position_np(self):
        return np.zeros(2)

    def get_description(self):
        pass

    def put_description(self, descr):
        pass

# класс только для работы с расчётом траекторий, хранит массу и радиус гравитационного колодца
# все триггеры игровой логики(защита от EMP) лежат в модуле logicEngine


class hBody(basic_Body):
    def __init__(self, mark_id=None, pos=None, mass=10, radius=100):
        super().__init__(mark_id, mass)
        self.gravity_radius = radius
        self.position = pos if pos else np.array([0, 0])

    def get_position_np(self):
        return self.position

    
    def set_position(self, position_np):
        self.position = position_np

    def get_description(self):
        descr = {
            "mark_id": self.mark_id,
            "pos": self.position.tolist(),
            "mass": self.mass,
            "gravity_radius": self.gravity_radius
        }
        return descr

    def put_description(self, descr):
        self.mark_id = descr["mark_id"]
        self.position = np.array(descr["pos"])
        self.mass = descr["mass"]
        self.gravity_radius = descr["gravity_radius"]

    def is_position_in_gravity_radius(self, position):
        distance = np.linalg.norm(position-self.position)
        return distance<self.gravity_radius


# базоый класс для объектов и для их траекторий
# моделирует тело, которое просто летит под действием сил грацитации
# вычислительная сложность за итерацию - О(1)
class dynamic_Body(basic_Body):
    def __init__(self, mark_id=None, pos=np.array([0, 0]), vel=np.array([0, 0])):
        super().__init__(mark_id)
        self.predictions_count = 2
        self.positions = np.zeros(
            [self.predictions_count, 2], dtype=np.float32)
        self.velocities = np.zeros(
            [self.predictions_count, 2], dtype=np.float32)
        self.set_position_and_velocity(pos, vel)

        # айди текущего гравитационного колодца
        self.hbody_idx = None

        # айди последнего, в котором побывал. Используется для оптимизации поиска нового текущего
        self.last_hbody_idx = None

        #вектор ускорения в любую сторону
        self.acceleration_vector = np.zeros(2)

    def get_position_np(self):
        return self.positions[1]

    def get_velocity_np(self):
        return self.velocities[1]

    # задает координаты, скорость и направление относительно ближайшего тела
    # clockwise работает только если скорость не задается вручную, а высчитывается относительно
    # ближайшего тела
    def set_position_and_velocity(self, position, velocity=None, clockwise=False):
        if type(position) == list:
            position = np.array(position)
        if type(velocity) == list:
            velocity = np.array(velocity)

        #if type(velocity) != type(None):
        #    velocity = CalculationUtilites.get_stable_velocity(
        #        position, hBodies()[self.hbody_idx])
        #    if clockwise:
        #        velocity = velocity*-1

        if type(velocity) == type(None):
            velocity = np.array([9999999,999999])

        for i in range(self.predictions_count):
            self.positions[i] = position
            self.velocities[i] = velocity

    def get_description(self):
        descr = {
            "mark_id": self.mark_id,
            "mass": self.mass,
            "pos": self.get_position_np().tolist(),
            "vel": self.get_velocity_np().tolist()
        }
        return descr

    def put_description(self, descr):
        self.mark_id = descr["mark_id"]
        self.mass = descr["mass"]
        self.set_position_and_velocity(descr["pos"], descr["vol"])

    def get_related_hbody_idx(self):
        return None

    def get_acceleration(self):
        return self.get_natural_acceleration(self.get_position_np())+self.get_artifical_acceleration()

    def get_natural_acceleration(self, position):
        acceleration = np.zeros(2)
        self.last_hbody_idx = self.hbody_idx if self.hbody_idx else self.last_hbody_idx

        
        is_hbody_idx_actual = hBodies().is_position_in_gravity_radius(position, self.hbody_idx)



        
        if not is_hbody_idx_actual:
            self.hbody_idx = hBodies().get_related_hbody_idx(position, self.last_hbody_idx)

            if self.hbody_idx:
                pass


    


        
        if self.hbody_idx:
            acceleration = hBodies().get_acceleration_for_position(position, self.mass, self.hbody_idx)

        

        elif self.last_hbody_idx:
            acceleration = hBodies().get_acceleration_for_position(position, self.mass, self.last_hbody_idx)



        return acceleration

    

    
    def set_artificial_acceleration(self, value_np):
        self.acceleration_vector = value_np

    def get_artifical_acceleration(self):
        return self.acceleration_vector

    def next_step(self):
        acceleration = self.get_acceleration()
        dt = WorldPhysConstants().timestep
        self.positions[0] = self.positions[1]
        self.velocities[0] = self.velocities[1]
        self.velocities[1] = self.velocities[0]+dt*acceleration
        self.positions[1] = self.positions[0]+dt*self.velocities[1]


class CrossDistancePool:
    _instance = None  # Приватное поле для хранения единственного экземпляра

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(CrossDistancePool, cls).__new__(cls)
            cls._instance.distances = {}

        return cls._instance

    def update(self):
        pass

    def clear(self):
        self.distances = {}

    def get_body(self, mark):
        if mark in lBodies():
            mark_body = lBodies()[mark]
            return mark_body
        return hBodies()[mark]

    
    def get_from_position_to_hbody(self, position_np, hbody_mark_id):

        key_p1 = position_np[0]+position_np[1]
        key = (key_p1,hbody_mark_id)
        if key in self.distances:
            return self.distances[key]

        
        pos_2 = hBodies()[hbody_mark_id].get_position_np()



        distance = np.linalg.norm(position_np-pos_2)

        self.distances[key]=distance
        return self.distances[key]

    def get(self, mark_1, mark_2):
        key = (mark_1, mark_2)
        key_rev = (mark_2, mark_1)
        distance = 9999999999
        try:

            if key in self.distances:
                return self.distances[key]

            
            if key_rev in self.distances:
                return self.distances[key_rev]

            
            mark_1_body:basic_Body = self.get_body(mark_1)
            mark_2_body:basic_Body = self.get_body(mark_2)
            pos_1 = mark_1_body.get_position_np()
            pos_2 = mark_2_body.get_position_np()
            distance = np.linalg.norm(pos_1-pos_2)

            self.distances[key]=distance
            self.distances[key_rev]=distance

        
        except Exception as e:
            distance = 9999999999
            logger.exception(f"CrossDistancePool: {traceback.format_exc()}")

        return distance


# класс физических объектов dynamic_Body. Работает только с физикой.


class lBodies(GameObjectsPool):
    _instance = None  # Приватное поле для хранения единственного экземпляра

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(lBodies, cls).__new__(cls)
        return cls._instance

    

    

class QuadrantIndex:
    def __init__(self, map_border, quadrant_grid_step):
        self.quadrant_index = {}
        self.map_border = map_border
        self.quadrant_grid_step = quadrant_grid_step
        self.base = 1234051231231

    def get_quandrant_idx_for_position(self, position):
        try:
            np_quad_idx:np.array = (position+self.map_border)//self.quadrant_grid_step
            np_quad_idx = self.base*np_quad_idx[0]+np_quad_idx[1]
            return np_quad_idx
        except Exception as e:
            print(e)

    def add_body_to_quandrant_index(self, body_idx, position):
        idx = self.get_quandrant_idx_for_position(position)
        if idx not in self.quadrant_index:
            self.quadrant_index[idx] = []
        self.quadrant_index[idx].append(body_idx)

    def __getitem__(self, key):
        return self.objects[str(key)]

    def get_direct_quandrant_for_position(self, position):
        idxs = self.get_quandrant_idx_for_position(position)
        if idxs in self.quadrant_index:
            return self.quadrant_index[idxs]
        return []

    
    def get_surrounding_quandrant_for_position(self, pos):
        result = []
        idxs = self.get_quandrant_idx_for_position(pos)
        idxi = np.array([int(a) for a in idxs[1:-1].split()])

        for i in [-1,1]:
            for j in [-1,1]:
                tmp_idx = str(idxi+np.array([i,j]))
                if tmp_idx in self.quadrant_index:
                    result= result+self.quadrant_index[tmp_idx]

        return result


# класс физических объектов hBody. Работает только с физикой.
class hBodies(GameObjectsPool):
    _instance = None  # Приватное поле для хранения единственного экземпляра
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(hBodies, cls).__new__(cls)
            # нужен для быстрого поиска квадранта небольшого размера,
            # в котором можно уже искать прямым перебором. С учётом того, что гравитационный колодец
            # не ограничен квадрантом - если не нашлось в центральном, ищется по 8 окрестным
            cls._instance.map_border = 100
            cls._instance.quadrant_index = QuadrantIndex(cls._instance.map_border, ConfigLoader().get("world.quadrant_grid_step_initial",float))

            # индекс "соседних" гравитационных колодцев. Служит для подгрузки статических объектов
            # по мере приближения наблюдателя
            cls._instance.neighbours = {}

            # условный радиус карты, в которой происходит действие

            
        return cls._instance

    
    def put_description(self, descr):
        self.objects = {}
        self.description = {}
        for mark_id in descr:
            hbody_descr = descr[mark_id]
            hbody = hBody(mark_id)
            hbody.put_description(descr[mark_id])
            self.add(hbody)
        self.update_supplementary()

    def update_map_border_value(self):
        max_distance = 100
        for body_idx in self.objects:
            max_distance = max(
                self.objects[body_idx].position[0], self.objects[body_idx].position[0], max_distance)
        self.map_border = max_distance+100

    def get_maximal_gravity_radius(self):
        max_gravity_radius = 100
        for body_idx in self.objects:
            gravity_radius = self.objects[body_idx].gravity_radius
            if gravity_radius > max_gravity_radius:
                max_gravity_radius = gravity_radius
        return max_gravity_radius

    
    def update_supplementary(self):
        self.update_map_border_value()
        self.update_quadrant_index()
        self.update_description()

    def update_quadrant_index(self):
        self.update_map_border_value()
        gravity_radius = self.get_maximal_gravity_radius()
        self.quadrant_index = QuadrantIndex(self.map_border, gravity_radius*4)
        for body_idx, body in self.objects.items():
            self.quadrant_index.add_body_to_quandrant_index(body_idx, body.position)


    def get_related_quadrant(self, pos):
        idx = self.get_quandrant_index_for_position(pos)
        if idx not in self.quadrant_index:
            return []

        

    def locate_related_hbody_in_set(self, pos, set_of_hbodies):
        for hbody_idx in set_of_hbodies:
            located = hBodies()[hbody_idx].is_position_in_gravity_radius(pos)
            if located:
                return hbody_idx
        return None
    # возвращает айди астероида, в гравитационном колодце которого
    # находится указанная позиция
    def get_related_hbody_idx(self, pos, latest_body_idx = None):
        #проверяем последние координаты
        if latest_body_idx:
            hbody_idx = self.locate_related_hbody_in_set(pos, [latest_body_idx])
            if hbody_idx: return hbody_idx

        #проверяем координаты в квадранте
        direct_quadrant = self.quadrant_index.get_direct_quandrant_for_position(pos)
        hbody_idx = self.locate_related_hbody_in_set(pos, direct_quadrant)
        if hbody_idx: 
            return hbody_idx


        
        #проверяем координаты в квадранте 3х3
        ##surrounding_quadrant = self.quadrant_index.get_surrounding_quandrant_for_position(pos)
        #hbody_idx = self.locate_related_hbody_in_set(pos, surrounding_quadrant)
        #if hbody_idx: 
        #    return hbody_idx

        #если совсем занесло не туда - возвращаем None
        return None

    
    def is_entity_in_gravity_radius(self, entity_mark, hbody_idx):
        try:
            if not entity_mark: return False
            if not hbody_idx: return False
            actual_distance = CrossDistancePool().get(entity_mark, hbody_idx)
            return actual_distance<hBodies()[hbody_idx].gravity_radius
        except Exception as e:
            logger.exception(traceback.format_exc())
        return False

    
    def is_position_in_gravity_radius(self, position_np, hbody_idx):
        try:
            if not hbody_idx: return False
            actual_distance = CrossDistancePool().get_from_position_to_hbody(position_np, hbody_idx)
            return actual_distance<hBodies()[hbody_idx].gravity_radius
        except Exception as e:
            logger.exception(traceback.format_exc())
        return False

    def get_acceleration_for_position(self, position, mass, hbody_idx):
        if not hbody_idx: return np.zeros(2)

        dPos = hBodies()[hbody_idx].get_position_np() - position
        distance = CrossDistancePool().get_from_position_to_hbody(position,hbody_idx)
        r = max(distance,40)
        F = WorldPhysConstants().gravity_constant*(mass*hBodies()[hbody_idx].mass)/(r*r)

        #distance_2_center = r/gravity_well_radius
        #if self.gravity_well_linear_percentage<=distance_2_center<=1:
        #    F = F*((1-distance_2_center)/(1-self.gravity_well_linear_percentage))

        acceleration_vector = CalculationUtilites.get_projections(F, dPos)/mass
        return acceleration_vector

    def get_acceleration_in_position(self, position, mass, hbody_idx):
        return np.array([1,1])
