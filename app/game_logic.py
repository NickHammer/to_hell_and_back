from .models import Game, Player, Round, Card  # Adjust import paths as needed
from . import db
import random

def get_shuffled_deck():
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
    # This now returns a list of Card instances instead of dictionaries
    deck = [Card(suit=suit, value=value) for suit in suits for value in values]
    random.shuffle(deck)
    return deck

def assign_card_to_player(card, player):
    # Assuming Card has a player_id field for the ForeignKey relationship
    card.player_id = player.id
    db.session.add(card)

def deal_cards(game_id, round_number):
    game = Game.query.get_or_404(game_id)

    players = Player.query.filter_by(game_id=game_id).all()
    num_cards = calculate_cards_per_round(round_number)
    deck = get_shuffled_deck()

    # Assign cards to players
    for player in players:
        # Reset player's hand if necessary or manage previous cards
        # Example: player.cards.clear()
        
        for _ in range(num_cards):
            card = deck.pop(0)  # Take the top card from the deck
            assign_card_to_player(card, player)

    # Set the trump suit for the round
    trump_card = deck.pop(0)  # Take the next card to determine the trump suit
    current_round = Round(game_id=game_id, number=round_number, trump_suit=trump_card.suit)
    db.session.add(current_round)

    db.session.commit()

def calculate_cards_per_round(round_number):
    if round_number <= 10:
        return round_number
    else:
        return 20 - round_number
