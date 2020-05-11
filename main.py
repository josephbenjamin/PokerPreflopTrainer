# POKER PREFLOP TRAINER
import os
from blocks import *

# clear the terminal window
os.system('clear')

sesh = Session(handcount=25, positionList=["UTG", "MID"], typeList=["OR"], shufflepos=True,shuffletype=False)
sesh.runSession()
sesh.summariseSession()

"""
TODO

A. prepare more strategy_grids
        OR  ROL 3Bet
    UTG  x    x    _
    MID  x    x    _
    CO   _    _    _
    BTN  _    _    _
    SB   _    _    _
    BB   _    _    _
B. create unit tests
    - check all grids are present
    - check all grids contain only 1 or 0
C. difficult mode
    i) focus on hardest hands only
    ii) only test differences between positiosn passed

"""
