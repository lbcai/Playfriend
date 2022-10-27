from flask import Flask, redirect, request, jsonify, make_response, render_template, send_from_directory
from dotenv import load_dotenv
import os

import dns
import pymongo
import json
import time
import requests

app = Flask(__name__, static_folder="build/static", template_folder="build")

load_dotenv()
UPTIME_ROBOT_API_KEY = os.getenv('UPTIME_ROBOT_API_KEY')
MONGODB_URI = os.getenv('MONGODB_URI')
# Connect to database
client = pymongo.MongoClient(MONGODB_URI)
mongo_db = client.db
mongo_db.launches.drop()

@app.route('/')
def serve():
    return render_template('index.html')

@app.route('/send', methods=['POST'])
def new_submission():
    print('test')
    submission = request.get_json()
    print(submission)
    result = mongo_db.submissions.insert_one(submission)
    return make_response(jsonify(result=result.acknowledged))

@app.route('/tttleader', methods=['GET'])
def get_ttt_winners():
    # Filter tic tac toe games, then group by winner and sum for each winner.

    return make_response(jsonify(list(mongo_db.games.aggregate([{"$match" : {"game" : "Tic-Tac-Toe"}}, {"$group" : {"_id" : "$winner", "num_won" : {"$sum" : 1}}}]))))

@app.route('/tictactoe', methods=['GET'])
def get_ttt_games():
    ttt_games = list(mongo_db.games.find({"game": "Tic-Tac-Toe"}))
    # Remove pesky _id field which contains an object that can't be jsonified
    for item in ttt_games:
        item.pop('_id', None)

    return make_response(jsonify(ttt_games))

@app.route('/hangman', methods=['GET'])
def get_hm_games():
    hm_games = list(mongo_db.games.find({"game": "Hangman"}))
    for item in hm_games:
        item.pop('_id', None)

    return make_response(jsonify(hm_games))

@app.route('/status', methods=['POST'])
def get_uptime_robot():
    url = "https://api.uptimerobot.com/v2/getMonitors"

    payload = f"api_key={UPTIME_ROBOT_API_KEY}&format=json&logs=1"
    headers = {
        'content-type': "application/x-www-form-urlencoded",
        'cache-control': "no-cache"
        }
    response = requests.request("POST", url, data=payload, headers=headers)
    print(response.text)
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT')), debug=True)
