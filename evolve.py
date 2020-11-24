import itertools, subprocess, os, os.path, random

def load_set(code):
    with open("magarena/resources/magic/data/sets/%s.txt" % code, "r") as f:
        return f.read().strip().split('\n')

basic_lands = ['Island', 'Forest', 'Swamp', 'Plains', 'Mountain']
def cardlist(*sets):
    return list(itertools.chain(basic_lands, *map(load_set, sets)))

POPFOLDER = "decks"
def make_population():
    os.makedirs(POPFOLDER, exist_ok=True)
    for i, l in enumerate(basic_lands):
        n = 2
        for j in range(n):
            save_deck(os.path.join(POPFOLDER, "%i.dec" % (i * n + j)), [l] * 40)

def write_deck(path, deck):
    with open(path, 'w') as f:
        f.write('\n'.join(map(lambda x: "1 " + x, deck)))

def duel_decks(deck1, deck2):
    write_deck("first.dec", deck1)
    write_deck("second.dec", deck2)
    awins, bwins = subprocess.check_output(["sh", "duel.sh", "first.dec", "second.dec"]).decode('utf-8').split('\n')[-2].split('\t')[-2:]

    return int(awins) > int(bwins)

class Spot:
    def __init__(self, path):
        self.path = path
        with open(self.path, 'r') as f:
            self.deck = list(f.read().split('\n'))
        self._reset()

    def _reset(self):
        # Decks always have one win initially so that they aren't immediately killed.
        self.wins = 1
        self.losses = 0

    def change_deck(self, deck):
        with open(self.path, 'w') as f:
            f.write('\n'.join(deck))
        self.deck = deck
        self._reset()

def duel(a, b):
    if duel_decks(a.deck, b.deck):
        a.wins += 1
        b.losses += 1
        return a
    else:
        a.losses += 1
        b.wins += 1
        return b

def winrate(spot):
    return spot.wins / (spot.wins + spot.losses)

spots = list(map(lambda x: Spot(os.path.join(POPFOLDER, x)), os.listdir(POPFOLDER)))

cards = cardlist('M19')

def crossover(a, b):
    c, d = zip(*((y, x) if random.random() < 0.5 else (x, y) for x, y in zip(a, b)))
    return list(c), list(d)

def mutate(deck):
    deck[random.randint(0, len(deck))] = random.choice(cards)

if __name__ == '__main__':
    while True:
        a, b, c, d = random.sample(spots, 4)
        winner1 = duel(a, b)
        winner2 = duel(c, d)

        for child in crossover(winner1, winner2):
            mutate(child)
            min(spots, key=winrate).change_deck(child)
