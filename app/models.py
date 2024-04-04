from app import db
from datetime import datetime

class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    suit = db.Column(db.String(20), nullable=False)  # E.g., "Hearts"
    value = db.Column(db.String(20), nullable=False)  # E.g., "Ace"
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=True)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=False)
    round_id = db.Column(db.Integer, db.ForeignKey('round.id'), nullable=False)

    def __repr__(self):
        return f'<Card {self.value} of {self.suit}, Player {self.player_id}>'


class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    score = db.Column(db.Integer, default=0)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=True)  # Link to a Game
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    cards = db.relationship('Card', backref='player', lazy=True, cascade="all, delete-orphan")
    rounds = db.relationship('PlayerRound', back_populates='player')

    def __repr__(self):
        return f'<Player {self.username}>'

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), default='pending', index=True)  # Indexed for quicker search
    players = db.relationship('Player', backref='game', lazy=True, cascade="all, delete-orphan")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    cards = db.relationship('Card', backref='game', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Game {self.name}>'
    
class Round(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=False)
    number_of_cards = db.Column(db.Integer, nullable=False)
    trump_suit = db.Column(db.String(10), nullable=True)
    cards = db.relationship('Card', backref='round', lazy=True, cascade="all, delete-orphan")
    players = db.relationship('PlayerRound', back_populates='round')

    def __repr__(self):
        return f'<Round {self.id}, Game {self.game_id}, Cards: {self.number_of_cards}, Trump: {self.trump_suit}>'
    
class PlayerRound(db.Model):
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'), primary_key=True)
    round_id = db.Column(db.Integer, db.ForeignKey('round.id'), primary_key=True)
    bid = db.Column(db.Integer)
    player = db.relationship('Player', back_populates='rounds')
    round = db.relationship('Round', back_populates='players')

