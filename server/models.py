# Import necessary utilities and modules 
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.ext.associationproxy import association_proxy

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

# Create a db to connect to the Flask app
db = SQLAlchemy(metadata=metadata)

# Create the necessary association table for many-to-many relationship between Session and Speaker tables. Each row needs to hold the session_id and speaker_id to connect the session to the correct speaker.
session_speakers = db.Table(
    "session_speakers",
    db.Column("session_id", db.Integer, db.ForeignKey("sessions.id"), primary_key=True),
    db.Column("speaker_id", db.Integer, db.ForeignKey("speakers.id"), primary_key=True)
)


# Create relationships for all models
class Event(db.Model):

    # This dictates what table this maps to
    __tablename__ = 'events'

    # Create unique primary key for events
    id = db.Column(db.Integer, primary_key=True)
    # Declare other table attributes
    name = db.Column(db.String, nullable=False)
    location = db.Column(db.String, nullable=False)

    # Create one-to-many relationship because one event has multiple sessions. Don't forget to use back_populates='events' to connect it to the session. Deleting an orphan event should delete the session.
    sessions = db.relationship("Session", back_populates="events", cascade="all, delete-orphan") 


    # Provides a string when an event is printed
    def __repr__(self):
        return f'<Event {self.id}, {self.name}, {self.location}>'

# Create a session model to represent a single event. It should be many-to-one and have many speakers (many-to-many) 
class Session(db.Model):

    # Dictates what this table maps to
    __tablename__ = 'sessions'

    # Create unique primary key for each session
    id = db.Column(db.Integer, primary_key=True)
    # Declare other table attributes
    title = db.Column(db.String, nullable=False)
    start_time = db.Column(db.DateTime)
    event_id = db.Column(db.Integer)

    # Provides a string when an session is printed
    def __repr__(self):
        return f'<Session {self.id}, {self.title}, {self.start_time}>'

# Create speaker model to represent speakers for each session. Each person should have one bio as one to one, but speak at many sessions as many to many.
class Speaker(db.Model):

    # Dictates what this table maps to
    __tablename__ = 'speakers'

    # Create unique ids for each speaker
    id = db.Column(db.Integer, primary_key=True)
    # Declare other attributes for the speaker
    name = db.Column(db.String, nullable=False)

    # Provides a string when an speaker is printed
    def __repr__(self):
        return f'<Speaker {id}, {name}>'

# Create a biography model for the speaker. Each bio should belong to one and only one speaker as one to one.
class Bio(db.Model):

    # Declare what this table maps to
    __tablename__ = 'bios'

    # Create unique id
    id = db.Column(db.Integer, primary_key=True)
    # Create other attributes for the bio
    bio_text = db.Column(db.Text, nullable=False)
    speaker_id = db.Column(db.Integer)

    def __repr__(self):
        return f'<Bio {id}, {bio_text}>'
