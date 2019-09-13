from flask import Flask, send_from_directory
from config import Config
from flask_bootstrap import Bootstrap
import os

app = Flask(__name__)
app.config.from_object(Config)
bootstrap = Bootstrap(app)



from app import routes, errors