import requests
import json
import xmltodict
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbsparta

@app.route('/')
def home():
    return 'hello'

@app.route('/main', methods=['GET'])
def main():
    r = requests.get(
        'http://api.nongsaro.go.kr/service/recomendDiet/recomendDietList?apiKey=20211101HGX1FPG4TTRUPRUQ36Y8MA')
    dictionary = xmltodict.parse(r.text)
    json_object = json.dumps(dictionary, ensure_ascii=False)
    real_json = json.loads(json_object)
    print(real_json['response']['body']['items']['item'][0]) # json 변환
    return render_template('main.html', items=real_json)

if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)