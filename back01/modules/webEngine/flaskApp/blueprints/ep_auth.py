from flask import jsonify, make_response, request,Blueprint 
from datetime import datetime, timedelta
import time

flask_endpoints_ep_auth = Blueprint("auth", __name__)
from loguru import logger
#region logs
#=====================================LOGS===============================================================

from modules.authController.UserAuthController import UsersControler
from modules.authController.AuthTokenController import AuthTokenController

@flask_endpoints_ep_auth.route('/login', methods=["GET"])
def on_login():
    login = request.headers.get("login")
    password = request.headers.get("password")
    ship = request.headers.get("ship")
    inner_login = UsersControler().auth(ship, login, password)
    if not inner_login:
        return make_response(jsonify({}), 403)

    
    if inner_login:
        ttl = UsersControler().get_ttl(password)
        token = AuthTokenController().create_token(inner_login, ttl)

    return make_response(jsonify({"auth_token":token}), 200)

#при логауте должны вылететь все сессии этого пользователя
@flask_endpoints_ep_auth.route('/login', methods=["DELETE"])
def on_logout():
    auth_token = request.headers.get("auth_token")
    AuthTokenController().delete_token(auth_token)
    return make_response(jsonify(), 200)


#при логауте должны вылететь все сессии этого пользователя
@flask_endpoints_ep_auth.route('/tabs_access', methods=["GET"])
def tabs_access():
    auth_token = request.headers.get("authToken")
    inner_login = AuthTokenController().get_login(auth_token)
    if not inner_login:
        return make_response(jsonify(), 403)

    
    tabs = UsersControler().get_available_tabs(inner_login)
    return make_response(jsonify(tabs), 200)

    













