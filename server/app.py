#!/usr/bin/env python3

# Import all utilities and modules
from flask import Flask, jsonify
from flask_migrate import Migrate
from models import db, Event, Session, Speaker, Bio

# Create the flask app
app = Flask(__name__)

# Configure the app
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

# Connect the app to the db to run and initilize it
migrate = Migrate(app, db)
db.init_app(app)

# Create all functionality for getting events at this route
@app.route('/events')
def get_events():
    # Search event's table rows in the db
    events = Event.query.all() 

    # Convert the event object into a dictionary so we can use jsonify
    return jsonify([
        {
            "id": e.id,
            "name": e.name,
            "location": e.location
        }

        for e in events

    ]), 200

# Create all functionality for sessions for an event at this route
@app.route('/events/<int:id>/sessions')
def get_event_sessions(id):
    # Find the event by its primary key
    event = db.session.get(Event, id)

    # Perform error handling if no event found return 404 
    if not event:
        return jsonify({"error": "Event not found"}), 404
    
    # Otherwise return all sessions for the event in jsonify form
    return jsonify([
        {
            "id": s.id,
            "title": s.title,
            "start_time": s.start_time.isoformat() if s.start_time else None
        }

        for s in events.sessions
    ]), 200

# Create all functionality for providing a list of all speakers with a specific id and name
@app.route('/speakers')
def get_speakers():
    # Search speaker's table rows in the db
    speakers = Speaker.query.all() 

    # Convert the speaker object into a dictionary so we can use jsonify
    return jsonify([
        {
            "id": s.id,
            "name": s.name,
            "location": s.location
        }

        for s in events

    ]), 200

# Create all functionality for providing a single speaker's bio
@app.route('/speakers/<int:id>')
def get_speaker(id):
    # Find the speaker by their primary key
    speaker = db.session.get(Speaker, id)

    # Perform error handling if no speaker found
    if not speaker:
        return jsonify({"error": "Speaker not found"}), 404
    
    # Otherwise provide bio 
    bio_text = speaker.bio.bio_text if speaker.bio else "No bio available"
    
    # jsonified
    return jsonify({
        "id": speaker.id,
        "name": speaker.name,
        "bio_text": bio_text
    }), 200

# Create all functionality for providing all speakers for a specific session with their bio text
@app.route('/sessions/<int:id>/speakers')
def get_session_speakers(id):
    # Find the session by its primary key
    session = db.session.get(Session, id)

    # Perform error handling if no session found with that ID
    if not session:
        return jsonify({"error": "Session not found"}), 404
    
    # Otherwise provide bio for all speakers for the session
    return jsonify([
        {
            "id": sp.id,
            "name": sp.name,
            "bio_text": sp.bio.bio_text if sp.bio else "No bio available"
        }
        for sp in session.speakers
    ]), 200


if __name__ == '__main__':
    app.run(port=5555, debug=True)