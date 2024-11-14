import random
# import numpy as np

PARES = ["AA","44","55","66","77","SS","CC","RR"]
MEDIAS =["AAA","444","555","666","777","SSS","CCC","RRR"]
GAME_MAX_POINTS = 40
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
    
    def discard(self, index):
        return(self.hand.pop(index))
    
    def sort_hand(self):
        # Sort the hand based on the value in `sort_hand_values`
        self.hand.sort(key=lambda card: self.sort_hand_values[card.rank])
    
    def check_pares(self):
        self.pares = ''
        self.pares_strength = 0
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
        self.round = 1

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
        active_players = self.players[self.mano_index:] + self.players[:self.mano_index]


        if stage=='pares':
            active_players = [player for player in active_players if player.has_pares]
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
            active_players = [player for player in active_players if player.has_juego]
            for player in active_players:
                print(player.name, player.has_juego)
            if len(active_players)>=2:
                if all(player.team=='team1' for player in active_players):
                    return bet_made, 'team1', 0
                if all(player.team=='team2' for player in active_players):
                    return bet_made, 'team2', 0
            if len(active_players)==1:
                return bet_made, active_players[0].team, current_bet
            if len(active_players)==0:
                active_players = self.players[self.mano_index:] + self.players[:self.mano_index]
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
                current_bet = int(bet_amount)
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
                                if pot==current_bet:
                                    return bet_made, betting_team, 1
                                    # This is when envido is not seen, opposit team wins 1
                                else: 
                                    return bet_made, betting_team, pot - int(current_bet)
                            else:
                                # This continue is so that the other team player can go
                                continue
                        if action=='call':
                            betting_settled=True
                            return bet_made, None, pot 
                        if action=='bet':
                            current_bet = int(bet_amount)
                            pot += current_bet
                            betting_team = player.team
                            break

    def offer_mus(self):
        mus_order_players = [self.players[(0+self.mano_index)%4], 
                             self.players[(2+self.mano_index)%4], 
                             self.players[(1+self.mano_index)%4], 
                             self.players[(3+self.mano_index)%4]]
        
        all_agree = all(input(f"{player.name}, do you want Mus? {player.show_hand()} (yes/no): ").strip().lower() == "yes"
                for player in mus_order_players)
        
        while all_agree:
            discard_pile = Deck(full=False)
            player_discards = []
            discard_amount = 0
            for player in self.players[self.mano_index:] + self.players[:self.mano_index]:
                print(f"{player.name}'s hand: {player.show_hand()}")
                discard_input = input(f"{player.name}, enter card positions to discard (1-4)").split(',')
                if len(discard_input)>1:
                    discard_amount += len(discard_input)
                    player_discards.append(sorted(discard_input,reverse=True))
                else:
                    discard_amount += 1
                    player_discards.append(discard_input)
            if discard_amount>len(self.deck):
                self.deck = discard_pile
                print("There are not enough cards to give out, shuffling discard")
                self.deck.shuffle()
            for i, player in enumerate(self.players[self.mano_index:] + self.players[:self.mano_index]):
                for dis in player_discards[i]:
                    discard_pile.append(player.discard(int(dis)-1))
                    # print(player.name,player.show_hand()[dis])
                self.deal(player,len(player_discards[i]))
                player.sort_hand()
                player.check_pares()
                player.check_juego()
            self.game_info()
            all_agree = all(input(f"{player.name}, do you want another Mus? {player.show_hand()} (yes/no): ").strip().lower() == "yes"
                            for player in mus_order_players)
    
    def game_info(self):
        print("********** SCORES **********")
        print(f"Team 1: {self.team_scores['team1']} | Team 2: {self.team_scores['team2']} | Round: {self.round}")
        for player in self.players:
            print(player.name, player.show_hand(), player.has_pares, player.pares,player.has_juego, player.juego)

    def rotate_mano(self):
        self.mano_index = (self.mano_index + 1)%4
        self.round += 1

    def play_round(self):
        self.deck.shuffle()
        self.deal_players()
        self.game_info()
        # This is where self.offermus() goes
        self.offer_mus()

        stages = ['grande', 'chica', 'pares', 'juego']
        stages_log = []
        for stage in stages:
            stage_data = []
            bet_made, winning_team, current_bet = self.betting_round(stage)
            if winning_team is None:
                if bet_made is False:
                    winning_team = self.find_winner(stage)
                    current_bet = 1
                else:
                    winning_team = self.find_winner(stage)
                self.compute_points(stage, winning_team, current_bet)
            else:
                self.compute_points(stage, winning_team,current_bet)

        self.clear_round()
        self.rotate_mano()

    def find_winner(self, stage):
        if stage=='grande':
            best_player = None
            best_hand_ranks = []

            # Get number of players to handle wrapping around from "mano"
            num_players = len(self.players)

            # Start from "mano" and go through players in turn order
            for i in range(num_players):
                player = self.players[(self.mano_index + i) % num_players]  # Starting from "mano" and wrap around

                # Get the sorted hand ranks for the player in descending order
                player_hand_ranks = sorted(
                    [player.sort_hand_values[card.rank] for card in player.hand],
                    reverse=True
                )

                # Compare this player's hand with the current best hand
                if player_hand_ranks > best_hand_ranks:
                    best_hand_ranks = player_hand_ranks
                    best_player = player
                elif player_hand_ranks == best_hand_ranks:
                    # If there's a tie, choose the player closest to "mano"
                    current_best_distance = (self.players.index(best_player) - self.mano_index) % num_players
                    current_player_distance = i
                    if current_player_distance < current_best_distance:
                        best_player = player

            # Return the team of the player with the best hand
            if best_player:
                print(f"The best hand for 'grande' belongs to {best_player.name} from team {best_player.team}")
                winning_team = best_player.team
            else:
                print("No player with the best hand found")
                return None
        
        if stage=='chica':
            best_player = None
            best_hand_ranks = [float('inf')] * 4  # Initialize to a high value for "lowest" comparison
            
            # Get number of players to handle wrapping around from "mano"
            num_players = len(self.players)

            # Start from "mano" and go through players in turn order
            for i in range(num_players):
                player = self.players[(self.mano_index + i) % 4]  # Start from "mano" and wrap around

                # Get the sorted hand ranks for the player in ascending order
                player_hand_ranks = sorted(
                    [player.sort_hand_values[card.rank] for card in player.hand]
                )

                # Compare this player's hand with the current best hand for "chica"
                if player_hand_ranks < best_hand_ranks:
                    best_hand_ranks = player_hand_ranks
                    best_player = player
                elif player_hand_ranks == best_hand_ranks:
                    # If there's a tie, choose the player closest to "mano"
                    current_best_distance = (self.players.index(best_player) - self.mano_index) % num_players
                    current_player_distance = i
                    if current_player_distance < current_best_distance:
                        best_player = player

            # Return the team of the player with the best "chica" hand
            if best_player:
                print(f"The best hand for 'chica' belongs to {best_player.name} from team {best_player.team}")
                winning_team = best_player.team
            else:
                print("No player with the best hand found")
                return None

        if stage=='pares':
            active_players = [player for player in self.players if player.has_pares]
            if len(active_players)==1:
                    winning_team = active_players[0].team
            else:
                best_player = None
                best_pares_strength = -1  # Initialize to a low value

                # Start from "mano" and go through players in turn order
                for i in range(4):
                    player = self.players[(self.mano_index + i) % 4]  # Starting from "mano" and wrap around

                    # Compare player's pares_strength with the best so far
                    if player.pares_strength > best_pares_strength:
                        best_pares_strength = player.pares_strength
                        best_player = player
                    elif player.pares_strength == best_pares_strength:
                        # Tie-breaking: player closest to "mano" wins
                        current_best_distance = (self.players.index(best_player) - self.mano_index) % 4
                        current_player_distance = i
                        if current_player_distance < current_best_distance:
                            best_player = player

                # Return the team of the player with the highest pares_strength
                if best_player:
                    print(f"The best 'pares' hand belongs to {best_player.name} from team {best_player.team} with pares strength {best_pares_strength}")
                    winning_team = best_player.team
                else:
                    print("No player with the best pares strength found")
                    return None

        if stage=='juego':
            # This is for computing who is closest to 30 for punto
            if all(player.has_juego==False for player in self.players):
                best_player = None
                best_total_below_31 = -1  # Initialize to a low value
                num_players = len(self.players)

                # Loop through players starting from "mano" position
                for i in range(num_players):
                    player = self.players[(self.mano_index + i) % num_players]  # Wrap around from "mano"

                    # Calculate the total hand value
                    hand_total = player.juego

                    # Only consider hands below 31, since no one has "juego"
                    if hand_total < 31:
                        # Compare the hand total with the current best below 31
                        if hand_total > best_total_below_31:
                            best_total_below_31 = hand_total
                            best_player = player
                        elif hand_total == best_total_below_31:
                            # Tie-breaking: player closest to "mano" wins
                            current_best_distance = (self.players.index(best_player) - self.mano) % num_players
                            current_player_distance = i
                            if current_player_distance < current_best_distance:
                                best_player = player

                # Return the team of the player with the best "punto" hand (highest hand below 31)
                if best_player:
                    print(f"The best 'punto' hand belongs to {best_player.name} from team {best_player.team} with hand total {best_total_below_31}")
                    return best_player.team
                else:
                    print("No player with a valid 'punto' hand found")
                    return None
            
            # This is for computing who is the strongest juego
            else:
                juego_priority = [JUEGO_PUNTOS.keys()]
                best_player = None
                best_juego_value = -1  # Initialize to a low value
                best_juego_priority = float('inf')  # Initialize to a high priority (31 is best)

                num_players = len(self.players)

                # Loop through players starting from "mano" position
                for i in range(num_players):
                    player = self.players[(self.mano_index + i) % num_players]  # Wrap around from "mano"

                    # Calculate the total hand value
                    hand_total = player.juego

                    # Only consider hands of 31 or more
                    if hand_total >= 31 and hand_total in juego_priority:
                        # Determine the priority of this "juego" value
                        current_priority = juego_priority.index(hand_total)

                        # Compare with the current best priority
                        if current_priority < best_juego_priority:
                            best_juego_priority = current_priority
                            best_juego_value = hand_total
                            best_player = player
                        elif current_priority == best_juego_priority:
                            # Tie-breaking: player closest to "mano" wins
                            current_best_distance = (self.players.index(best_player) - self.mano_index) % num_players
                            current_player_distance = i
                            if current_player_distance < current_best_distance:
                                best_player = player

                # Return the team of the player with the best "juego" hand
                if best_player:
                    print(f"The best 'juego' hand belongs to {best_player.name} from team {best_player.team} with a total of {best_juego_value}")
                    winning_team = best_player.team

        return winning_team
    
    def compute_points(self, stage, winning_team, current_bet):
        if stage=='grande' or stage=='chica':
            self.team_scores[winning_team] += current_bet

        if stage=='pares':
            for player in self.players:
                if player.team==winning_team and player.has_pares:
                    self.team_scores[winning_team] += PARES_PUNTOS[PARES_DICT[player.pares]]
            if len([player for player in self.players if player.has_pares==False])==4:
                current_bet = 0
            self.team_scores[winning_team] += current_bet

        if stage=='juego':
            for player in self.players:
                if player.team==winning_team and player.has_juego:
                    self.team_scores[winning_team] += JUEGO_PUNTOS[player.juego]
            if len([player for player in self.players if player.has_juego==False])==4:
                current_bet +=1
            self.team_scores[winning_team] += current_bet

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

    def play_game(self):
        while self.team_scores['team1']<GAME_MAX_POINTS and self.team_scores['team2']<GAME_MAX_POINTS:
            self.play_round()

