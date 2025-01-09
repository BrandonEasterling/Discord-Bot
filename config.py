import random


PREFIX = "!"
games = {}

# Card and game logic
class Card:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit

    def __repr__(self):
        return f"{self.value} of {self.suit}"

# Create deck
def create_deck():
    suits = ['spades', 'diamonds', 'hearts', 'clubs']
    values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king', 'ace']
    spade_extras = ['ljoker', 'bjoker']

    # Create the initial deck
    deck = [Card(value, suit) for suit in suits for value in values]
    deck += [Card(extra, 'spades') for extra in spade_extras]

    # Remove specific cards
    deck = [card for card in deck if not (card.value == '2' and card.suit in ['hearts', 'clubs'])]

    return deck

# Deal cards
def deal(deck):
    random.shuffle(deck)
    hands = [deck[i:i+13] for i in range(0, len(deck), 13)]
    return hands[:4]
