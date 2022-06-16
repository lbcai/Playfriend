from flask import Flask, redirect, request, jsonify
from dotenv import load_dotenv
import os

import dns
import pymongo
import json
import time

app = Flask(__name__)

load_dotenv()
MONGODB_URI = os.getenv('MONGODB_URI')
# Connect to database
client = pymongo.MongoClient(MONGODB_URI)
mongo_db = client.db
mongo_db.launches.drop()


@app.route('/')
def index():
    return redirect("https://discord.com/oauth2/authorize?client_id=785345529722175498&permissions=470080&scope=bot")


@app.route('/time')
def get_current_time():
    return {'time': time.time()}

@app.route('/tttleader')
def get_ttt_winners():
    # Filter tic tac toe games, then group by winner and sum for each winner.
    return jsonify(list(mongo_db.games.aggregate([{"$match" : {"game" : "Tic-Tac-Toe"}}, {"$group" : {"_id" : "$winner", "num_won" : {"$sum" : 1}}}])))

@app.route('/tictactoe')
def get_ttt_games():
    ttt_games = list(mongo_db.games.find({"game": "Tic-Tac-Toe"}))
    # Remove pesky _id field which contains an object that can't be jsonified
    for item in ttt_games:
        item.pop('_id', None)

    return jsonify(ttt_games)

@app.route('/hangman')
def get_hm_games():
    hm_games = list(mongo_db.games.find({"game": "Hangman"}))
    for item in hm_games:
        item.pop('_id', None)

    return jsonify(hm_games)

if __name__ == '__main__':
    app.run()
