class AuthController:
    _instance = None # Приватное поле для хранения единственного экземпляра

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AuthController, cls).__new__(cls)


    def create_token(self, ttl):
        pass
