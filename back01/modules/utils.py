






        
import traceback
import functools
from modules.CommandController import Command
from loguru import logger

def catch_exception(function):
    from functools import wraps
    @functools.wraps(function)
    def wrapper(*args, **kw):
            try:
                result = function(*args, **kw)
                return result
            except Exception as e:
                logger.exception(f"{function.__name__}:{traceback.format_exc()}")
    return wrapper

def get_dt_ms(t1, t2):
    return round((t2-t1).microseconds/1000000,4)

import configparser


class ConfigLoader:
    _instance = None # Приватное поле для хранения единственного экземпляра

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigLoader, cls).__new__(cls)
            cls._instance.config = configparser.ConfigParser()
            cls._instance.filename = "configs/config.ini"
            cls._instance.config.read("configs/config.ini")
            cls._instance.config_cache = {}

        return cls._instance

        
    def update(self):
        self.config = configparser.ConfigParser()
        self.config.read(self.filename)

     
    def get(self, key_word, type = str):
        if key_word in self.config_cache:
            return self.config_cache[key_word]

        
        tmp = self.config
        for key in key_word.split('.'):
            tmp = tmp[key]            
        if type==list:
            return [float(a) for a in tmp.split()]

        
        self.config_cache[key_word] = type(tmp)
        return self.config_cache[key_word]

        
    def proceed_command(self, command:Command):
        params = command.get_params()
        action = command.get_action()
        match action:
            case "save":
                self.save(params["filename"], params["config_data"])
            case "load":
                self.load(params["filename"])

    def load(self, filename):
        self.filename = f"configs/{filename}"
        self.update()            

    def save(self, filename, config_data):
        config_object = configparser.ConfigParser()
        sections=config_data.keys()
        for section in sections:
            config_object.add_section(section)
        for section in sections:
            inner_dict=config_data[section]
            fields=inner_dict.keys()
            for field in fields:
                value=inner_dict[field]
                config_object.set(section, field, str(value))

        file = open("configs/"+filename+".ini","w")
        config_object.write(file)
        file.close()
        #self.config = configparser.ConfigParser()
        #self.config.read(f"configs/{filename}")


from datetime import datetime, timedelta
class StaticticsCollector:
    _instance = None # Приватное поле для хранения единственного экземпляра

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(StaticticsCollector, cls).__new__(cls)
            cls._instance.data = {}
            cls._instance.time_tracks = {}

        return cls._instance

    def add(self, key, timestep):
        if key not in self.data: self.data[key]=0
        self.data[key] = self.data[key]+timestep

    def set(self, key, timestep):
        self.data[key] = timestep

    def get(self):
        return self.data

    
    def begin_time_track(self, key):
        self.time_tracks[key] = datetime.now()

    def end_time_track(self, key):
        dt:timedelta = datetime.now() - self.time_tracks[key]
        result = dt.microseconds/1000000
        if key not in self.data:
            self.data[key] = 0
        self.data[key] = self.data[key]+result

    def clear(self):
        self.data = {}
        self.time_tracks ={}

import sys
def get_size(obj, seen=None):
    """Recursively finds size of objects"""
    size = sys.getsizeof(obj)
    if seen is None:
        seen = set()
    obj_id = id(obj)
    if obj_id in seen:
        return 0
    # Important mark as seen *before* entering recursion to gracefully handle
    # self-referential objects
    seen.add(obj_id)
    if isinstance(obj, dict):
        size += sum([get_size(v, seen) for v in obj.values()])
        size += sum([get_size(k, seen) for k in obj.keys()])
    elif hasattr(obj, '__dict__'):
        size += get_size(obj.__dict__, seen)
    elif hasattr(obj, '__iter__') and not isinstance(obj, (str, bytes, bytearray)):
        size += sum([get_size(i, seen) for i in obj])
    return size
