from collections import Counter, OrderedDict
from enum import Enum
from itertools import islice

HAND_SIZE = 5
MAX_NUMBER_OF_SAME_CARD = 4

LOW_STRAIGHT_HIGH_CARD = '5'  # Highest card in a low straight
CARD_RANK = [*(str(i) for i in range(2, 10)), 't', 'j', 'q', 'k', 'a']
LOW_ACE_RANK = -1
WILD_CARD = '*'
VALID_CARDS = {WILD_CARD, *CARD_RANK}


class InvalidHand(Exception):
    pass


class HandType(Enum):
    """ Possible hand types. The instance value indicates type rank. """
    HIGHCARD = 0
    PAIR = 1
    TWOPAIR = 2
    THREEOFAKIND = 3
    STRAIGHT = 4
    FULLHOUSE = 5
    FOUROFAKIND = 6


class Hand:
    """
    Represent a hand in a game of poker. Provides properties for the hand's
    `hand_type` and `rank`. The `hand_type` is the poker hand type (instance of
    HandType) and the `rank` is the hands rank within the `hand_type` (a list
    of cards from high to low).
    """

    _CARD_TYPE_MAP = {
        (4, 1): HandType.FOUROFAKIND,
        (3, 2): HandType.FULLHOUSE,
        (3, 1, 1): HandType.THREEOFAKIND,
        (2, 2, 1): HandType.TWOPAIR,
        (2, 1, 1, 1): HandType.PAIR,
        (1, 1, 1, 1, 1): HandType.HIGHCARD,
    }

    def __init__(self, cards):
        if len(cards) != HAND_SIZE:
            raise InvalidHand('Incorrect number of cards in hand. Expected: 5, Hand: {}'.format(cards))

        card_counts = Counter(cards)
        if not VALID_CARDS.issuperset(card_counts.keys()):
            raise InvalidHand('Invalid card(s) in hand: {}'.format(card_counts.keys() - VALID_CARDS))

        most_common_card, count = card_counts.most_common(n=1)[0]
        if count > MAX_NUMBER_OF_SAME_CARD:
            raise InvalidHand('Invalid number of {}s. Expected: {}'.format(most_common_card, MAX_NUMBER_OF_SAME_CARD))

        if card_counts.get(WILD_CARD, 0) > 1:
            raise InvalidHand('Expected a max of one wild card. Received: {}'.format(card_counts[WILD_CARD]))

        self.hand_type, self.rank = self._calc_hand_type_and_rank(cards)

    @classmethod
    def _calc_hand_type_and_rank(cls, cards):
        hand_type, rank = cls._find_straight_type(cards)
        if hand_type:
            return hand_type, rank

        return cls._find_non_straight_card_types(cards)

    @classmethod
    def _find_straight_type(cls, cards):
        """ Check if cards contain a straight """
        card_set = set(card for card in cards)
        if len(card_set) < HAND_SIZE:
            # More than one of a single card type, a straight is not possible
            return None, None

        card_set.discard(WILD_CARD)
        for straight in window(reversed(('a', *CARD_RANK)), n=HAND_SIZE):
            if card_set.issubset(straight):
                return HandType.STRAIGHT, [straight[0]]

        return None, None

    @staticmethod
    def _has_low_straight_card(card_indexes):
        """ Check if card_indexes contain any low straight cards (besides aces) """
        return any(card_index in card_indexes
                   for card_index in range(CARD_RANK.index(LOW_STRAIGHT_HIGH_CARD)))

    @classmethod
    def _find_non_straight_card_types(cls, cards):
        """ Check for all card types besides a straight """

        sorted_cards, wild_card_count = cls._sort_cards(cards)
        sorted_cards = list(cls._backfill_wildcards(sorted_cards, wild_card_count))

        rank, card_type_key = zip(*sorted_cards)
        hand_type = cls._CARD_TYPE_MAP.get(card_type_key)

        if not hand_type:
            # This should not happen with a valid hand
            raise RuntimeError('Could not find hand type and rank!', card_type_key, rank)

        return hand_type, list(rank)

    @classmethod
    def _sort_cards(cls, cards):
        """
        Count and sort cards into a list of tuples from high to low ranking.
        Returns a tuple for the sorted cards and the wild card
        count: ([('a', 3), ('q', 1), ('2', 1)], 0)
        """
        card_counts = Counter(cards)
        wild_card_count = card_counts.pop(WILD_CARD, 0)
        # For cards with the same count we need to sort by card value
        sorted_cards = sorted(card_counts.items(),
                              key=lambda item: (item[1], CARD_RANK.index(item[0])),
                              reverse=True)
        return sorted_cards, wild_card_count

    @classmethod
    def _backfill_wildcards(cls, sorted_cards, wild_card_count):
        """
        Backfill of a kind hand with wild cards. This will increase the card
        counts to give the hand the highest possible rank and type.
        """
        used_cards = []

        # Fill existing card counts
        for card, count in sorted_cards:
            extra_count = min(wild_card_count, MAX_NUMBER_OF_SAME_CARD - count)
            yield card, count + extra_count
            used_cards.append(card)
            wild_card_count -= extra_count

        # Add extra cards with the highest value
        while wild_card_count > 0:
            card = next(card for card in reversed(CARD_RANK) if card not in used_cards)
            count = min(wild_card_count, MAX_NUMBER_OF_SAME_CARD)
            yield card, count
            used_cards.append(card)
            wild_card_count -= count


def compare_hands(hand_a, hand_b):
    """ Compare two Hands """
    return '01'


def window(seq, n=2):
    """
    Sliding window implementation, sourced from https://stackoverflow.com/a/6822773
    """
    it = iter(seq)
    result = tuple(islice(it, n))
    if len(result) == n:
        yield result
    for elem in it:
        result = result[1:] + (elem,)
        yield result
