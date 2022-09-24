import os
from flask import Flask, render_template
from dotenv import load_dotenv

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)

if __name__ == '__main__':
    load_dotenv()
    app.run(debug = (os.getenv('env', 'production') == 'development'))