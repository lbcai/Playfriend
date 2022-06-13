from flask import Flask, redirect, request
from flask_mysqldb import MySQL
import os
import time

app = Flask(__name__)

app.config['MYSQL_HOST'] = os.getenv('CLEARDB_DATABASE_URL')
app.config['MYSQL_USER'] = os.getenv('CLEARDB_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('CLEARDB_PASS')
app.config['MYSQL_DB'] = os.getenv('CLEARDB_NAME')

mysql = MySQL(app)

@app.route('/')
def index():
    return redirect("https://discord.com/oauth2/authorize?client_id=785345529722175498&permissions=470080&scope=bot")

@app.route('/time')
def get_current_time():
    return {'time': time.time()}

if __name__ == '__main__':
    app.run(debug=True)
