

import numpy as np
from random import randint
import json
import random
import copy

from modules.utils import Command

#оперирует объектами класса gameObjects(и производными)
class MapEditor:
    def __init__(self):
        self.selected_object_id = None

    def get_status(self):
        return {
            "selected_object_id": self.selected_object_id
        }

    def proceed_command(self, command:Command):
        try:
            action = command.get_action()
            match action:
                case 'save_map': self.save_map(command.get_params()["map_name"])
        except Exception as e:
            print(repr(e))
