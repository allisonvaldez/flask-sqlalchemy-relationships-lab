#!/usr/bin/env python3

# Import all utilities and modules
from flask import Flask, jsonify
from flask_migrate import Migrate

from models import db, Event, Session, Speaker, Bio

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

# TODO: add functionality to all routes

@app.route('/events')
def get_events():
    pass


@app.route('/events/<int:id>/sessions')
def get_event_sessions(id):
    pass


@app.route('/speakers')
def get_speakers():
    pass


@app.route('/speakers/<int:id>')
def get_speaker(id):
    pass


@app.route('/sessions/<int:id>/speakers')
def get_session_speakers(id):
    pass


if __name__ == '__main__':
    app.run(port=5555, debug=True)