import json
import random
from datetime import date, datetime, timedelta

import requests
import xmltodict
from flask import Flask, render_template, jsonify, request, redirect, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)

from pymongo import MongoClient

client = MongoClient('mongodb://3.35.19.169', 27017, username="test", password="test")
db = client.todaystable

# JWT 토큰을 만들 때 필요한 비밀번호와 같은 문자열.
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
        dishes = list(db.foodInfo.find({}, {'_id': False}).sort('likeCount', -1))
        for dish in dishes:
            dish["count_like"] = db.likes.count_documents({'foodNum':dish['no'], 'type':'heart'})
            dish["like_by_me"] = bool(db.likes.find_one({'foodNum':dish['no'], 'type':'heart', 'username':payload['id']}))
        recommends = random.sample(dishes, 3)

        return render_template('main.html', nickname=user_info["nickname"], dishes=dishes, recommends=recommends, user_pic=user_info["profile_pic_real"])
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


# 아이디 중복 체크 API
@app.route('/api/sign_up/check_dup', methods=['POST'])
def check_dup():
    username_receive = request.form['username_give']
    exists = bool(db.users.find_one({"username": username_receive}))
    return jsonify({'result': 'success', 'exists': exists})


# 회원가입 완료 후 DB에 저장
@app.route('/api/sign_up', methods=['POST'])
def sign_up():
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']
    nickname_receive = request.form['nickname_give']
    password_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    doc = {
        "username": username_receive,
        "password": password_hash,
        "nickname": nickname_receive,
        "profile_pic": "default_pic.jpg",
        "profile_pic_real": "profile_pics/default_pic.jpg"
    }
    db.users.insert_one(doc)
    return jsonify({'result': 'success'})


# 로그인 기능
@app.route('/api/sign_in', methods=['POST'])
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


# detail 페이지
@app.route('/detail/<keyword>')
def detail(keyword):
    food = db.foodInfo.find_one({'no' : keyword}, {'_id': False})
    comments = db.comments.find({'num': keyword}, {'_id': False})

    token_receive = request.cookies.get('mytoken')
    payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
    user_info = db.users.find_one({"username": payload['id']})
    user_pic = user_info["profile_pic_real"]

    username = user_info['username']
    nickname = user_info['nickname']

    food_recipe = db.foodManual.find({'num': keyword}, {'_id': False, 'num': False})[0]
    food_img = db.foodImg.find({'num': keyword}, {'_id': False, 'num': False})[0]

    return render_template('detail.html', food=food, comments=comments,
                           receipe=food_recipe, foodImg=food_img, username=username, nickname=nickname, user_pic=user_pic)


# 코멘트 저장
@app.route('/api/save_comment', methods=['POST'])
def save_comment():
    comment_receive = request.form['comment_give']
    num_receive = request.form['num_give']
    time_receive = request.form['time_give']

    token_receive = request.cookies.get('mytoken')
    payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
    user_info = db.users.find_one({"username": payload['id']})
    username = user_info['username']
    nickname = user_info['nickname']
    user_pic = user_info['profile_pic_real']

    doc = {
        "num": num_receive,
        "username": username,
        "nickname": nickname,
        "comment": comment_receive,
        "time": time_receive,
        "profile_pic_real": user_pic
    }

    db.comments.insert_one(doc)

    return jsonify({'result': 'success', 'msg': 'Comment 저장 성공'})


# 코멘트 불러오기
@app.route('/api/get_comments', methods=['POST'])
def get_comments():
    num_receive = request.form['num_give']
    comments = list(db.comments.find({'num': num_receive}, {'_id': False}).sort("time", -1))

    return jsonify({'result': 'success', 'comments': comments})


# 코멘트 삭제하기
@app.route('/api/delete_comment', methods=['POST'])
def delete_comment():
    username_receive = request.form['username_give']
    comment_receive = request.form['comment_give']
    db.comments.delete_one({'username': username_receive, 'comment': comment_receive})

    return jsonify({'result': 'success', 'msg': '코멘트가 삭제되었습니다.'})


@app.route('/update_like', methods=['POST'])
def update_like():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])

        user_info = db.users.find_one({"username": payload["id"]})
        food_num_receive = request.form["food_num_give"]
        type_receive = request.form["type_give"]
        action_receive = request.form["action_give"]
        doc = {
            "foodNum": food_num_receive,
            "username": user_info["username"],
            "type": type_receive
        }
        if action_receive == "like":
            db.likes.insert_one(doc)
        else:
            db.likes.delete_one(doc)
        count = db.likes.count_documents({"foodNum": food_num_receive, "type": "heart"})
        db.foodInfo.update({"no": food_num_receive}, {"$set": {"likeCount": count}})
        return jsonify({"result": "success", 'msg': 'updated', "count": count})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("/"))


