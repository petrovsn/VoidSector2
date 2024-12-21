from modules.abstract.GameObjectsPool import GameObjectsPool
from modules.utils import Command
class cShips(GameObjectsPool):
    _instance = None # Приватное поле для хранения единственного экземпляра

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(cShips, cls).__new__(cls)
        return cls._instance


    def proceed_command(self, command:Command):
        try:
            target_id = command.get_target_id("ships")
            if target_id in self.objects:
                self.objects[target_id].proceed_command(command)
        except Exception as e:
            print(repr(e))

