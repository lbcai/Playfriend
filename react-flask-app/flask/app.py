from flask import Flask, redirect
import time

app = Flask(__name__)


@app.route('/')
def index():
    return redirect("https://discord.com/oauth2/authorize?client_id=785345529722175498&permissions=470080&scope=bot")

@app.route('/time')
def get_current_time():
    return {'time': time.time()}

if __name__ == '__main__':
    app.run(debug=True)
