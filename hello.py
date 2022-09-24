import os
from flask import Flask
from dotenv import load_dotenv

app = Flask(__name__)

@app.route('/')
def index():
    return "<h1>Hello World!</h1>"

@app.route('/user/<name>')
def user(name):
    return "<h1>Hello, {}!</h1>".format(name)

if __name__ == '__main__':
    load_dotenv()
    app.run(debug = (os.getenv('env', 'production') == 'development'))