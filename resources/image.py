from flask_restful import Resource
from flask.cli import run_command
from werkzeug.utils import secure_filename
from flask import request
import os

# 파일 확장자명의 제어가 가능함.
# 화이트리스트
ALLOWED_EXTENSIONS = set( ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

# 확장자 검사 함수
def allowd_file(filename) :
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS


class FileUploadResource(Resource) :
    def post(self) :

        if 'photo' not in request.files: #파일 없는 경우
            return {'error':'파일이 없습니다.'}, 400

        file = request.files['photo'] #파일 가져오기

        # 파일 이름 확인
        if file.filename == '':
            return {'error':'파일 이름을 확인해주세요.'}, 400

        # 파일 저장
        if file and allowd_file(file.filename) :
            filename = secure_filename(file.filename)
            file.save(os.path.join('files'), filename)


        return {'result':'잘 저장되었습니다.'}