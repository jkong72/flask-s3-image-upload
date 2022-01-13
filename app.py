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

        # 사진(파일)과 텍스트 데이터를 함께 받을 수 있다.

        # from-data의 text 형식에서 데이터를 가져오는 경우
        # content 라는 키에 데이터를 받는다. (body)
        print(request.form['content'])

        # form-data의 file 형식에서 데이터를 가져오는 경우
        # photo 라는 키에 데이터를 받는다. (body)
        if 'photo' not in request.files:
            
            return {'error':'파일 업로드 하세요'}, 400
         
        file = request.files['photo']

        if file.filename == '':
            
            return {'error':'파일명을 정확히 입력하세요'}, 400

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename)) #로컬(파일시스템) 경로 저장

            

        
        return {'result' : '잘 저장되었습니다.'}       


api.add_resource(FileUpload,'/data')

if __name__ == '__main__':
    app.run()