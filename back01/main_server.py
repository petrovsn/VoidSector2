import asyncio
import multiprocessing as mp
from threading import Thread
import time
import asyncio
import websockets
import json
import time
import secrets

from modules.ServerController import EngineSector_interactor
from modules.webEngine.flaskApp.flaskApp import ServerInteractorFlaskApp
from modules.webEngine.WebsocketController import WSController

if __name__ == '__main__':

    mp.set_start_method('spawn', force=True)
    server = EngineSector_interactor()
    server.init_server()
    server.start()

    loop = asyncio.new_event_loop()

    thread_async = Thread(target=loop.run_forever)
    asyncio.set_event_loop(loop)

    loop.create_task(WSController.main())
    loop.create_task(WSController.broadcast())
    loop.create_task(WSController.disauth_expired_tokens())
    loop.create_task(WSController.terminate_dead_tokens())

    # loop.create_task(WSController.clear_broken_connections())
    thread_async = Thread(target=loop.run_forever)
    thread_async.start()

    flask_app = ServerInteractorFlaskApp()
    flask_app.run_forever()

    print("server launched")
