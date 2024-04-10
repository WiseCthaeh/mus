import random


class Deck:
    def __init__(self):
        self.cards = []
        self.values = {"A": 1, "4": 4, "5": 5, "6": 6, "7": 7, "S": 10, "C": 10, "R": 10}
        self.build()

    def build(self):
        self.cards = ["A", "A", "4", "5", "6", "7", "S", "C", "R", "R"] * 4

    def shuffle(self):
        self.cards = random.shuffle(self.cards)

    def drawCard(self):
        return self.cards.pop()
    

class Player:
    def __init__(self):
        self.hand = []
        self.values = {"A": 1, "4": 4, "5": 5, "6": 6, "7": 7, "S": 10, "C": 10, "R": 10}
        self.points = 0
        self.pairs = 0
        self.has_juego = False
        self.has_pares = False

    def draw(self, card):
        self.hand.append(card)
        return self

    def count_points(self):
        self.points = sum([self.values[card] for card in self.hand])
        self.has_juego = self.points >= 31

    def count_pairs(self):
        pairs = 0
        for card in self.hand:
            if self.hand.count(card) == 2:
                pairs += 1
        return pairs
    

class Game:
    def __init__(self):
        self.deck = Deck()
        self.player1 = Player()
        self.player2 = Player()
        self.player3 = Player()
        self.player4 = Player()
        
        # deal cards
        self.deal()

    def deal(self):
        for _ in range(4):
            self.player1.draw(self.deck.drawCard())
            self.player2.draw(self.deck.drawCard())
            self.player3.draw(self.deck.drawCard())
            self.player4.draw(self.deck.drawCard())