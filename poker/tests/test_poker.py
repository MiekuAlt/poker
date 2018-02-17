import pytest

from poker.poker import Hand, InvalidHand, HandType, compare_hands


@pytest.mark.parametrize('hand', ['', 'aaaa', 'aaaaaa', 'aaaaf', 'aaaa1'])
def test_raises_on_invalid_hand(hand):
    with pytest.raises(InvalidHand):
        Hand(hand)


@pytest.mark.parametrize(('hand', 'expected'), [
    ('2q222', HandType.FOUROFAKIND),
    ('2q2*2', HandType.FOUROFAKIND),
    ('a2aa2', HandType.FULLHOUSE),
    ('a2a*2', HandType.FULLHOUSE),
    ('a2345', HandType.STRAIGHT),
    ('a2*45', HandType.STRAIGHT),
    ('tjqka', HandType.STRAIGHT),
    ('6789t', HandType.STRAIGHT),
    ('kkak2', HandType.THREEOFAKIND),
    ('k*ak2', HandType.THREEOFAKIND),
    ('a2a32', HandType.TWOPAIR),
    ('53929', HandType.PAIR),
    ('aa234', HandType.PAIR),
    ('a*237', HandType.PAIR),
    ('a9725', HandType.HIGHCARD),
])
def test_type(hand, expected):
    assert expected == Hand(hand).hand_type


@pytest.mark.parametrize(('hand', 'expected'), [
    ('2q222', ['2', 'q']),
    ('2q2*2', ['2', 'q']),
    ('2*222', ['2', 'a']),
    ('aaaa*', ['a', 'k']),
    ('a2aa2', ['a', '2']),
    ('a2a*2', ['a', '2']),
    ('a2345', ['5']),
    ('*2345', ['6']),
    ('tjqka', ['a']),
    ('tjqk*', ['a']),
    ('*jqka', ['a']),
    ('6789t', ['t']),
    ('kkak2', ['k', 'a', '2']),
    ('kka*2', ['k', 'a', '2']),
    ('a2a32', ['a', '2', '3']),
    ('53929', ['9', '5', '3', '2']),
    ('a9725', ['a', '9', '7', '5', '2']),
    ('*9725', ['9', '7', '5', '2']),
])
def test_rank(hand, expected):
    assert expected == Hand(hand).rank


# @pytest.mark.parametrize(('hand_a', 'hand_b', 'expected'), [
#     ('AAKKK', '23456', '0'),
#     ('KA225', '33A47', '1'),
#     ('AA225', '44465', '1'),
#     ('TT4A2', 'TTA89', '01'),
#     ('A345*', '254*6', '1'),
#     ('QQ2AT', 'QQT2J', '0'),
# ])
# def test_compare_hand(hand_a, hand_b, expected):
#     assert expected == compare_hands(Hand(hand_a), Hand(hand_b))
