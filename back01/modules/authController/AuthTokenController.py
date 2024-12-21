import secrets
from datetime import datetime, timedelta
from modules.utils import ConfigLoader

class AuthTokenInfo:
    def __init__(self, login, ttl) -> None:
        self.login = login
        self.timeout = datetime.now()+ttl if ttl else None

    
    def is_valid(self):
        if not self.timeout: return True
        return datetime.now()<self.timeout

class AuthTokenController:
    _instance = None # Приватное поле для хранения единственного экземпляра

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AuthTokenController, cls).__new__(cls)
            cls.tokens = {}
        return cls._instance

    
    def create_token(self, inner_login, ttl):
        new_token = secrets.token_urlsafe(ConfigLoader().get("system.token_length", int))
        self.tokens[new_token] = AuthTokenInfo(inner_login, ttl)
        return new_token

    def delete_token(self, token):
        del self.tokens[token]

    def get_login(self, token):
        if token in self.tokens:
            return self.tokens[token].login
        return None

    
    def is_token_valid(self,token):
        if token in self.tokens:
            tokeninfo = self.tokens[token]
            return tokeninfo.is_valid()
        return False