# 마이 페이지
@app.route('/user')
def user():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"username": payload["id"]}, {"_id": False})
        user_pic = db.users.find_one({"username": payload["id"]}, {"_id": False})["profile_pic_real"]
        comments = list(db.comments.find({"username": payload["id"]}, {"_id": False}))
        food_info = {}
        for comment in comments:
            food_info["num"] = db.foodInfo.find_one({"no":comment["num"]})["no"]
            food_info[comment["num"]] = db.foodInfo.find_one({"no":comment["num"]})["menu_name"]

        return render_template('user.html', user_info=user_info, nickname=user_info["nickname"], food_info=food_info, comments=comments, user_pic=user_pic)
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("/"))

#
# @app.route('/api/time_string', methods=['POST'])
# def time_string():
#     time_receive = request.form['time_give']
#     return render_template('user.html', time_string=time_receive)


# 마이페이지 코멘트 불러오기
@app.route('/api/get_my_comments', methods=['GET'])
def get_my_comments():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"username": payload["id"]}, {"_id": False})
        food_info = list(db.foodInfo.find({}, {"_id": False}))
        # food_info = {}
        # for comment in comments:
        #     food_info[comment["num"]] = db.foodInfo.find_one({"no":comment["num"]})["menu_name"]
        #     food_infos.append(food_info)
        return jsonify({'result': 'success', 'user_info': user_info})
        #, 'comments': comments, 'food_info': food_info}
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("/"))


#음식 추천
@app.route('/api/recommend_food', methods=['POST'])
def recommend_food():
    answer1 = request.form['answers1']
    answer2 = request.form['answers2']
    answer3 = request.form['answers3']

    main_dish = db.foodInfo.find({'menu_type': '밥'}, {'_id': False})
    dessert = db.foodInfo.find({'menu_type': '후식'}, {'_id': False})

    r = main_dish if answer1 == "밥" else dessert

    r2 = []
    for i in r:
        if answer2 == "고단백":
            if float(i['protein']) > 25:
                r2.append(i)
                print(r2)
        else:
            if float(i['natrium']) < 100:
                r2.append(i)
                print(r2)

    r3 = []
    for i in r2:
        if answer3 == "다이어트식":
            if float(i['calorie']) < 300:
                r3.append(i)
                print(r3)
        else:
            if float(i['calorie']) > 500:
                r3.append(i)
                print(r3)

    result = random.sample(r3, 1)
    # result = {'no': '16', 'menu_name': '누룽지 두부 계란죽', 'menu_howto': '끓이기', 'menu_type': '밥', 'calorie': '380', 'carbo': '67', 'protein': '12', 'fat': '7', 'natrium': '271', 'ingredient': '채소준비\n애호박 30g(1/6개), 표고버섯 20g(2개), 당근 5g(3×2×1cm)\n누룽지 죽\n누룽지 70g(1/3컵), 순두부 100g(1/4모), 달걀 50g(1개),참기름 3g(2/3작은술), 소금 약간, 참깨 약간, 흰 후추 약간', 'img': 'http://www.foodsafetykorea.go.kr/uploadimg/cook/10_00016_1.png', 'Manual01': '1. 깨끗이 씻어 손질한 애호박, 당근과 기둥을 뗀 표고버섯을 잘게 다지듯이 썬다.a', 'FoodImg01': 'http://www.foodsafetykorea.go.kr/uploadimg/cook/20_00016_1.png', 'Manual02': '2. 누룽지는 1cm 정도로 잘게 부숴준다.b', 'FoodImg02': 'http://www.foodsafetykorea.go.kr/uploadimg/cook/20_00016_2.png', 'Manual03': '3. 냄비에 참기름을 두르고 썰어놓은 채소를 볶다가 누룽지와 물을 넣고 끓인다.', 'Manual04': '4. 누룽지가 살짝 퍼지면 순두부를 넣고 흰후추와 소금을 넣는다.', 'Manual05': '5. 죽이 끓으면 달걀을 풀어 넣고 한 소끔 끓여낸 후 참깨를 뿌려 마무리 한다.c', 'FoodImg05': 'http://www.foodsafetykorea.go.kr/uploadimg/cook/20_00016_5.png', 'likeCount': 1}
    return jsonify({'result': 'success', 'recommended': result})

# 프로필 수정
@app.route('/update_profile', methods=['POST'])
def update_profile():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        username = payload["id"]
        nickname_receive = request.form["nickname_give"]
        new_doc = {
            "nickname": nickname_receive,
        }
        if 'file_give' in request.files:
            file = request.files["file_give"]
            filename = secure_filename(file.filename)
            extension = filename.split(".")[-1]
            file_path = f"profile_pics/{username}.{extension}"
            file.save("./static/"+file_path)
            new_doc["profile_pic"] = filename
            new_doc["profile_pic_real"] = file_path
        db.users.update_one({'username': payload['id']}, {'$set':new_doc})
        db.comments.update_many({'username': payload['id']}, {'$set': {'nickname': nickname_receive}})
        return jsonify({"result": "success", 'msg': '프로필을 업데이트했습니다.'})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("/"))


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
