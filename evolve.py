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
            with open(os.path.join(POPFOLDER, "%i" % (i * n + j)), "w") as f:
                f.write('\n'.join([l] * 40))

def write_deck(path, deck):
    with open(path, 'w') as f:
        f.write('\n'.join(map(lambda x: "1 " + x, deck)))

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

    def __repr__(self):
        return "%s: %i/%i" % (self.path, self.wins, self.losses)

def duel(deck1, deck2):
    write_deck("first.dec", deck1.deck)
    write_deck("second.dec", deck2.deck)
    try:
        output = subprocess.check_output(["sh", "duel.sh", "first.dec", "second.dec"])
    except subprocess.CalledProcessError:
        a.losses += 1
        b.losses += 1
        return None

    awins, bwins = output.decode('utf-8').split('\n')[-2].split('\t')[-2:]

    if int(awins) > int(bwins):
        a.wins += 1
        b.losses += 1
        return a
    else:
        a.losses += 1
        b.wins += 1
        return b

def winrate(spot):
    return spot.wins / (spot.wins + spot.losses)

def crossover(a, b):
    c, d = zip(*((y, x) if random.random() < 0.5 else (x, y) for x, y in zip(a, b)))
    return list(c), list(d)

def mutate(deck):
    deck[random.randint(0, len(deck)-1)] = random.choice(cards)

if __name__ == '__main__':

    spots = list(map(lambda x: Spot(os.path.join(POPFOLDER, x)), os.listdir(POPFOLDER)))

    cards = cardlist('M10')

    while True:
        a, b, c, d = random.sample(spots, 4)
        winner1 = duel(a, b)

        # Don't want to breed decks that crash the AI
        # This happens when decks contain unimplemented cards mostly
        if winner1 is None:
            winner1 = c
            winner2 = d
        else:
            winner2 = duel(c, d)
            if winner2 is None:
                winner2 = winner1

        for child in crossover(winner1.deck, winner2.deck):
            mutate(child)
            min(spots, key=winrate).change_deck(child)

        for spot in spots:
            print(spot)
