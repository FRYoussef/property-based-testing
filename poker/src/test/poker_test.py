import unittest
from hypothesis import given, settings,  Verbosity, strategies as st
import random

from src.app.card import Deck

class PokerTest(unittest.TestCase):
    DeckStrategy = st.builds(Deck)


    @given(d=DeckStrategy, 
           n_gets=st.integers(min_value=0, max_value=55), 
           m_sets=st.integers(min_value=0, max_value=55))
    #@settings(verbosity=Verbosity.verbose)
    def test_deck_gets_and_sets(self, d: Deck, n_gets, m_sets) -> None:
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

        assert len(withdraws) + len(d.deck) == Deck.TOTAL_CARDS




if __name__ == "__main__":
    unittest.main()