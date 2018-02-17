# poker
Determine winning poker hands

## Dependencies
Only required for testing, project should run on Python >=3.5

Install pipenv and install the projects dependencies:
```
pip install pipenv
pipenv install --dev
```

## Usage
```
# Compare poker hands
./run.py AAAA3 AAQQQ

# View command help
./run.py --help
```

## Running Tests
```
py.test --pylint
```

## Implementation
The entered hands are validated and then parsed for their rank and type. These
are then compared to determine the winning hand which is subsequently printed.

## Design Decisions
### Single Wildcard
The problem implied only a single wildcard could be used in a hand at a time.
A validation check was put into place to ensure only single wildcards are
accepted. To enable multiple wildcards some rethinking of the algorithm
would be necessary to ensure a straight vs an of a kind hand is selected.

### Cross Hand Validation
For simplicity validation is only performed on a single hand at a time. This
means that two hands could have more aces than are available in a conventional
card deck. The primary motivation for this was the complication that wildcards
introduce into hand validation. Do wildcards allow two hands to have more aces
than are available in the deck? If so then why not make five of a kind hands
possible?

## Alternative Approaches
### PokerHandFactory
The current Hand class implementation could be changed to a namedtuple
containing just a hand_type and rank. This would the be produced from a
PokerHandFactory class or method that analyzes the card string. This would
be a more object-oriented approach but I felt it wasn't very pythonic and
that it was a bit overkill for the task at hand.

### Hand Lookup Table
Current implementation of determining rank and type of hand feels a bit
clumsy. An alternative would be to list all possible hands in a lookup table
which is then traversed to determine the value of an entered hand. This would
make exact matching trivial and wild card handling much simpler (by just
checking for subsets). Complication in this method is the upfront cost of
generating all possible hands and storing them.
