from datetime import date, datetime, timedelta
from flask import Flask, render_template, jsonify, request, redirect, url_for

app = Flask(__name__)

from pymongo import MongoClient

client = MongoClient('mongodb://3.38.96.45', 27017, username="test", password="test")
db = client.what_to_feed

# JWT 토큰을 만들 때 필요한 비밀번호와 같은 문자열.
# 내 서버에서만 토큰을 인코딩/디코딩이 가능하다.
SECRET_KEY = 'HANGHAE99'

# PYJWT 패키지 사용
import jwt

# 토큰 만료시간을 지정하기 위해 datetime 모듈 사용
import datetime

# 비밀번호는 암호화하여 DB에 저장해야 함. 그래야 개발자도 비밀번호를 알 수 없음
import hashlib


@app.route('/')
def home():
    # 클라이언트로 부터 토큰이 담긴 쿠키를 받는다.
    token_receive = request.cookies.get('mytoken')
    try:
        # payload 생성
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"username": payload['id']})
        return render_template('main.html', nickname=user_info["nickname"])
    # 토큰이 만료되었을 때
    except jwt.ExpiredSignatureError:
        return redirect(url_for("index", msg="login expired"))
    # 로그아웃해서 토큰이 없을 때
    except jwt.exceptions.DecodeError:
        return redirect(url_for("index", msg="not logged in"))

# 로그인 페이지
@app.route('/index')
def index():
    msg = request.args.get("msg")
    return render_template('index.html', msg=msg)


# @app.route('/register')
# def register():
#     return render_template('register.html')


# 아이디 중복 체크 API
@app.route('/sign_up/check_dup', methods=['POST'])
def check_dup():
    username_receive = request.form['username_give']
    exists = bool(db.users.find_one({"username": username_receive}))
    return jsonify({'result': 'success', 'exists': exists})


# 회원가입 완료 후 DB에 저장
@app.route('/sign_up/save', methods=['POST'])
def sign_up():
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']
    nickname_receive = request.form['nickname_give']
    password_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    doc = {
        "username": username_receive,
        "password": password_hash,
        "nickname": nickname_receive
    }
    db.users.insert_one(doc)
    return jsonify({'result': 'success'})


# 로그인 기능
@app.route('/sign_in', methods=['POST'])
def sign_in():
    # 로그인
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']

    pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    result = db.users.find_one({'username': username_receive, 'password': pw_hash})

    if result is not None:
        payload = {
         'id': username_receive,
         'exp': datetime.datetime.utcnow() + timedelta(seconds=60 * 60 * 24) # 로그인 24시간 유지
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        return jsonify({'result': 'success', 'token': token})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})


# 메인 페이지
# @app.route('/main')
# def main():
#     token_receive = request.cookies.get('mytoken')
#     # payload 생성
#     payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
#     user_info = db.users.find_one({"username": payload['id']})
#     return render_template('main.html')


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)