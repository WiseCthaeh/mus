import random
from collections import Counter
import matplotlib.pyplot as plt

# card values
val = {'A': 1, '4': 4, '5': 5, '6': 6, '7': 7, 'S': 10, 'C': 10, 'R': 10}
fr_pares = {'Nada': 0, 'Par': 0, 'Medias': 0, 'Duples': 0}
fr_juego = {i: 0 for i in range(31, 41)}

# Game runs for simulation
runs = 100000
total_juego = 0


class Game:
    def __init__(self, team1_names, team2_names):
        self.teams = {"team1": [Player(name, "team1") for name in team1_names],
                      "team2": [Player(name, "team2") for name in team2_names]}
        self.players = [self.teams["team1"][0], self.teams["team2"][0], self.teams["team1"][1], self.teams["team2"][1]]
        self.deck = Deck(full=True)
        self.team_scores = {"team1": 0, "team2": 0}
        self.mano_index = 0
        self.round = 1
        self.pares_stats = Counter()
        self.juego_stats = Counter()
        self.total_juego_rounds = 0

    def deal_players(self):
        for player in self.players:
            self.deal(player, n=4)
            player.sort_hand()
            player.check_pares()
            player.check_juego()

    def compute_game_statistics(self):
        for player in self.players:
            pares_type = self.get_pares_type(player)
            self.pares_stats[pares_type] += 1

            if player.juego >= 31:
                self.juego_stats[player.juego] += 1
                self.total_juego_rounds += 1

    def get_pares_type(self, player):
        """Determine the pares type for a player."""
        pares_counter = Counter(player.show_hand())
        pairs = 0
        for count in pares_counter.values():
            if count == 2:
                pairs += 2
            elif count == 3:
                pairs += 3
            elif count == 4:
                pairs += 4

        if pairs == 0:
            return 'Nada'
        elif pairs == 2:
            return 'Par'
        elif pairs == 3:
            return 'Medias'
        else:
            return 'Duples'

    def play_round(self):
        self.deck.shuffle()
        self.deal_players()
        self.compute_game_statistics()
        self.clear_round()
        self.rotate_mano()

    def play_game(self, max_points=40):
        while self.team_scores['team1'] < max_points and self.team_scores['team2'] < max_points:
            self.play_round()
        print("Game Over")

    def visualize_statistics(self):
        """Generate visualizations for collected statistics."""
        fr_pares = {key: 100 * value / sum(self.pares_stats.values()) for key, value in self.pares_stats.items()}
        fr_juego = {key: 100 * value / self.total_juego_rounds for key, value in self.juego_stats.items()}

        # Plotting "juego"
        plt.figure(1)
        plt.bar(fr_juego.keys(), fr_juego.values(), color='g')
        plt.xlabel('Juego')
        plt.ylabel('Frequency (%)')
        plt.title('Juego')

        # Plotting "pares"
        plt.figure(2)
        plt.bar(fr_pares.keys(), fr_pares.values(), color='b')
        plt.xlabel('Tipo de pares')
        plt.ylabel('Frequency (%)')
        plt.title('Pares')

        plt.show()

        print('Probability of having "juego":', sum(self.juego_stats.values()) / (4 * len(self.pares_stats)))

    def clear_round(self):
        for player in self.players:
            player.hand = []
            player.is_mano = False
            player.has_pares = False
            player.has_juego = False
            player.pares = ''
            player.pares_strength = 0
            player.juego = 0
        self.deck = Deck(full=True)


# Supporting classes (Player, Card, Deck) remain unchanged
class Player:
    def __init__(self, name, team):
        self.name = name
        self.team = team
        self.hand = []
        self.is_mano = False
        self.sort_hand_values = val
        self.juego_values = val
        self.has_pares = False
        self.has_juego = False
        self.pares = ''
        self.pares_strength = 0
        self.juego = 0

    def show_hand(self):
        return ''.join(card.rank for card in self.hand)

    def draw(self, card):
        self.hand.append(card)

    def sort_hand(self):
        self.hand.sort(key=lambda card: self.sort_hand_values[card.rank])

    def check_pares(self):
        self.pares = ''
        self.pares_strength = 0
        for card in self.show_hand():
            if self.show_hand().count(card) >= 2:
                self.has_pares = True
                self.pares += card

    def check_juego(self):
        self.juego = sum(self.juego_values[card.rank] for card in self.hand)
        self.has_juego = self.juego >= 31


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


# Example usage:
team1_names = ['Player1', 'Player2']
team2_names = ['Player3', 'Player4']
game = Game(team1_names, team2_names)
game.play_game(max_points=40)
game.visualize_statistics()
