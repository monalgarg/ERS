from random import shuffle
import copy
import sys,tty


class Card:
    def __init__(self, suit, num):
        self.suit = suit
        self.num = num
    
    def getSuit(self):
        return self.suit

    def getNum(self):
        return self.num
    
    def getSuitName(self):
        if self.suit == 0:
            return "Heart"
        elif self.suit == 1:
            return "Diamond"
        elif self.suit == 2:
            return "Spades"
        elif self.suit == 3:
            return "Clubs" 
        else:
            return "Undefined" 
    
    def getNumName(self):
        if self.num >= 2 and self.num <= 10:
            return str(self.num)
        elif self.num == 1:
            return "Ace"
        elif self.num == 11:
            return "Jack"
        elif self.num == 12:
            return "Queen"
        elif self.num == 13:
            return "King"
        else:
            return "Undefined"
        
    def getCardName(self):
        return self.getNumName() + " of " + self.getSuitName()

class Deck:
    def __init__(self):
        self.deck = []
        for i in range(4):
            for j in range(1, 14):
                c = Card(i, j)
                self.deck.append(c) 
                
    def shuffleDeck(self):
        shuffle(self.deck) 
        
    def printDeck(self):
        for i in self.deck:
            print(i.getCardName())  
            
    def getList(self):
        return self.deck     
    
class ERS:
    def __init__(self, num_players):        
        self.num_players = num_players
        self.cards_played = [] # middle pile
        self.players = [None] * self.num_players
        
        self.initalizeGame()
        tty.setcbreak(sys.stdin)  
        
    def initalizeGame(self):   
        # initalize 52 card deck 
        initial_deck = []
        for i in range(4):
            for j in range(1, 14):
                c = Card(i, j)
                initial_deck.append(c) 
        shuffle(initial_deck)
            
        # distributing cards amongst players
        cards_per_player = int(len(initial_deck) / self.num_players)
        remainder = len(initial_deck) % self.num_players
        
        start_card_indx = 0
        for i in range(self.num_players):
            self.players[i] = copy.deepcopy(initial_deck[start_card_indx : start_card_indx + cards_per_player])
            start_card_indx += cards_per_player
            
        for i in range(remainder):
               self.players[i].append(initial_deck[start_card_indx])
               start_card_indx += 1
               
        # set up keyboard input map
        self.keyboard_flip = {
            97  : 0, # 'a'
            102 : 1, # 'f'
            # 106 : 2, # 'j'
            # 108 : 3  # 'l'
        }
        
        self.keyboard_slap = {
            115 : 0, # 's'
            103 : 1, # 'g'
            # 107 : 2, # 'k'
            # 59  : 3  # ';'
        }
            
    def play(self):
        self.turn = 0
        print("Player 0 starts")
        
        while (not self.isGameFinished()):
            player_indx = None
            while player_indx is None: 
                [player_indx, is_flip] = self.listen()
            
            print(str(player_indx) + " " + str(is_flip))
            # flip card and other stuff
            self.turn = (self.turn + 1) % self.num_players
            
        # while(not input("") and len(self.deck.getList()) != 0):
        #     c = self.deck.getList().pop() # and add to whatever list you are growing
        #     self.cards_played.insert(0, c)
        #     print(c.getCardName())

        #     self.checkSlaps()

    # returns player name and whether or not it is a flip (true) or slap (false)
    def listen(self):
        key = ord(sys.stdin.read(1))
        
        if key in self.keyboard_flip:
            return self.keyboard_flip[key], True
        elif key in self.keyboard_slap:
            return self.keyboard_slap[key], False
        else: 
            return None, None
                
    def checkSlaps(self):
        self.checkDouble()
        self.checkSandwich()
        self.checkMarriage()
        self.checkTopAndBottom()
        self.checkAddToTen()
        
    def checkDouble(self):
        if len(self.cards_played) >= 2:
            first_card = self.cards_played[0]
            second_card = self.cards_played[1]
        
            if first_card.getNum() == second_card.getNum():
                print("Double!")
                return True
        
    def checkSandwich(self):
        if len(self.cards_played) >= 3:
            first_card = self.cards_played[0]
            second_card = self.cards_played[1]
            third_card = self.cards_played[2]
        
            if first_card.getNum() == third_card.getNum():
                print("Sandwich!")
                return True  
              
    def checkMarriage(self):
        if len(self.cards_played) >= 2:
            first_card = self.cards_played[0]
            second_card = self.cards_played[1]
            
            if (first_card.getNum() == "Queen" and second_card.getNum() == "King") or (first_card.getNum() == "King" and second_card.getNum() == "Queen"):
                print("Marriage!")
                return True
                       
    def checkTopAndBottom(self):
        if len(self.cards_played) >= 3:
            bottom_card = self.cards_played[len(self.cards_played) - 1]
            top_card = self.cards_played[0]   
            
            if (bottom_card.getNum() == top_card.getNum()):
                print("Top and Bottom!") 
                return True
    
    def checkAddToTen(self):
        if len(self.cards_played) >= 2:
            first_card = self.cards_played[0]
            second_card = self.cards_played[1]
            
            if first_card.getNum() + second_card.getNum() == 10:
                print("Add to Ten!")
                return True
            
    def isGameFinished(self):
        for i, player_deck in enumerate(self.players):
            if len(player_deck) == 52:
                print("Player " + str(i) + " is the winner!")
                return True
        return False

game = ERS(2)
game.play()
# for i, deck in enumerate(game.players):
#     print("PLAYER " + str(i) + " size of deck: " + str(len(deck)))
#     for j in deck:
#         print(j.getCardName())
#     print('\n')
    
# tty.setcbreak(sys.stdin)  
# key = ord(sys.stdin.read(1))  # key captures the key-code 
# # based on the input we do something - in this case print something
# if key==97:
#     print("you pressed a")
# else:
#     print("you pressed something else ...")
# sys.exit(0)