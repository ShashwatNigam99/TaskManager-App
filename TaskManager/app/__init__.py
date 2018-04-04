from flask import Flask
from config import Config

# make a variable named app a flask object
app = Flask(__name__)
app.config.from_object(Config)

from app import routes
