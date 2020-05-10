# POKER PREFLOP TRAINER

from blocks import *

session = Session(handcount=10)
session.play()


"""
TODO

1. generate log of games
POSITION :: SHORTHAND :: DECISION :: STRATEGY :: CORRECT :: TIMESTAMP
UTG      :: AAo       :: "bet"    :: 1        :: TRUE    :: 2020-05-10_010136

2. ability to switch positions at the table and then use the new correct strategy grid

3. build more strategy tables

4. quiz one position but OR / ROL / 3BET scenarios

"""
