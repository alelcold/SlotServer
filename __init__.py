from flask import Flask
from config import Config
from extensions import mongo, redis_client
from routes import auth_blueprint, game_blueprint
from flask_socketio import SocketIO

socketio = SocketIO(cors_allowed_origins="*")  # WebSocket 支持

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # 初始化擴展
    mongo.init_app(app)
    redis_client.init_app(app)
    socketio.init_app(app)

    # 註冊 Blueprint
    app.register_blueprint(auth_blueprint, url_prefix="/auth")
    app.register_blueprint(game_blueprint, url_prefix="/game")

    return app