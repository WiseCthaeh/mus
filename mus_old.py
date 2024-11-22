import random
from collections import Counter
import matplotlib.pyplot as plt

# card values
val = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, 'S':10, 'C':10, 'R':10}
# dictionary to store frequency of card values
fr_pares = {'Nada':0, 'Par':0, 'Medias': 0, 'Duples':0}
fr_juego = {i:0 for i in range(31, 41)}

runs = 100000
total_juego = 0


# function to calculate pares
def pares(cards):
    card_counts = Counter(cards)

    pair_count = 0
    for count in card_counts.values():
        if count == 2:
            pair_count += 2
        elif count == 3:
            pair_count += 3
        elif count == 4:
            pair_count += 4

    if pair_count == 0:
        return 'Nada'
    elif pair_count == 2:
        return 'Par'
    elif pair_count == 3:
        return 'Medias'
    else:
        return 'Duples'

# function to calculate juego
def juego(cards):
    return sum(val[i] for i in cards)

# loop to run the simulation
for _ in range(runs):
    deck = ['A', 'A', '4', '5', '6', '7', 'S', 'C', 'R', 'R'] * 4
    deck = ['A', '2', '3', '4', '5', '6', '7', 'S', 'C', 'R'] * 4
    random.shuffle(deck)
    # draw 4 cards for each player
    p1, p2, p3, p4 = deck[:4], deck[4:8], deck[8:12], deck[12:16]
    ps1 = pares(p1)
    t1 = juego(p1)
    fr_pares[ps1] += 100 / runs
    if t1 > 30:
        fr_juego[t1] += 1
        total_juego += 1

# update the dictionary
fr_juego = {key: 100 * value / total_juego for key, value in fr_juego.items()}

# plot the frequency of card values
plt.figure(1)
plt.bar(fr_juego.keys(),fr_juego.values(), color = 'g')
plt.xlabel('Juego')
plt.ylabel('Frecuencia (%)')
plt.title('Juego')

plt.figure(2)
plt.bar(fr_pares.keys(), fr_pares.values(), color = 'b')
plt.xlabel('Tipo de pares')
plt.ylabel('Frecuencia (%)')
plt.title('Pares')
plt.show()

print('Probabilidad de juego: ', total_juego / runs)

