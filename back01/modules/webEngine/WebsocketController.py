import secrets
import asyncio
import websockets
import json
from websockets.legacy.server import WebSocketServerProtocol
from modules.utils import Command, ConfigLoader
from modules.ServerController import EngineSector_interactor
from modules.authController.AuthTokenController import AuthTokenController
import time
from loguru import logger
import traceback
from datetime import datetime, timedelta
#from modules.physEngine.predictor import launch_new_TrajectoryPredictor_controller

class WSConnectionInfo:
    ping_limit = timedelta(seconds=ConfigLoader().get("system.ws_ping_limit", int))

    def __init__(self, websocket):
        self.websocket = websocket
        self.origin = websocket.origin
        self.token = secrets.token_urlsafe(ConfigLoader().get("system.token_length", int))
        self.authed = False
        self.auth_token = None
        self.pinged_at = datetime.now()

        
        #mode - нужноя для разных режимов передачи данных с игрового сервера на клиент
        #map_editor - то данные по расположению астероидов (hObjects) передаются в реал-тайме
        #ship_crew_<id> - передаются данные состояния только одного корабля
        self.mode = ""

    def get_info_str(self):
        return json.dumps({
            "token":self.token,
            "origin": self.origin
        })

    def auth(self, auth_token):
        self.authed = True
        self.auth_token = auth_token

    def disauth(self):
        self.authed = False
        self.auth_token = None

    def ping(self):
        self.pinged_at = datetime.now()

    def check_ping(self):
        return datetime.now()-self.pinged_at<WSConnectionInfo.ping_limit

    def get_info(self):
        return {
            "origin":self.origin,
            "ws_token": self.token,
            "auth_token": self.auth_token,
            "authed":self.authed,
            "last_ping_ago": (datetime.now() - self.pinged_at).seconds
        }

    async def send(self, *args, **kwargs):
        await self.websocket.send(*args, **kwargs)

class WSController:
    connections = {}

    def get_status():
        result = {}
        for token in WSController.connections:
            result[token] = WSController.connections[token].get_info()
        return result

    
    async def handler(websocket):
        token = None
        try:
            #получаем входящее соединение, сохраняем айпи и генерируем ws_token для него
            logger.info("ws connection initiated")
            connection_info = WSConnectionInfo(websocket)
            token = connection_info.token
            WSController.connections[connection_info.token] = connection_info
            logger.info(f"ws connection created: {WSController.connections[connection_info.token].get_info_str()}")

            #ожидаем входящей команды
            async for message in websocket:
                message_data = json.loads(message)
                command = Command(message_data)

                if command.contains_level("connection"):
                    #если команда относится к управлению соединениями, обрабатываем. Единственный случай когда 
                    #в функцию proceed_command передается не только сама команда, но и ws_токен соединения.
                    WSController.proceed_command(connection_info.token, command)
                else:
                    #перенаправляем на сервер, если соединение уже прошло авторизацию
                    if WSController.connections[connection_info.token].authed:
                        EngineSector_interactor().proceed_command(message_data)


        except Exception as e:
            logger.error(f"ws connection error: {str(traceback.format_exc())}", )

        if token:
            if token in WSController.connections:
                logger.info(f"ws connection terminated: {WSController.connections[token].get_info_str()}")
            else:
                logger.info(f"ws connection terminated: {token}")
        else:
            logger.info(f"ws connection terminated")


    

    def clear_connection(token):
        WSController.connections.pop(token)              

    def proceed_command(ws_token, command:Command):
        action = command.get_action()
        params = command.get_params()
        match action:
            case "auth":
                auth_token = params["auth_token"]
                if AuthTokenController().is_token_valid(auth_token):
                    WSController.connections[ws_token].auth(auth_token)

            case "ping":
                WSController.connections[ws_token].ping()

            
    async def broadcast():
        while True:
            try:
                active_entities = EngineSector_interactor().get_entities()
                admin_data = EngineSector_interactor().get_admin_data()
                tokens2delete = []
                for token in WSController.connections:
                    try:
                        if WSController.connections[token].authed:
                            sended_data = {"lObjects":active_entities,
                                           "admin":admin_data,
                                           }
                            await WSController.connections[token].send(json.dumps(sended_data))
                    except websockets.ConnectionClosedOK:
                        tokens2delete.append(token)
                for token in tokens2delete:
                    del WSController.connections[token]

            except Exception as e:
                logger.error(f"ws broadcast error: {str(traceback.format_exc())}", )
                del WSController.connections[token]
            await asyncio.sleep(0.02)


    async def disauth_expired_tokens():
        while True:
            try:
                to_disauth = []
                for ws_token in WSController.connections:
                    auth_token = WSController.connections[ws_token].auth_token
                    if auth_token:
                        if not AuthTokenController().is_token_valid(auth_token):
                            logger.info(f"ws clear tokens: {auth_token} auth_token tll expired", )
                            to_disauth.append(ws_token)

                for expired_ws_token in to_disauth:
                    WSController.connections[expired_ws_token].disauth()
                    logger.info(f"ws clear tokens: {expired_ws_token} expired", )

            except Exception as e:
                logger.error(f"ws clear tokens error: {str(traceback.format_exc())}", )
            await asyncio.sleep(1)


    async def terminate_dead_tokens():
        while True:
            try:
                to_terminate = []
                for ws_token in WSController.connections:
                    ping_alive = WSController.connections[ws_token].check_ping()
                    if not ping_alive:
                        logger.info(f"ws dead tokens: {ws_token} does not send ping")
                        to_terminate.append(ws_token)

                for ws_token in to_terminate:
                    try:
                        await WSController.connections[ws_token].websocket.close()
                        logger.info(f"ws dead tokens: {ws_token} close connection")
                    except Exception as e:
                        pass

                    
                    if ws_token in WSController.connections:
                        del WSController.connections[ws_token]
                        logger.info(f"ws dead tokens: {ws_token} delete connection")

            except Exception as e:
                logger.error(f"ws dead tokens: {str(traceback.format_exc())}")
            await asyncio.sleep(1)




    async def main():
        ip = ConfigLoader().get("system.ip")
        port = ConfigLoader().get("system.ws_port", int)
        async with websockets.serve(WSController.handler, ip, port):
            while True:await asyncio.sleep(0.04)
