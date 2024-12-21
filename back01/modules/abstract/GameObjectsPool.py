from modules.abstract.SingletonDict import SingletonDict
#from SingletonDict import SingletonDict
class GameObjectsPool(SingletonDict):
    _instance = None  # Приватное поле для хранения единственного экземпляра
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GameObjectsPool, cls).__new__(cls)
            cls._instance.description = {}
        return cls._instance

    
    def get_essential_key(self, obj):
        return obj.mark_id

    
    def add(self,obj):
        super().add(obj)   
        self.description[obj.mark_id] = obj.get_description()

    def delete(self, key):
        super().delete(key)
        self.description.pop(key)

    
    def update_description(self):
        self.description = {}
        for mark_id in self.objects:
            self.description[mark_id] = self.objects[mark_id].get_description()

    def get_description(self):
        self.update_description()
        return self.description

    
    def next_step(self):
        for mark_id in self.objects:
            self.objects[mark_id].next_step()




    
