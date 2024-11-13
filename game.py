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

    def player_promt(self, bet_made, betting_team, current_bet):
        # This should return action, current_bet
        options = ['pass', 'bet', 'fold', 'call']
        if bet_made==False:
            options.remove('fold')
            options.remove('call')

        if current_bet != 0 or bet_made:
            options.remove('pass')

        action = input(f"{self.name} {self.show_hand()} choice of options = {options}| bet: {bet_made} current bet: {current_bet} ")
        if action =='pass':
            return action, current_bet
        if action == 'call':
            return action, current_bet
        if action == 'bet':
            current_bet = input(f"Place a bet")
            return action, current_bet
        if action == 'fold':
            return action, current_bet

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
        betting_team = None
        betting_settled = False
        current_bet = 0
        pot = 0
        active_players = self.players

        if stage=='pares':
            active_players = [player for player in self.players if player.has_pares]
            for player in active_players:
                print(player.name, player.has_pares)
            if len(active_players)>=2:
                if all(player.team=='team1' for player in active_players):
                    # This is the case for only one team having pairs
                    return bet_made, 'team1', 0
                if all(player.team=='team2' for player in active_players):
                    # This is the case for only one team having pairs
                    return bet_made, 'team2', 0
            else:
                print('No pairs or sufficient players for betting allowed')
                return bet_made, betting_team, current_bet

        if stage=='juego':
            active_players = [player for player in self.players if player.has_juego]
            for player in active_players:
                print(player.name, player.has_juego)
            if len(active_players)>=2:
                if all(player.team=='team1' for player in active_players):
                    return bet_made, 'team1', 0
                if all(player.team=='team2' for player in active_players):
                    return bet_made, 'team2', 0
            if len(active_players)==1:
                return bet_made, active_players[0].team, current_bet
            else:
                active_players = self.players
                print('No one has juego, proceed to bet towards punto')

        for i, player in enumerate(active_players):
            action, bet_amount = player.player_promt(bet_made, betting_team, current_bet)
            if action == 'pass':
                if i==len(active_players)-1:
                    print("If no bets are placed by the last player, the round is left al paso")
                    return bet_made, betting_team, current_bet
                else:
                    continue
            if action =='bet':
                current_bet = bet_amount
                betting_team = player.team
                pot += int(bet_amount)
                bet_made = True
                betting_settled = False
                
        
            if bet_made:
                while betting_settled==False:
                    respond_players = [player for player in active_players if player.team!=betting_team]
                    for j, player in enumerate(respond_players):
                        action, bet_amount = player.player_promt(bet_made, betting_team, pot)
                        if action=='fold':
                            # print('player chose fold')
                            if j ==len(respond_players)-1:
                                # print('final fold')
                                if pot==2:
                                    return bet_made, betting_team, 1
                                    # This is when envido is not seen, opposit team wins 1
                                else: 
                                    return bet_made, betting_team, pot - current_bet
                            else:
                                # This continue is so that the other team player can go
                                continue
                        if action=='call':
                            betting_settled=True
                            return bet_made, None, current_bet
                        if action=='bet':
                            current_bet = int(bet_amount)
                            pot += current_bet
                            betting_team = player.team
                            break



 
    def evalute_winner(self, stage, bet_made, winning_team, current_bet):
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

    def offer_mus(self):
        raise NotImplementedError
    
    def play_round(self):
        self.deck.shuffle()
        self.deal_players()
        for player in game.players:
            print(player.name, player.show_hand(), player.has_pares, player.pares,player.has_juego, player.juego)

        stages = ['grande', 'chica', 'pares', 'juego']
        stage_data =[]
        for stage in stages:
            bet_made, winning_team, current_bet = self.betting_round(stage)
            print(stage, bet_made, winning_team, current_bet)
            # self.evalute_winner(bet_made, winning_team, current_bet)


    def play_game(self):
        self.play_round()

team1_names = ["A", "C"]
team2_names = ["B", "D"]
game = Game(team1_names, team2_names)
game.play_game()
