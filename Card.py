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
            return "♡"
        elif self.suit == 1:
            return "♢"
        elif self.suit == 2:
            return "♠"
        elif self.suit == 3:
            return "♣" 
        else:
            return "Undefined" 
    
    def getNumName(self):
        if self.num >= 2 and self.num <= 10:
            return str(self.num)
        elif self.num == 1:
            return "A"
        elif self.num == 11:
            return "J"
        elif self.num == 12:
            return "Q"
        elif self.num == 13:
            return "K"
        else:
            return "Undefined"
        
    def getCardName(self):
        return self.getSuitName() + " " + self.getNumName()