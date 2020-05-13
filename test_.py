import pytest
from blocks import *

def test_card_showall():
    # show all 52 cards
    for suit in range(0,3):
        for value in range(0,13):
            card = Card(suit, value)
            card.show()

def test_deck_length():
    # test deck length
    testdeck = Deck()
    testdeck.shuffle()
    assert len(testdeck.cards) == 52

def test_deck_isEmpty():
    # draw 52 cards and test empty property
    testdeck = Deck()
    testdeck.shuffle()
    for card in range (0,len(testdeck.cards)):
        testdeck.drawCard()
    assert testdeck.isEmpty()

def test_deck_drawfromempty():
    testdeck = Deck()
    testdeck.shuffle()
    # empty the deck
    for card in range(0,len(testdeck.cards)):
        testdeck.drawCard()

    # draw from empty Deck
    testdeck.drawCard()

def test_deck_show():
    testdeck = Deck()
    testdeck.show()

def test_player_attributes():
    player = Player()
    
