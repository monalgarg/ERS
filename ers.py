from random import shuffle
import copy
import sys,tty
from Card import Card
import time

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

        self.face_card_holder_player_indx = None
        self.attempts_left = None
        
        while (not self.isGameFinished()):
            player_indx = None
            while player_indx is None: 
                [player_indx, is_flip] = self.listen()
            
            self.resolveAction(player_indx, is_flip)

    def resolveAction(self, player_indx, is_flip):
        if is_flip: #flip
            if player_indx != self.turn: # someone played out of turn
                print("Player " + str(player_indx) + " played out of turn. Burn a card!")
                self.burnCard(player_indx)
            else: # regular flip
                card_played = self.players[player_indx].pop(0)
                self.cards_played.insert(0, card_played)

                print(card_played.getCardName())

                # face card stuff
                if card_played.isFaceCard(): 
                    self.face_card_holder_player_indx = player_indx
                    self.attempts_left = self.numTriesForFaceCard(card_played)

                    self.nextPlayerTurn()
                else:
                    if self.face_card_holder_player_indx is None:
                        self.nextPlayerTurn()
                    else:
                        self.attempts_left -= 1
                        if self.attempts_left == 0: # ran out of all tries    
                            is_valid_slap = self.buffer()

                            # if not is_valid_slap:
                            #     print("Player " + str(self.face_card_holder_player_indx) + " gets the deck!")
                            #     self.takePile(self.face_card_holder_player_indx)
        else: # slap
            print("Player " + str(player_indx) + " slapped!")

            slap_rules = self.checkSlaps()
            if slap_rules: # valid slap
                print(slap_rules)
                self.takePile(player_indx) # give the pile to player_indx
            else: # invalid slap
                print("Player " + str(player_indx) + " slapped incorrectly. Burn a card!")
                self.burnCard(player_indx)

    def buffer(self):
        player_indx_first_slap = None
        all_slappers = set()

        slap_rules = self.checkSlaps()

        t_end = time.time() + 3 # buffer of 3 seconds
        while time.time() < t_end:
            [player_indx, is_flip] = self.listen()
            if player_indx is not None and not is_flip: # someone slapped
                if player_indx_first_slap is None:
                    player_indx_first_slap = player_indx # record the first player who slapped

                    if player_indx == self.face_card_holder_player_indx and not slap_rules: # just taking the deck
                        print("Player " + str(player_indx) + " gets the deck!")
                        self.takePile(player_indx) # give the pile to player_indx
                        return

                print("Player " + str(player_indx) + " slapped!")
                all_slappers.add(player_indx)

        if slap_rules: # valid slap
            print(slap_rules)
            print("Player " + str(player_indx_first_slap) + " slapped first and gets the deck.")
            self.takePile(player_indx_first_slap) # give the pile to player_indx
            return True
        else:
            for i in all_slappers:
                if i != self.face_card_holder_player_indx:
                    print("Player " + str(i) + " slapped incorrectly. Burn a card!")
                    self.burnCard(i)
            print("Player " + str(self.face_card_holder_player_indx) + " gets the deck!")
            self.takePile(self.face_card_holder_player_indx) # give the pile to face_card_holder_player_indx
            return True

    def nextPlayerTurn(self):
        self.turn = (self.turn + 1) % self.num_players

    def takePile(self, player_indx):
        pile_copy = copy.deepcopy(self.cards_played)
        self.cards_played = []

        pile_copy.reverse()
        self.players[player_indx].extend(pile_copy)

        print("")
        print("Player " + str(player_indx) + " will now play a card.")
        self.turn = player_indx # reset turn to who slapped/got the deck

        self.face_card_holder_player_indx = None
        self.attempts_left = None

    def burnCard(self, player_indx):
        card_played = self.players[player_indx].pop(0)
        self.cards_played.append(card_played) # adds to end

        print("Burned " + card_played.getCardName())

    def numTriesForFaceCard(self, card):
        num = card.getNum()
        return 4 if num == 1 else num - 10

    # returns player name and whether or not it is a flip (true) or slap (false)
    # blocking listen for keystroke
    def listen(self):
        key = ord(sys.stdin.read(1))
        
        if key in self.keyboard_flip:
            return self.keyboard_flip[key], True
        elif key in self.keyboard_slap:
            return self.keyboard_slap[key], False
        else: 
            return None, None
                
    # ************ SLAP RULES ************

    def checkSlaps(self):
        slap_rules = ""

        slap_rules += self.checkDouble()
        slap_rules += self.checkSandwich()
        slap_rules += self.checkMarriage()
        slap_rules += self.checkTopAndBottom()
        slap_rules += self.checkAddToTen()
        slap_rules += self.addingRule()

        return slap_rules
        
    def checkDouble(self):
        if len(self.cards_played) >= 2:
            first_card = self.cards_played[0]
            second_card = self.cards_played[1]
        
            if first_card.getNum() == second_card.getNum():
                return "Double! "
        return ""
        
    def checkSandwich(self):
        if len(self.cards_played) >= 3:
            first_card = self.cards_played[0]
            second_card = self.cards_played[1]
            third_card = self.cards_played[2]
        
            if first_card.getNum() == third_card.getNum():
                return "Sandwich! "
        return ""
              
    def checkMarriage(self):
        if len(self.cards_played) >= 2:
            first_card = self.cards_played[0]
            second_card = self.cards_played[1]
            
            if ((first_card.getNum() == 12 and second_card.getNum() == 13) or 
            (first_card.getNum() == 13 and second_card.getNum() == 12)):
                return "Marriage !"
        return ""
                       
    def checkTopAndBottom(self):
        if len(self.cards_played) >= 3:
            bottom_card = self.cards_played[len(self.cards_played) - 1]
            top_card = self.cards_played[0]   
            
            if (bottom_card.getNum() == top_card.getNum()):
                return "Top and Bottom! "   
        return ""
    
    def checkAddToTen(self):
        if len(self.cards_played) >= 2:
            first_card = self.cards_played[0]
            second_card = self.cards_played[1]
            
            if first_card.getNum() + second_card.getNum() == 10:
                return "Add to Ten! " 
        return ""
            
    def addingRule(self):
        if len(self.cards_played) >= 3:
            first_card_num = self.cards_played[0].getNum()
            second_card_num = self.cards_played[1].getNum()
            third_card_num = self.cards_played[2].getNum()

            if (first_card_num + second_card_num == third_card_num or
                first_card_num + third_card_num == second_card_num or
                second_card_num + third_card_num == first_card_num):
                return "Adding rule! "
            if (first_card_num == 1 and second_card_num + third_card_num == 14 or
                second_card_num == 1 and first_card_num + third_card_num == 14 or 
                third_card_num == 1 and first_card_num + second_card_num == 14):
                return "Adding rule! "
        return ""

    def isGameFinished(self):
        for i, player_deck in enumerate(self.players):
            if len(player_deck) == 52:
                print("Player " + str(i) + " is the winner!")
                return True
        return False

game = ERS(2)
game.play()
