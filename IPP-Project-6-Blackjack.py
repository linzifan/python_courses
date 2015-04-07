# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = "Press Deal button!"
score = 0
win, lose = 0, 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank
        self.show = True

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        if self.show:
            card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                        CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
            canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        else:
            canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
       
        
# define hand class
class Hand:
    def __init__(self):
        self.cards = list()	# create Hand object

    def __str__(self):
        ans = "Hand contains "
        for item in self.cards:
            ans += str(item) + " "
        return ans	# return a string representation of a hand

    def add_card(self, card):
        self.cards.append(card)	# add a card object to a hand

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        value = 0
        aces = 0
        for card in self.cards:
            rank = card.get_rank()
            value += VALUES.get(rank)
            if rank == "A":
                aces += 1
        if aces == 0:
            return value
        else:
            if value + 10 <= 21:
                return value + 10
            else:
                return value
   
    def draw(self, canvas, pos):
        # draw a hand on the canvas, use the draw method for cards
        for i in range(len(self.cards)):
            self.cards[i].draw(canvas, (pos[0] + (80 * i), pos[1]))
        
# define deck class 
class Deck:
    def __init__(self):
        self.cards = list()  # create a Deck object
        for suit in SUITS:
            for rank in RANKS:
                self.cards.append(Card(suit, rank))

    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.cards)    # use random.shuffle()

    def deal_card(self):
        return self.cards.pop()	# deal a card object from the deck
    
    def __str__(self):
        ans = "Deck contains "
        for item in self.cards:
            ans += str(item) + " "
        return ans	# return a string representing the deck




#define event handlers for buttons
def deal():
    global outcome, in_play, deck, dealer, player, win, lose
    if in_play:
        lose += 1
    deck = Deck()
    deck.shuffle()
    dealer = Hand()
    player = Hand()
    for time in range(2):
        dealer.add_card(deck.deal_card())
        player.add_card(deck.deal_card())
    # print "Dealer: ", str(dealer)
    # print "Player: ", str(player)
    dealer.cards[0].show = False
    in_play = True
    outcome = "Hit or Stand?"

def hit():
    global outcome, in_play, player, win, lose
    if not in_play:
        return
    if player.get_value() <= 21:
        player.add_card(deck.deal_card())
        # print "Player: ", str(player)
        outcome = "Hit or Stand?"
    else:
        # print "You have busted"
        outcome = "You have busted! New deal?"
        in_play = False
        dealer.cards[0].show = True
        lose += 1
    
    
def stand():
    global outcome, in_play, player, dealer, win, lose
    if not in_play:
        return
    if player.get_value() > 21:
         # print "You have busted"
        outcome = "You have busted! New deal?"
        in_play = False
        dealer.cards[0].show = True
        lose += 1
    else:         
        while dealer.get_value() < 17:
            dealer.add_card(deck.deal_card())
        # print "Dealer: ", str(dealer)
        if dealer.get_value() > 21:
            # print "Dealer Busted!"
            outcome = "Dealer Busted! New deal?"
            in_play = False
            dealer.cards[0].show = True
            win += 1
        elif dealer.get_value() < player.get_value():
            # print "You win!"
            outcome = "You win! New deal?"
            in_play = False
            dealer.cards[0].show = True
            win += 1
        else:
            # print "You lose."
            outcome = "You lose. New deal?"
            in_play = False
            dealer.cards[0].show = True
            lose += 1
    
    
    
    
    
# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    canvas.draw_text("BLACKJACK", (20,50), 40, "Black")
    canvas.draw_text("Dealer", (80,130), 25, "White")
    dealer.draw(canvas, (100, 150))
    canvas.draw_text("Player", (80,280), 25, "White")
    player.draw(canvas, (100, 300))
    canvas.draw_text(outcome, (180, 280), 30, "Silver")
    canvas.draw_text("Win: ", (320, 40), 30, "White")
    canvas.draw_text(str(win), (400, 40), 30, "White")
    canvas.draw_text("Lose: ", (320, 70), 30, "White")
    canvas.draw_text(str(lose), (400, 70), 30, "White")
    


# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
dealer = Hand()
player = Hand()
frame.start()


# remember to review the gradic rubric