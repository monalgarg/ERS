from random import shuffle
from Card import Card

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
    