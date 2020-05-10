import random
from strategy import *

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

    def __init__(self, handcount):
        self.handcount = handcount
        self.score = 0
        print '\n'
        print "POKER PREFLOP TRAINER"
        print ">> A New session has been initiated"
        print ">> Length: {} hands \n".format(self.handcount)

    def play(self):

        for i in range(1,self.handcount + 1):
            decision = ""
            player = Player('me')
            deck = Deck()
            deck.shuffle()

            # print "\n" + "Hand {}".format(i)
            player.drawtoHand(deck,count=2)
            #player.showPosition()
            #player.showHand(short=True)

            # ultra short info
            print "h" + str(i) + " :: " + player.positionlabel + " :: " + shortenHand(player.hand)

            while True:
                try:
                    decision_string = raw_input("b/f? ")
                except ValueError:
                    print("Sorry, I don't understand that. Bet or Fold. ")
                    continue
                if decision_string[0].lower() == "f":
                    decision = 0
                    break
                if decision_string[0].lower() == "b":
                    decision = 1
                    break
                if decision_string[0].lower() == "q":
                    decision = "quit"
                    break
                else:
                    print("Sorry, that's not an option. Bet or Fold. ")
                    continue

            # get a decision from the player
            # evaluate the player's decision
            if decision == "quit":
                print "You chose to quit. Bye for now."
                break
            elif decision == strategise(player.hand, UTG_OR_grid):
                print "CORRECT"
                self.score += 1
                continue
            else:
                print "INCORRECT"
                continue
        # indicate that all hands are complete
        print "\n" +  ("{} out of {} hands completed.".format(i,self.handcount))
        print ("SCORE: " + str(self.score / float(self.handcount) * 100) + "%")

#####################
# GENERAL FUNCTIONS #
#####################

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
