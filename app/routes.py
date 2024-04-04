from flask import Blueprint, jsonify, request
from .models import Player, Game, Round, PlayerRound
from .game_logic import deal_cards
from . import db

bp = Blueprint('bp', __name__)

@bp.route('/game/create', methods=['POST'])
def create_game():
    data = request.get_json()
    name = data.get('name')
    if not name:
        return jsonify({'error': 'Game name is required'}), 400
    
    game = Game(name=name)
    db.session.add(game)
    db.session.commit()
    
    return jsonify({'message': 'Game created successfully', 'game': {'id': game.id, 'name': game.name}}), 201

@bp.route('/game/<int:game_id>/start', methods=['POST'])
def start_game(game_id):
    game = Game.query.get_or_404(game_id)
    if game.status != 'pending':
        return jsonify({'error': 'Game is already started or finished'}), 400

    # Logic to shuffle and deal cards, set the game status to 'active'
    # and determine the first player (simplified for example)
    game.status = 'active'
    deal_cards(game_id)  # You need to implement this function
    
    db.session.commit()
    return jsonify({'message': 'Game started', 'game': {'id': game.id, 'status': game.status}}), 200


@bp.route('/player/add', methods=['POST'])
def add_player():
    data = request.get_json()
    username = data.get('username')
    game_id = data.get('game_id')
    
    if not all([username, game_id]):
        return jsonify({'error': 'Username and game ID are required'}), 400
    
    game = Game.query.get(game_id)
    if not game:
        return jsonify({'error': 'Game not found'}), 404
    
    # Check if the username already exists in the database
    if Player.query.filter_by(username=username).first():
        return jsonify({'error': 'This username is already taken'}), 400
    
    player = Player(username=username, game_id=game_id)
    db.session.add(player)
    db.session.commit()
    
    return jsonify({'message': 'Player added successfully', 'player': {'id': player.id, 'username': player.username, 'game_id': player.game_id}}), 201

@bp.route('/game/<int:game_id>/round/<int:round_id>/bid', methods=['POST'])
def make_bid(game_id, round_id):
    data = request.get_json()
    player_id = data.get('player_id')
    bid = data.get('bid')
    # Find or create the PlayerRound entry
    player_round = PlayerRound.query.filter_by(player_id=player_id, round_id=round_id).first()
    if not player_round:
        player_round = PlayerRound(player_id=player_id, round_id=round_id)
    player_round.bid = bid
    db.session.add(player_round)
    db.session.commit()
    return jsonify({'message': 'Bid made', 'player': player_id, 'bid': bid}), 200

def play_card_logic(game_id, round_id, player_id, card_id):
    # Fetch the round, player, and card instances
    # Validate the play based on game rules
    # This might involve checking if it's the player's turn, if the card is in the player's hand,
    # and if the play follows the game's rules (e.g., following suit)
    # Update the game state accordingly
    pass


@bp.route('/game/<int:game_id>/round/<int:round_id>/play', methods=['POST'])
def play_card(game_id, round_id):
    data = request.get_json()
    player_id = data.get('player_id')
    card_id = data.get('card_id')  # Assuming each card has a unique ID

    round = Round.query.get_or_404(round_id)
    if round.game_id != game_id:
        return jsonify({'error': 'Round does not belong to this game'}), 400

    player = Player.query.get_or_404(player_id)
    if player.game_id != game_id:
        return jsonify({'error': 'Player does not belong to this game'}), 400

    card = Card.query.get_or_404(card_id)
    if card.player_id != player_id:
        return jsonify({'error': 'Card does not belong to the player'}), 400

    # Logic to play the card (simplified for example)
    play_card_logic(game_id, round_id, player_id, card_id)  # Implement based on your game rules
    
    db.session.commit()
    return jsonify({'message': 'Card played', 'player': player_id, 'card': card_id}), 200

