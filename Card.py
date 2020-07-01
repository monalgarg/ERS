class Card:
    def __init__(self, suit, num):
        self.suit = suit
        self.num = num

    def getSuit(self):
        return self.suit

    def getNum(self):
        return self.num
    
    def isFaceCard(self):
        return self.num == 1 or self.num >= 11

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