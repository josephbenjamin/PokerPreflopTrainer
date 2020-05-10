# POKER PREFLOP TRAINER
import os
from blocks import *

# clear the terminal window
os.system('clear')

# instantiate and then play a session
#session = Session(handcount=5)
#session.play()
# for i in range(1,5):
#     sitch = Situation()
#     sitch.getDecision()
#     sitch.evaluateDecision()
#     if sitch.decision == "quit":
#         break
#     else: sitch.logSituation()
sesh = Session(handcount=2, positionList=["UTG", "MID"], typeList=["OR"], shufflepos=False,shuffletype=False)
sesh.runSession()
sesh.summariseSession()


"""
TODO

A. prepare more strategy_grids
B. create unit tests
C.

"""
