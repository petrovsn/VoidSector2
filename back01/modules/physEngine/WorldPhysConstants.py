from modules.utils import ConfigLoader
class WorldPhysConstants:
    _instance = None # Приватное поле для хранения единственного экземпляра

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(WorldPhysConstants, cls).__new__(cls)
            cls._instance.update_constants()
            cls._instance.frame_counter = 0
        return cls._instance

    
    def update_constants(self):
        self._gravity_constant = ConfigLoader().get("world.gravity_constant", float)
        self._fps = ConfigLoader().get("world.fps", float)
        self._timestep = 1/ConfigLoader().get("world.fps", float)

    @property
    def gravity_constant(self):
        return self._gravity_constant

    
    @property
    def fps(self):
        return self._fps

    
    @property
    def timestep(self):
        return self._timestep

    def next_step(self):
        self.frame_counter = self.frame_counter+1

    def seconds2ticks(self, seconds):
        return seconds/self.timestep

    def get_onetick_step(self, summary_value, summary_realtime):
        step_per_sec = summary_value/summary_realtime
        step_per_tick = step_per_sec/(1/self._timestep)
        return step_per_tick

            

    




        
