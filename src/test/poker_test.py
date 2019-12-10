import unittest
from hypothesis import given, settings, assume, Verbosity, strategies as st
import random

from src.app.card import Deck, Card, Suit, Value
from src.app.hand import Hand, Play, Result, calculate_play_hand


DeckStrategy = st.builds(Deck)

NaiveHandStrategy = st.builds(Hand, st.sets(
    st.builds(Card, 
        st.sampled_from(Suit), 
        st.sampled_from(Value))
    , max_size = 5
    , min_size = 5))


@st.composite
def three_of_a_kind_in_hand(draw) -> Hand:
    d = draw(DeckStrategy)
    r = draw(st.randoms())

    #1
    sample = r.choice(list(d.deck))
    cards = set([sample])
    #2
    sample = Card(sample.suit.next(), sample.val.next())
    cards.add(sample)
    #3
    sample = Card(sample.suit.next(), sample.val.next())
    cards.add(sample)
    #4
    sample = Card(sample.suit.next(), sample.val)
    cards.add(sample)
    #5
    sample = Card(sample.suit.next(), sample.val)
    cards.add(sample)

    return Hand(cards)


@st.composite
def full_house_in_hand(draw) -> Hand:
    d = draw(DeckStrategy)
    r = draw(st.randoms())

    #1
    sample = r.choice(list(d.deck))
    cards = set([sample])
    #2
    sample = Card(sample.suit.next(), sample.val)
    cards.add(sample)
    #3
    sample = Card(sample.suit.next(), sample.val.next())
    cards.add(sample)
    #4
    sample = Card(sample.suit.next(), sample.val)
    cards.add(sample)
    #5
    sample = Card(sample.suit.next(), sample.val)
    cards.add(sample)

    return Hand(cards)


@st.composite
def straight_in_hand(draw) -> Hand:
    blacklist = {Value.JACK, Value.QUEEN, Value.KING}
    d = draw(DeckStrategy)
    r = draw(st.randoms())

    sample = r.choice(list(d.deck))

    assume(not sample.val in blacklist)

    # while v in blacklist:
    #     v = random.choice(list(Value))

    cards = set([sample])
    for _ in range(4):
        sample = Card(sample.suit.next(), sample.val.next())
        cards.add(sample)

    return Hand(cards)



class PokerTest(unittest.TestCase):

    @given(d=DeckStrategy, 
           n_gets=st.integers(min_value=0, max_value=55), 
           m_sets=st.integers(min_value=0, max_value=55))
    #@settings(verbosity=Verbosity.verbose)
    def test_deck_gets_and_sets(self, d: Deck, n_gets, m_sets) -> None:
        """
        Tests if the deck class takes and returns properly cards
        """
        withdraws = list()
        for _ in range(n_gets+1):
            card = d.get_random_card()
            if card:
                withdraws.append(card)

        for _ in range(m_sets+1):
            if withdraws:
                card = random.choice(withdraws)
                withdraws.remove(card)
                d.set_card(card)

        self.assertEqual(len(withdraws) + len(d.deck), Deck.TOTAL_CARDS)


    @given(hand=NaiveHandStrategy)
    @settings(max_examples=150)
    def test_hand_plays_value(self, hand: Hand) -> None:
        calculate_play_hand(hand)
        assert hand.value > 0 and len(hand.cards) == 5


    @given(hand=three_of_a_kind_in_hand())
    def test_three_of_a_kind(self, hand: Hand) -> None:
        calculate_play_hand(hand)
        self.assertEqual(hand.play, Play.THREE_OF_A_KIND)


    @given(hand=full_house_in_hand())
    def test_full_house(self, hand: Hand) -> None:
        calculate_play_hand(hand)
        self.assertEqual(hand.play, Play.FULL_HOUSE)


    @given(hand=straight_in_hand())
    def test_straight(self, hand: Hand) -> None:
        calculate_play_hand(hand)
        self.assertEqual(hand.play, Play.STRAIGHT)


    @given(hand1=st.one_of(full_house_in_hand(), straight_in_hand()),
            hand2=st.one_of(three_of_a_kind_in_hand()))
    #@settings(verbosity=Verbosity.verbose)
    def test_two_hands(self, hand1: Hand, hand2: Hand) -> None:
        calculate_play_hand(hand1)
        calculate_play_hand(hand2)
        self.assertEqual(Result.WIN, hand1.compare(hand2))

if __name__ == "__main__":
    unittest.main()