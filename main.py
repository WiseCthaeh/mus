from game import Game


def main():
    team1_names = ["A", "C"]
    team2_names = ["B", "D"]
    g = Game(team1_names, team2_names)
    g.play_game()


if __name__ == '__main__':
    main()
    