import random
from collections import Counter
import matplotlib.pyplot as plt

# Global constants
PARES = ["AA", "44", "55", "66", "77", "SS", "CC", "RR"]
MEDIAS = ["AAA", "444", "555", "666", "777", "SSS", "CCC", "RRR"]
DUPLES = {str(i + j): k for k, (i, j) in enumerate((x, y) for x in PARES for y in PARES if PARES.index(x) <= PARES.index(y))}
PARES_DICT = {par: count + 1 for count, par in enumerate([*PARES, *MEDIAS, *DUPLES.keys()])}
VAL = {'A': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, 'S': 10, 'C': 10, 'R': 10}
JUEGO_PUNTOS = {31: 3, 32: 2, 33: 2, 34: 2, 35: 2, 36: 2, 37: 2, 40: 2}

class Card:
    def __init__(self, rank):
        self.rank = rank

class Deck(list):
    def __init__(self, full=True):
        ranks = ["A", "A", "4", "5", "6", "7", "S", "C", "R", "R"]
        if full:
            [[self.append(Card(rank)) for rank in ranks] for _ in range(4)]
    
    def shuffle(self):
        random.shuffle(self)

class Player:
    def __init__(self, name, team):
        self.name = name
        self.team = team
        self.hand = []
        self.is_mano = False
        self.pares = ''
        self.pares_strength = 0
        self.juego = 0
        self.has_pares = False
        self.has_juego = False
    
    def draw(self, card):
        self.hand.append(card)
    
    def show_hand(self):
        return ''.join([card.rank for card in self.hand])
    
    def sort_hand(self):
        self.hand.sort(key=lambda card: VAL[card.rank])
    
    def check_pares(self):
        card_counts = Counter(card.rank for card in self.hand)
        self.pares = ''.join(sorted(card for card, count in card_counts.items() if count >= 2))
        if self.pares:
            self.pares_strength = PARES_DICT.get(self.pares, 0)
            self.has_pares = True
    
    def check_juego(self):
        self.juego = sum(VAL[card.rank] for card in self.hand)
        self.has_juego = self.juego >= 31

class Game:
    def __init__(self, team1_names, team2_names):
        self.teams = {"team1": [Player(name, "team1") for name in team1_names],
                      "team2": [Player(name, "team2") for name in team2_names]}
        self.players = [self.teams["team1"][0], self.teams["team2"][0], self.teams["team1"][1], self.teams["team2"][1]]
        self.deck = Deck(full=True)
        self.team_scores = {"team1": 0, "team2": 0}
        self.mano_index = 0
        self.fr_pares = {'Nada': 0, 'Par': 0, 'Medias': 0, 'Duples': 0}
        self.fr_juego = {i: 0 for i in range(31, 41)}
        self.total_juego = 0
        self.runs = 0
    
    def deal(self, player, n=1):
        for _ in range(n):
            player.draw(self.deck.pop())
    
    def deal_players(self):
        for player in self.players:
            self.deal(player, n=4)
            player.sort_hand()
            player.check_pares()
            player.check_juego()
    
    def simulate(self, runs):
        self.runs = runs
        for _ in range(runs):
            self.deck = Deck(full=True)
            self.deck.shuffle()
            self.deal_players()
            for player in self.players:
                # Count pares frequency
                if player.pares == '':
                    self.fr_pares['Nada'] += 100 / runs
                elif len(player.pares) == 2:
                    self.fr_pares['Par'] += 100 / runs
                elif len(player.pares) == 3:
                    self.fr_pares['Medias'] += 100 / runs
                else:
                    self.fr_pares['Duples'] += 100 / runs
                
                # Count juego frequency
                if player.juego > 30:
                    self.fr_juego[player.juego] += 1
                    self.total_juego += 1

        # Normalize juego frequencies
        self.fr_juego = {key: 100 * value / self.total_juego for key, value in self.fr_juego.items()}
        self.plot_results()
    
    def plot_results(self):
        # Plot frequency of Juego
        plt.figure(1)
        plt.bar(self.fr_juego.keys(), self.fr_juego.values(), color='g')
        plt.xlabel('Juego')
        plt.ylabel('Frecuencia (%)')
        plt.title('Juego')

        # Plot frequency of Pares
        plt.figure(2)
        plt.bar(self.fr_pares.keys(), self.fr_pares.values(), color='b')
        plt.xlabel('Tipo de Pares')
        plt.ylabel('Frecuencia (%)')
        plt.title('Pares')
        plt.show()

        print('Probabilidad de juego:', self.total_juego / self.runs)


if __name__ == "__main__":
    # Example simulation
    team1_names = ["A", "C"]
    team2_names = ["B", "D"]
    game = Game(team1_names, team2_names)
    game.simulate(runs=100000)
