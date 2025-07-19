
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security
from flask_wtf.csrf import CSRFProtect
from flask_restful import Api
import redis

db = SQLAlchemy()
security = Security()
csrf = CSRFProtect()
api_ref = Api()
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)
