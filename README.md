# Poker Preflop Trainer
- The Poker Preflop Trainer is a minimalist tool that allows the user to practice making preflop betting decisions in Texas Hold'em Poker.
- The main input is a 13x13 matrix, which we call a strategy grid. The grid defines the decisions to be made in a specific table position and scenario.
- Once the strategy is defined, the tool allows for rapid drilling of these bet vs. fold decisions. A % score is provided at the end of a pre-set number of hands.

## TODO
- test the tool
- create more of the strategy_grids so that more scenarios can be tested
- visualisation of progress
- trailing average score

## MECHANIC
### Core
We define Card, Deck and Player classes.

A Player object can draw cards from a deck object, giving it card objects that are contained within player.hand

### Training: Situations and Sessions
We also define a Situation class, which is used to construct a single table situation comprising of:
  - a freshly dealt pair of hole cards
  - the position or positions to be tested
  - the strategy_grid to be used to judge the decision

The Session class is designed to run a training session in three main stages:
  - controlling the table positions and situation types to be trained
  - generating N Situation instances and evaluating them
  - summarising Results

### Logging
We support logging of every Situation instance. As long as /logs directory existss, a log_default.csv will be appended with the detail of every completed Situation.

### Example Routine:
`session = Session()
session.runSession()
session.summariseSession()`
