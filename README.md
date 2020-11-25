# Genetic Algorithm making MTG decks

Breeds decks to find the deck with the highest winrate when played by the Magarena AI.

## Usage
### Prepare magarena

``` shell
git clone https://github.com/magarena/magarena.git
cd magarena
make
```

### Start evolving
``` shell
python reset_population.py
python evolve.py
```
