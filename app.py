from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return "redirect"


if __name__ == '__main__':
    app.run()
