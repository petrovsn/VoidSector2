from flask import jsonify, make_response, request,Blueprint 
from datetime import datetime, timedelta
import time
from modules.ServerController import EngineSector_interactor

flask_endpoints_ep_game_engine = Blueprint("engine", __name__)
from loguru import logger
#region logs
#=====================================LOGS===============================================================


@flask_endpoints_ep_game_engine.route('/map', methods=["GET"])
def netstate():
    hObjects = EngineSector_interactor().get_sector_map()
    return make_response(jsonify({"hObjects":hObjects}), 200)







