from modules.logicEngine.gameObjects.gameObjects import GameObject, hObjects
from modules.physEngine.core import hBody, lBodies, hBodies, CrossDistancePool
from modules.utils import ConfigLoader
from modules.logicEngine.triggers.collector import TriggerQueue
#класс hbody отвечает только за физический объект с массой и нулевым бокс-коллайдером
#класс ObjectAsteroid содержит в себе информацию о предельном гравитационном радиусе и прочих специфических эффектах
#по вызову функции check_interaction, которая вызывается объектом класса "ship" или "projectile", проверяет, релевантно ли это воздействие
class ObjectAsteroid(GameObject):
    def __init__(self, mark_id=None, position_np=None, mass = 10, radius = 100):
        super().__init__(mark_id, position_np)
        self.body = hBody(mark_id, position_np, mass, radius)

        #сразу после создания объект спавнится в физическом мире(обсчитывается через physEngine)
        hBodies().add(self.body)
        self.collider_radius = radius*ConfigLoader().get("world.default_objAster_collider_perc", float)

    def set_position(self, position_np):
        self.body.set_position(position_np)

        
    def get_description(self):
        descr = super().get_description()
        descr["collider_radius"] = self.collider_radius
        return descr

    
    def put_description(self, descr):
        super().put_description(descr)
        self.collider_radius = descr["collider_radius"]

    def check_collision(self, interactor_id, distance):
        if distance<self.collider_radius:
            TriggerQueue().add("collision", self.mark_id, {
                "collider":self.mark_id,
                "object": interactor_id
            })

        
    def check_interaction(self, interactor_id):
        distance = CrossDistancePool().get(self.mark_id, interactor_id)
        self.check_collision(self, interactor_id, distance)

        
