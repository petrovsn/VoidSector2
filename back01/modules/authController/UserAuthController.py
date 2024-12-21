

#содержит с
from datetime import datetime, timedelta
import json
from loguru import logger
from modules.utils import ConfigLoader

class AccessRights:
    tabs = ["config_editor", "admin", "map_editor", "game_master", "pilot_master", "captain", "navigator", "cannoneer", "engineer", "medic", "master_medic", "NPC_pilot", "common_radar"]

#"map_editor": False, "admin":False, "game_master": False, "pilot": False, "captain":False,
#  "navigator":False, "cannoneer":False, "engineer":False, "NPC_pilot":False, "medic": False, "common_radar":False}


#у каждого юзера в системе есть корабль и список доступных панелей на этом корабле
#корабль null - админские роли.
class UserData:
    def __init__(self, ship, login, password, roles):
        self.ship = ship
        self.login = login
        self.password = password
        self.tabs = {}
        for role in AccessRights.tabs:
            self.tabs[role] = False
        if roles=='*':
            for role in AccessRights.tabs:
                self.tabs[role] = True
        else:
            for role in roles:
                self.tabs[role] = True

    def get_tabs(self):
        return self.tabs

    
    def get_available_tabs(self):
        result = []
        for tab in self.tabs:
            if self.tabs[tab]:
                result.append(tab)
        return result

    def set_tab_access(self, tab, state):
        if type(state) != bool:
            state = state.lower()=="true"
        self.tabs[tab] = state

    def auth(self, password):
        return password == self.password


class UsersControler:
    _instance = None # Приватное поле для хранения единственного экземпляра

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(UsersControler, cls).__new__(cls)
            cls._instance.users = {}
            cls._instance.update_auth_data()
        return cls._instance

    
    def update_auth_data(self):
        self.users = {}
        raw_auth_data = json.load(open('configs/auth.json'))


        
        for ship in raw_auth_data:
            for login in raw_auth_data[ship]:
                password = raw_auth_data[ship][login]["password"]
                roles = raw_auth_data[ship][login]["roles"]
                user_key = (ship, login)
                self.users[user_key] = UserData(ship, login, password, roles)

    #возвращает универсальный внутрисистемный логин пользователя
    def auth(self, ship, login, password):
        user_key = (ship, login)
        if user_key not in self.users:
            return None
        if self.users[user_key].auth(password):
            return user_key
        return None

    #возврщает None если токен бессрочный, возвращает timedelta, если пароль одноразовый
    def get_ttl(self, password)->timedelta:
        return None #timedelta(seconds=10)

        
    def get_state(self):
        result = {}
        for login in self.users:
            result[login] = self.users[login].get_tabs()
        return result



        
    def get_roles_list(self, login):
        result = []
        roles_dict = self.users[login].get_tabs()
        for role in roles_dict:
            if roles_dict[role]:
                result.append(role)

        return result

    
    def get_available_tabs(self, login):
        if login in self.users:
            return self.users[login].get_available_tabs()


    def set_tab_access(self, login, tab, state):
        if login in self.users:
            self.users[login].set_tab_access(tab, state)
