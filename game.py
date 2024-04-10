import random


class DiscardPile:
    def __init__(self):
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)


class Deck:
    def __init__(self):
        self.cards = []
        self.values = {"A": 1, "4": 4, "5": 5, "6": 6, "7": 7, "S": 10, "C": 10, "R": 10}
        self.build()

    def build(self):
        self.cards = ["A", "A", "4", "5", "6", "7", "S", "C", "R", "R"] * 4

    def shuffle(self):
        self.cards = random.shuffle(self.cards)
        return self

    def draw_card(self):
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

    def count_points(self):
        self.points = sum([self.values[card] for card in self.hand])
        self.has_juego = self.points >= 31

    def count_pairs(self):
        pairs = 0
        for card in self.hand:
            if self.hand.count(card) == 2:
                pairs += 1
        return pairs
    
class BettingSystem:
    def __init__(self):
        self.pot = 0
        self.bet = 0
        self.better = None
        self.caller = None

    def bet(self, player, amount):
        if amount < 0:
            raise ValueError("Minimum bet is 2")
        self.better = player
        self.bet = amount

    def call(self, player):
        if player == self.better:
            raise ValueError("You can't call your own bet")
        self.caller = player

    def raise_bet(self, player, amount):
        if amount < self.bet + 2:
            raise ValueError("Minimum raise is 2 above previous bet")
        self.better = player
        self.bet, self.pot = amount, self.bet

    def fold(self, player):
        if player == self.better:
            raise ValueError("You can't fold your own bet")
        self.pot = max(self.pot, 1)   # in case it is still 0


class Game:
    def __init__(self):
        self.deck = Deck()
        self.discard_pile = DiscardPile()
        self.betting_system = BettingSystem()
        self.players = [Player(), Player(), Player(), Player()]

        # deal cards
        self.deal()

        # update flags for pairs and juego
        self.count_points()
        self.count_pairs()

        # 'mano' pointer
        self.mano = 0

        # score
        self.score = [0, 0]

    def reset(self):
        self.deck = Deck()
        self.discard_pile = DiscardPile()
        self.players = [Player(), Player(), Player(), Player()]

        # deal cards
        self.deal()

        # update flags for pairs and juego
        self.count_points()
        self.count_pairs()

        # 'mano' pointer
        self.mano += 1
        self.mano //= 4

    def deal(self):
        for _ in range(4):
            for player in self.players:
                player.draw(self.deck.draw_card())

    def count_points(self):
        for player in self.players:
            player.count_points()

    def count_pairs(self):
        for player in self.players:
            player.count_pairs()

    def discard(self, player, card):
        player.hand.remove(card)
        self.discard_pile.add_card(card)

    def mus(self, player, cards):
        for card in cards:
            self.discard(player, card)
            player.draw(self.deck.draw_card())

        self.count_pairs()
        self.count_points()

    def play(self):
        print("Still developing...")
