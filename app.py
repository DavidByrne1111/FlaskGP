from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_lad():
    return 'Hello Lad!'


if __name__ == '__main__':
    app.run()
