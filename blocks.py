import random
import csv
from datetime import datetime
from strategy import UTG_OR_grid
from strategy import strategy_grid_dict

class Card:
    suitList = ["Clubs", "Diamonds", "Hearts", "Spades"]
    rankList = ["narf", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King","Ace"]
    shortrankList = ["narf", "2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K","A"]

    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def __str__(self):
        return (self.rankList[self.value] + " of " +
                self.suitList[self.suit])

    def __cmp__(self, other):
        # check the suits
        # if self.suit > other.suit: return 1
        # if self.suit < other.suit: return -1
        # suits are the same... check ranks
        # ace is high
        # if (self.rank == 1 and other.rank != 1): return 1
        # if (self.rank != 1 and other.rank == 1): return -1
        if self.value > other.value: return 1
        if self.value < other.value: return -1
        return 0

    def show(self):
        print self

class Deck:
    def __init__(self):
        self.cards = []
        self.build()

    def __str__(self):
        print "\n"
        s = " "
        for i in range(len(self.cards)):
            s = s + " "*i + str(self.cards[i]) + "\n"
        return s

    def build(self):
        for s in range(0,3):
            for v in range(1, 14):
                self.cards.append(Card(s, v))

    def show(self):
        print self

    def shuffle(self):
        for i in range(len(self.cards) - 1, 0, -1): # iterate backwards
            r = random.randint(0, i) # choose a random pos r to swap with
            self.cards[i], self.cards[r] = self.cards[r], self.cards[i] # swap card i with r

    def drawCard(self):
        return self.cards.pop()

    def isEmpty(self):
        return (len(self.cards) == 0)

class Player:
    # mapping of position to positionlabel occurs here globally
    # lookups from strategy_grid_dict are based on label
    positionList = ["UTG", "MID", "CO", "BTN", "SB", "BB"]

    def __init__(self, name):
        self.name = name
        self.hand = []
        self.sitdown()

    def drawtoHand(self, deck, count=2):
        for i in range(0,count):
            self.hand.append(deck.drawCard())
        return self

    def showPosition(self):
        print ("{}".format(self.positionlabel))

    def sitdown(self,position=0):
        self.position = position
        self.positionlabel = self.positionList[self.position]

    def showHand(self,short=False):
        if short: print shortenHand(self.hand)
        else:
            s = " | "
            print s.join(str(c) for c in self.hand)

class Session:
    # a new Session class, that is designed to be even more modular, making use of the Situation class so streamline the flow

    def __init__(self, handcount=10, positionList=["UTG"], shufflepos=False, typeList=["OR", "ROL"], shuffletype=False):
        self.handcount = handcount
        self.handsplayed = 0
        self.currenthand = 1
        self.score = 0

        self.positionList = positionList
        self.position = 0
        self.positionlabel = self.positionList[self.position]
        self.shufflepos = shufflepos

        self.typeList = typeList
        self.type = 0
        self.typelabel = self.typeList[self.type]
        self.shuffletype = shuffletype
        self.printHeader()

    def printHeader(self):
        print "POKER PREFLOP TRAINER"
        print "  A new {} hand session has been initiated".format(self.handcount)
        print "  Positions to be tested: {}".format(self.positionList)
        print "  Situation types to be tested: {}".format(self.typeList)
        print "  Randomise position: {}".format(self.shufflepos)
        print "  Randomise situation type: {}".format(self.shuffletype)
        print ""

    def runSession(self):
        for i in range(0,self.handcount):
            sitch = Situation(name=self.currenthand, positionlabel = self.positionlabel, typelabel = self.typelabel)
            sitch.getDecision()
            sitch.evaluateDecision()

            # log and update session status with completed Situation info
            if sitch.decision == "quit":
                break
            elif sitch.decision == "no_grid":
                pass
            else:
                sitch.logSituation()
                self.handsplayed += 1
                self.score += sitch.score

            self.updatePosition()
            self.updateType()
            self.currenthand += 1

    def summariseSession(self):
        if self.handsplayed != 0:
            print "\n" +  ("{} out of {} hands completed.".format(self.handsplayed,self.handcount))
            print ("SCORE: " + str(self.score / float(self.handsplayed) * 100) + "%")

    def updatePosition(self):
        # update next table position
        if self.shufflepos:
            self.position = random.randint(0,len(self.positionList)-1)
        else:
            self.position = (self.position + 1) % len(self.positionList)
        self.positionlabel = self.positionList[self.position]

    def updateType(self):
        if self.shuffletype:
            self.type = random.randint(0,len(self.typeList)-1)
        else:
            self.type = (self.type + 1) % len(self.typeList)
        self.typelabel = self.typeList[self.type]

class Situation():

    def __init__(self, name, positionlabel, typelabel):
        self.name = name
        self.decision = False
        self.strategy = False
        self.strategy_grid = []
        self.score = 0
        self.player = Player('me')
        self.typelabel = typelabel
        self.positionlabel = positionlabel
        # ignore player possition attribute: situation now has its own positionlabel which is used for getting strategy_grid
        # self.player.sitdown(self.position)
        self.deck = Deck()
        self.deck.shuffle()
        self.player.drawtoHand(self.deck,count=2)

    def getDecision(self):
        prompt = "#" + str(self.name) + " : " + self.positionlabel + " : " + self.typelabel + " : " + shortenHand(self.player.hand)

        while True:
            try:
                decision_string = raw_input(prompt + " ? ")
            except ValueError:
                print("Sorry, I don't understand that. Bet or Fold? ")
                continue
            if decision_string == "":
                print("Sorry, I don't understand that. Bet or Fold? ")
                continue
            if decision_string[0].lower() == "f":
                decision = "fold"
                break
            if decision_string[0].lower() == "b":
                decision = "bet"
                break
            if decision_string[0].lower() == "q":
                decision = "quit"
                break
            else:
                print("Sorry, that's not an option. Bet or Fold. ")
                continue
        self.decision = decision

    def evaluateDecision(self):
        # once a decision has been made using situation.getDecision, this function decides what to do next and returns a True or False

        assert self.decision, "Attempted to evaluateDecision prior to decision being made"

        pos = str(self.positionlabel); typ = str(self.typelabel)
        self.strategy_grid = strategy_grid_dict[pos][typ]

        # assert len(self.strategy_grid)==13, "Required strategy grid not found: " + pos + "_" +typ +"_grid"
        if len(self.strategy_grid) != 13:
            self.decision = "no_grid"
            print ">> ?? No strategy grid found for {} {}. Skipping.".format(pos, typ)

        elif self.decision == "quit":
            print "You chose to quit. Bye for now."
            #or somehow return something that causes the Session instance to run endSession() function
        else:
            # explicit assigning of strategy string temporarily
            if (strategise(self.player.hand, self.strategy_grid) == 1):
                self.strategy = "bet"
            elif (strategise(self.player.hand, self.strategy_grid) == 0) :
                self.strategy = "fold"
            else:
                self.strategy = strategise(self.player.hand, self.strategy_grid)
                assert (self.strategy == 0 or self.strategy == 1), "Strategy grid value not equal to 0 or 1: " + self.strategy

            if self.decision == self.strategy:
                print ">> CORRECT"
                self.score = 1
                return True
            else:
                print ">> INCORRECT"
                return False

    def logSituation(self,logfile="./logs/log_default.csv"):
        dateTimeObj = datetime.now()
        timestampStr = dateTimeObj.strftime("%Y-%m-%d %H:%M:%S")
        position = self.positionlabel
        type = self.typelabel
        hand = shortenHand(self.player.hand)
        assert self.decision, "Attempted to log prior to decision being made"
        decision = self.decision
        assert self.strategy, "Attempted to log prior to strategy evaluation"
        strategy = self.strategy
        score = (decision == strategy)
        # TIMESTAMP, POSITION, HAND, DECISION, STRATEGY, SCORE
        row_entry = [timestampStr, position, type, hand, decision, strategy, score]

        with open(logfile, "a") as f:
            writer = csv.writer(f)
            writer.writerow(row_entry)

#####################
# GENERAL FUNCTIONS #
#####################

def logHand(player, decision, strategy, logfile="./logs/log_default.csv"):
    dateTimeObj = datetime.now()
    timestampStr = dateTimeObj.strftime("%Y-%m-%d %H:%M:%S")
    # TIMESTAMP, POSITION, HAND, DECISION, STRATEGY, CORRECT
    row_entry = [timestampStr,player.positionlabel, shortenHand(player.hand), decision, strategy, decision == strategy]
    with open(logfile, "a") as f:
        writer = csv.writer(f)
        writer.writerow(row_entry)

def strategise(hand, strategy_grid):
    gridpos = ""
    suited = False
    card1 = hand[0]
    card2 = hand[1]
    if card1.suit == card2.suit: suited = True
    gridpos = [card1.value, card2.value]
    if suited: gridpos.sort()
    else: gridpos.sort(reverse=True)
    row = 13 - gridpos[1]
    col = 13 - gridpos[0]
    return strategy_grid[row][col]

def shortenHand(hand):
    suited = False
    if len(hand) !=2:
        raise Exception("Only two-card hands can be shorthanded")
    else:
        if hand[0].suit == hand[1].suit:
            suited = True
        hand.sort()
        shorthand = hand[1].shortrankList[hand[1].value] + hand[0].shortrankList[hand[0].value]
        if suited: shorthand = shorthand + "s"
        else: shorthand = shorthand + "o"
    return shorthand
