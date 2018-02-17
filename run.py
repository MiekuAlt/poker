#!/usr/bin/env python

import argparse

from poker.poker import Hand, compare_hands


def main():
    """ Parses command line arguments and run the poker module """
    parser = argparse.ArgumentParser(description='Determine winning poker hand.')
    parser.add_argument('hand_a', metavar='HAND_A', help="the first player's hand")
    parser.add_argument('hand_b', metavar='HAND_B', help="the second player's hand")

    args = parser.parse_args()
    hand_a = Hand(args.hand_a)
    hand_b = Hand(args.hand_b)
    result = compare_hands(hand_a, hand_b)
    print('{}, {}, {}'.format(hand_a.hand_type.name, hand_b.hand_type.name, result))

if __name__ == '__main__':
    main()
