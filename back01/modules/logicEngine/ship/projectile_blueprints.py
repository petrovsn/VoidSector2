from modules.physEngine.projectiles.projectiles_core import pjtl_Constructed
from modules.utils import ConfigLoader


class ProjectileConstructorController:
    _instance = None # Приватное поле для хранения единственного экземпляра

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ProjectileConstructorController, cls).__new__(cls)
            cls._instance.blueprints = {}
            cls._instance.prices = {}

        return cls._instance

    def get_basic_blueprints(self):
        return {
            "basic":{
                    "timer":1,
                    "inhibitor":1,
                    "thruster":0,
                    "explosive":1,
                    "emp":0,
                    "entities_detection":0,
                    "projectiles_detection":0,
                    "buster": 0,
                    "detonator":0,
                    "decoy":0
            },
            "torpedo":{
                    "timer":0,
                    "inhibitor":1,
                    "thruster":2,
                    "explosive":3,
                    "emp":0,
                    "entities_detection":0,
                    "projectiles_detection":0,
                    "buster": 0,
                    "detonator":0,
                    "decoy":0
            },
            "interceptor":{
                    "timer":0,
                    "inhibitor":1,
                    "thruster":1,
                    "explosive":0,
                    "emp":2,
                    "entities_detection":0,
                    "projectiles_detection":5,
                    "buster": 1,
                    "detonator":2,
                    "decoy":0
            },
            "interceptor_back":{
                    "timer":0,
                    "inhibitor":1,
                    "thruster":0,
                    "explosive":0,
                    "emp":2,
                    "entities_detection":0,
                    "projectiles_detection":5,
                    "buster": 1,
                    "detonator":2,
                    "decoy":0
            },
            "torpeda_mk2":{
                    "timer":3,
                    "inhibitor":0,
                    "thruster":2,
                    "explosive":3,
                    "emp":0,
                    "entities_detection":0,
                    "projectiles_detection":0,
                    "buster": 0,
                    "detonator":0,
                    "decoy":0
            },
            "basic_mk2":{
                    "timer":2,
                    "inhibitor":0,
                    "thruster":1,
                    "explosive":2,
                    "emp":0,
                    "entities_detection":0,
                    "projectiles_detection":0,
                    "buster": 0,
                    "detonator":0,
                    "decoy":0
            },
        }

    def initiate_ship_blueprints(self, ship_mark_id):
        basic_bps = self.get_basic_blueprints()
        self.blueprints[ship_mark_id] = basic_bps
        self.prices[ship_mark_id] = {}
        for bp_name in basic_bps:
            self.prices[ship_mark_id][bp_name] = self.get_blueprint_cost(basic_bps[bp_name])


    def append_blueprint(self, ship_mark_id, name, pjtl_description):
        self.blueprints[ship_mark_id][name] = pjtl_description
        self.prices[ship_mark_id][name] = self.get_blueprint_cost(pjtl_description)

    def get_blueprint(self, ship_mark_id, name):
        a = self.blueprints[ship_mark_id][name]
        return a



        
    def get_cost(self, ship_mark_id, name):
        a = self.prices[ship_mark_id][name]
        return a



        
    def get_volume(self, ship_mark_id, name):
        pjtl = pjtl_Constructed(None, None, self.blueprints[ship_mark_id][name], dumb = True)
        stats = pjtl.get_stats()
        return stats["details"]


    def get_blueprints_list(self, ship_mark_id):
        return(list(self.blueprints[ship_mark_id].keys()))

    def get_blueprint_cost(self, pjtl_description):
        sum = 0
        for comp_name in pjtl_description:
            sum = sum+ConfigLoader().get(f"projectile_builder_cost.{comp_name}", float)*pjtl_description[comp_name]
        return sum



        

    def get_production_time(self, pjtl_description):
        return 10

    def get_stats(self, pjtl_description):
        pjtl = pjtl_Constructed(None, None, pjtl_description, dumb=True)
        stats = pjtl.get_stats()
        stats["cost"] = self.get_blueprint_cost(pjtl_description)
        stats["production_time"] = 5 #stats["details"]*ConfigLoader().get(f"projectile_builder_cost.one_detail_time_production", float)
        return stats

    

    def get_description(self, mark_id):
        return {
            "blueprints":self.blueprints[mark_id]
        }

    
    def put_description(self, mark_id, descr):
        self.blueprints[mark_id] = descr["blueprints"]



        



        
