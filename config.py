import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
    
    # MongoDB 設定
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/slot_machine")

    # Redis 設定
    REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT = os.getenv("REDIS_PORT", 6379)
    REDIS_DB = 0