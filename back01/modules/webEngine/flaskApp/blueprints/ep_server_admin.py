from flask import jsonify, make_response, request,Blueprint 
from datetime import datetime, timedelta
import time

flask_endpoints_ep_server_admin = Blueprint("admin", __name__)
from loguru import logger
#region logs
#=====================================LOGS===============================================================
from modules.webEngine.WebsocketController import WSController

@flask_endpoints_ep_server_admin.route('/ws_connections', methods=["GET"])
def netstate():
    result = WSController.get_status()
    return make_response(jsonify({"connections":result}), 200)


@flask_endpoints_ep_server_admin.route('/ws_connections/<ws_token>', methods=["DELETE"])
def del_connection(ws_token):
    #result = WSController.get_status()
    return make_response(None, 200)








