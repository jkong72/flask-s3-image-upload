from flask import Flask, request
from flask_restful import Api
from werkzeug.utils import secure_filename
from flask.cli import run_command
import os

#configuration
from config import Config

#API
from resources.image import FileUploadResource

app = Flask(__name__)
app.config.from_object(Config)

#API
api = Api(app)
api.add_resource(FileUploadResource, '/data')

if __name__ == '__main__':
    app.run()