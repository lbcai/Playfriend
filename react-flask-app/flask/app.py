from flask import Flask, redirect, request
from dotenv import load_dotenv
import os
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


if __name__ == '__main__':
    app.run()
