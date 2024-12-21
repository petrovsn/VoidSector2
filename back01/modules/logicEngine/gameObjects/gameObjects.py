from modules.physEngine.core import basic_Body

#базовый класс для всех _физических_ сущностей на поле
class GameObject:
    def __init__(self, mark_id = None, position_np = None):
        self.type = self.__class__.__name__
        self.mark_id = mark_id if mark_id else id(self) 
        self.marker_type = self.__class__.__name__
        self.body:basic_Body = None

    def next_step(self):
        pass

    def set_position(self):
        pass

    def get_description(self):
        return {
            "mark_id":self.mark_id,
            "body":self.body.get_description(),
            "marker_type": self.marker_type
        }

    def put_description(self, descr):
        self.mark_id = descr["mark_id"]
        self.body.put_description(descr)

class abstractPool:
    def __init__(self):
        self.objects = {}

    def add(self, body_object):
        lbody_id = body_object.mark_id
        self.bodies[lbody_id] = body_object

from modules.abstract.GameObjectsPool import GameObjectsPool

class lObjects(GameObjectsPool):
    _instance = None  # Приватное поле для хранения единственного экземпляра
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(lObjects, cls).__new__(cls)
        return cls._instance

    



class hObjects(GameObjectsPool):
    _instance = None  # Приватное поле для хранения единственного экземпляра
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(hObjects, cls).__new__(cls)
        return cls._instance
