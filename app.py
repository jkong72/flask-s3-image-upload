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

            # S3와 연결 
            s3 = boto3.client('s3',
                        aws_access_key_id = app.config['ACCESS_KEY'],
                        aws_secret_access_key = app.config['SECRET_ACCESS'])
            
            try:
                s3.upload_fileobj(file,
                                app.config['S3_BUCKET'],
                                file.filename, # 현재 예제에서는 파일명을 그대로 사용하지만, 시간이나 닉네임등을 이용해 유니크하게 만들어줄 필요가 있음.
                                ExtraArgs = {'ACL' : 'public-read',
                                            'ContentType' : file.content_type}) 

            except Exception as e:
                return {'message':'에러가 발생했습니다.', 'error' : f'에러 코드 : {str(e)}' }
        

        # 업로드한 파일의 객체 url의 형식은 https:// (버킷).amazonaws.com/ (파일명) 형식이다.
        return {'result' : '잘 저장되었습니다.',
                'img_url' : app.config['S3_LOCATION'] + file.filename,
                'content' : request.form['content']}

                # 실제 이미지는 S3 (스토리지)에, url과 주석(파일에 대한 설명 등)은 RDS(DB)에 



api.add_resource(FileUpload,'/data')

if __name__ == '__main__':
    app.run()