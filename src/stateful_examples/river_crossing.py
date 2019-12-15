import unittest
from enum import Enum
from hypothesis import settings, note
from hypothesis.stateful import RuleBasedStateMachine, rule, invariant, precondition

class Side(Enum):
    Left = 0
    Right = 1

    def __str__(self) -> str:
        return 'L' if self.value == Side.Left.value else 'R'

    def switch(self):
        return Side.Left if self.value == Side.Right.value else self.Right 


class RiverCrossing(RuleBasedStateMachine):
    def __init__(self) -> None:
        super(RiverCrossing, self).__init__()
        self.shepherd = Side.Left
        self.wolf = Side.Left
        self.goat = Side.Left
        self.cabbage = Side.Left 

    def is_disaster(self):
        return (self.shepherd != self.goat) and ((self.wolf == self.goat) or (self.cabbage == self.goat))

    def is_final_state(self):
        r = Side.Right
        return self.shepherd == r and self.wolf == r and self.goat == r and self.cabbage == r

    @rule()
    def cross_shepherd(self) -> None:
        self.shepherd = self.shepherd.switch()

    @precondition(lambda self: self.shepherd == self.wolf)
    @rule()
    def cross_shepherd_wolf(self) -> None:
        self.shepherd = self.shepherd.switch()
        self.wolf = self.wolf.switch()

    @precondition(lambda self: self.shepherd == self.goat)
    @rule()
    def cross_shepherd_goat(self) -> None:
        self.shepherd = self.shepherd.switch()
        self.goat = self.goat.switch()

    @precondition(lambda self: self.shepherd == self.cabbage)
    @rule()
    def cross_shepherd_cabbage(self) -> None:
        self.shepherd = self.shepherd.switch()
        self.cabbage = self.cabbage.switch()

    @invariant()
    def solve(self) -> None:
        note(f"S({self.shepherd}) W({self.wolf}) G({self.goat}) C({self.cabbage})")
        assert not self.is_final_state()

if __name__ == "__main__":
    RiverCrossing.TestCase.settings = settings(max_examples=100, stateful_step_count=50)
    RiverCrossingTest = RiverCrossing.TestCase
    unittest.main()