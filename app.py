from flask import Flask, redirect

app = Flask(__name__)


@app.route('/')
def index():
    return redirect("https://discord.com/oauth2/authorize?client_id=785345529722175498&permissions=470080&scope=bot")


if __name__ == '__main__':
    app.run()
