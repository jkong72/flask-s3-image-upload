from flask import Flask
from config import Config
from flask_restful import Resource, Api
from flask_restful import reqparse
from flask import Flask, request, redirect, jsonify
from werkzeug.utils import secure_filename
import os

import boto3, botocore


ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

app = Flask(__name__)
api = Api(app)
# 환경변수 셋팅
app.config.from_object(Config)


app.config['UPLOAD_FOLDER'] = 'files' # 데이터폴더 이미 있어야함.
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


class FileUpload(Resource):
    def post(self):

        if 'photo' not in request.files:
            
            return {'error':'파일 업로드 하세요'}, 400
         
        file = request.files['photo']

        if file.filename == '':
            
            return {'error':'파일명을 정확히 입력하세요'}, 400

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        
        return {'result' : '잘 저장되었습니다.'}       


api.add_resource(FileUpload,'/data')

if __name__ == '__main__':
    app.run()