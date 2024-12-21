
from flask import Flask, jsonify, make_response, request
from flask_cors import CORS
from flask import render_template
from gevent.pywsgi import WSGIServer
from modules.webEngine.flaskApp.blueprints.ep_auth import flask_endpoints_ep_auth
from modules.webEngine.flaskApp.blueprints.ep_server_admin import flask_endpoints_ep_server_admin
from modules.webEngine.flaskApp.blueprints.ep_game_engine import flask_endpoints_ep_game_engine

app = Flask(__name__)
cors = CORS(app)
app.register_blueprint(flask_endpoints_ep_auth, url_prefix='/auth')
app.register_blueprint(flask_endpoints_ep_server_admin, url_prefix='/admin')
app.register_blueprint(flask_endpoints_ep_game_engine, url_prefix='/game_engine')

class ServerInteractorFlaskApp:
    def __init__(self):
        pass

    def run_forever(self):
        http_server = WSGIServer(("0.0.0.0", 1924), app)
        http_server.serve_forever()



        



        
