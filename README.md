# to_hell_and_back
The card game "To Hell and Back"

# What decisions does AI Player need to make?
    1. Be able to recieve cards from the deck.
    2. Know what the "trump" suit is.
    3. Decide whether it makes bid first, or plays card first in the sequence of the round.
    4. Retain card or cards in hand and what suit, number, and face each card is.
    5. Determine what card to play relative to the trump suit, and the human player's play.
    6. Know how to bid on cards, based on how high or low they are, and their relation to trump suit.

# What are the rules of the game?
    - There are 19 rounds in the game. Each round, players recieve one more card than the last (Ex: Round 1, players get 1 card, Round 9, players get 9 cards, etc).
    - After round 10, the rounds decrease back to 1 [1,2,3,4,5,6,7,8,9,10,9,8,7,6,5,4,3,2,1]
    - The goal of the game is to accumulate the most points by collecting the amount of tricks you bid per round.

        Ex: | Player     | Bid | Round 5 (Five Tricks)  |
            | ---------- | --- | ---------------------- |
            | Player One | 2   | Takes 1 trick, loses   |
            | Player Two | 4   | Takes 4 tricks, *wins* |

    - Whichever suit the first player plays, has to be given up by the other players. If another player doesn't have that suit, they can play any suit.

        Ex: Player one plays a diamond, so player two HAS to play a diamond if they have one.

    - After the cards are dealt out to players, the next card in the deck is flipped over revealing the trump suit.
    - If a player wants a trick but cannot obtain it with a higher card that matches the dealt suit, they can play a trump card, assuming they do not have lower cards of the dealt suit.

        Ex: Trump is Hearts. Player one starts the round by playing a 9-spade. Player two can:
            1. Play a lower spade, losing the hand
            2. **Play a higher spade, winning the hand**
            3. Play a diamond or club if they have no spades, losing the hand.
            4. **Play a heart if they have no spades, winning the hand.**
