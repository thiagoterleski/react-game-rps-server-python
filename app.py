#!flask/bin/python
from flask import Flask, jsonify

import time

app = Flask(__name__)

games = [
    {
        'id': 1,
        'hash': 'd41d8cd98f00b204e9800998ecf8427e',
        'created': time.strftime("%I:%M:%S")
    },
    {
        'id': 2,
        'hash': '07cc694b9b3fc636710fa08b6922c42b',
        'created': time.strftime("%I:%M:%S")
    },
]

@app.route('/')

def index():
    return "Hello, World!"

@app.route('/games', methods=['GET'])

def getGames():
    return jsonify({'games': games})

if __name__ == '__main__':
    app.run(debug=True)
