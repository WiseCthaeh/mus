import random
# import numpy as np

PARES = ["AA","44","55","66","77","SS","CC","RR"]
MEDIAS =["AAA","444","555","666","777","SSS","CCC","RRR"]

DUPLES = {str(i+j): k for k, (i, j) in enumerate((x, y) for x in PARES for y in PARES if PARES.index(x) <= PARES.index(y))}
# print(DUPLES.keys())


PARES = [*PARES, *MEDIAS,*DUPLES.keys()]
PARES_DICT = {par: count+1 for count, par in enumerate(PARES)}
# print(PARES)
JUEGO_PUNTOS = {31:3, 32:2, 33:2, 34:2, 35:2, 36:2, 37:2, 40:2}
PARES_PUNTOS = [0]
for key in PARES_DICT.keys():
    if len(key)==2:
        PARES_PUNTOS.append(1)
    if len(key)==3:
        PARES_PUNTOS.append(2)
    if len(key)==4:
        PARES_PUNTOS.append(3)


class Player():
    def __init__(self, name, team):
        self.name = name
        self.team = team #team is a binary value
        self.hand = []
        self.is_mano = False
        self.sort_hand_values =  {"A": 1, "4": 4, "5": 5, "6": 6, "7": 7, "S": 10, "C": 11, "R": 12}
        self.juego_values =  {"A": 1, "4": 4, "5": 5, "6": 6, "7": 7, "S": 10, "C": 10, "R": 10}
        self.has_pares = False
        self.has_juego = False
        self.pares = ''
        self.pares_strength = 0
        self.juego = 0

    def show_hand(self):
        _ = [card.rank for card in self.hand]
        return ''.join(_)
    
    def draw(self, card):
        self.hand.append(card)
    
    def sort_hand(self):
        # Sort the hand based on the value in `sort_hand_values`
        self.hand.sort(key=lambda card: self.sort_hand_values[card.rank])
    
    def check_pares(self):
        for card in self.show_hand():
            if self.show_hand().count(card) >= 2:
                self.has_pares = True
                self.pares += card
        if self.pares != '':
            self.pares_strength = PARES_DICT[self.pares]

    def check_juego(self):
        if sum(self.juego_values[card.rank] for card in self.hand)>=31:
            self.has_juego = True
        else:
            self.has_juego = False
        self.juego = sum(self.juego_values[card.rank] for card in self.hand)

class Card():
    def __init__(self, rank) -> None:
        self.rank = rank

class Deck(list):
    def __init__(self,full=True):
        ranks = ["A", "A", "4", "5", "6", "7", "S", "C", "R", "R"] 
        if full:
            [[self.append(Card(rank)) for rank in ranks] for _ in range(4)]
    
    def shuffle(self):
        random.shuffle(self)
    

class Game():
    def __init__(self, team1_names, team2_names):
        self.teams = {"team1": [Player(name, "team1") for name in team1_names],
                      "team2": [Player(name, "team2") for name in team2_names]}
        self.players =[self.teams["team1"][0], self.teams["team2"][0], self.teams["team1"][1], self.teams["team2"][1]]
        # self.players goes in clockwise order
        self.deck = Deck(full=True)
        self.team_scores = {"team1":0, "team2":0}
        self.mano_index = 0

    def deal(self, player,n=1):
        for _ in range(n):
            player.draw(self.deck.pop())

    def deal_players(self):
        for player in self.players:
            self.deal(player,n=4)
            player.sort_hand()
            player.check_pares()
            player.check_juego()

    def betting_round(self, stage):
        print(f"\n--- Betting Round: {stage} ---")
        bet_made = False
        winning_team = None
        current_bet = 0
        pot = 0
        if stage=='pares':
            pass
        if stage=='juego':
            pass

        # Start with the player who is Mano and proceed clockwise
        current_player_index = self.mano_index
        for i, player in enumerate(self.players):

            if i==3:
                if bet_made == False:

                    "If no bets are 3placed by the last player, the round is left al paso"
                    raise NotImplementedError
    
    def offer_mus(self):
        raise NotImplementedError
    
    def play_round(self):
        self.deck.shuffle()
        self.deal_players()
        # self.offer_mus()
        # for player in self.players:
        #     print(player.show_hand())

        stages = ['grande', 'chica', 'pares', 'juego']
        stage_data =[]
        for stage in stages:
            bet_made, winning_team, current_bet = self.betting_round(stage)
            if winning_team == None:
            # These two lines deal with either an accepted bet or a stage that is not bet on,
            # Both scenarios
                if bet_made != 0:
                    print('Compute which team wins the bet')
                    pass
                else:
                    print('Compute which team wins (was left al paso)')
                    pass
            else:
                # Here a team has won the round, compute points and add to team scores
                pass
                #

    def play_game(self):
        self.play_round()

team1_names = ["A", "C"]
team2_names = ["B", "D"]
game = Game(team1_names, team2_names)
# game.play_game()
for player in game.players:
    print(player.name, player.show_hand(), player.has_pares, player.pares,player.has_juego, player.juego)
