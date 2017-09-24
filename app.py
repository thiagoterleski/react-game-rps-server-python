from flask import Flask, g, abort, jsonify, make_response
from pprint import pprint
import time, uuid, sqlite3
from aiohttp import web
from flask_socketio import SocketIO, join_room, leave_room

DATABASE = 'database.db'

app = Flask(__name__)

socketio = SocketIO(app)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    return (rv[0] if rv else None) if one else rv

@app.route('/')

def index():
    return "Start app"

# List games
@app.route('/game', methods=['GET'])
def get_games():
    cur = get_db().execute('select * from game')
    return jsonify({ 'results': cur.fetchall()})

# Get game by id
@app.route('/game/<string:game_id>', methods=['GET'])
def get_game(game_id):
    cur = get_db().execute("select * from game WHERE id = ?", [game_id])
    game = cur.fetchone()
    return jsonify({ 'game': game })

# Create a new Game
@app.route('/game', methods=['POST'])
def create_game():
    game_hash = str(uuid.uuid1())
    cur = get_db().execute("insert into game (id) values (?)", [game_hash])
    get_db().commit()

    return jsonify({ 'result': game_hash })

# Socket functions


if __name__ == '__main__':
    socketio.run(app)


