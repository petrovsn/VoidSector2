
from queue import Queue

command_json = {
    "level": ["map_loader", "server", "ship"],
    "action":"str",
    "params": "str",
}
#
#
#
class Command:
    def __init__(self, command_json):
        self.json = command_json

    def contains_level(self, level_keyword):
        return level_keyword in self.json["level"]

    def get_target_id(self, level_keyword):

        levels = self.json["level"].split('.')
        targets = self.json["target"].split('.')
        for i,level_name in enumerate(levels):
            if level_name==level_keyword:
                return targets[i]
        return None



        
    def get_params(self):
        return self.json["params"]



        
    def get_action(self):
        return self.json["action"]



    

    
