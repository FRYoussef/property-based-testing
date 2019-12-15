import unittest
from hypothesis import settings, assume, note, strategies as st
from hypothesis.stateful import RuleBasedStateMachine, rule, invariant, precondition
import random

class DieHard(RuleBasedStateMachine):
    N_JUGS: int = 3

    def __init__(self) -> None:
        super(DieHard, self).__init__()
        self.jugs: list(tuple) = [(3, 0), (5, 0), (8, 0)]
        self.randomize_indexes(random)

    def randomize_indexes(self, r: random) -> None:
        self.i_jug: int = r.randint(0, self.N_JUGS-1)
        self.j_jug: int = r.randint(0, self.N_JUGS-1)
        while self.j_jug == self.i_jug:
            self.j_jug = r.randint(0, self.N_JUGS-1)

    def is_full(self, i: int) -> bool:
        (m, n) = self.jugs[i]
        return n == m

    def is_empty(self, i: int) -> bool:
        (_, n) = self.jugs[i]
        return n == 0

    @precondition(lambda self: not self.is_full(self.i_jug))
    @rule(r=st.randoms())
    def fill_jug(self, r: random) -> None:
        (m, _) = self.jugs[self.i_jug]
        self.jugs[self.i_jug] = (m, m)
        self.randomize_indexes(r)

    @precondition(lambda self: not self.is_empty(self.i_jug))
    @rule(r=st.randoms())
    def empty_jug(self, r: random) -> None:
        (m, _) = self.jugs[self.i_jug]
        self.jugs[self.i_jug] = (m, 0)
        self.randomize_indexes(r)

    @precondition(lambda self: not (self.is_empty(self.i_jug) and self.is_empty(self.j_jug)))
    @rule(r=st.randoms())
    def pour(self, r: random) -> None:
        (m1, n1) = self.jugs[self.i_jug]
        (m2, n2) = self.jugs[self.j_jug]
        if n1 + n2 <= m2:
            self.jugs[self.i_jug] = (m1, 0)
            self.jugs[self.j_jug] = (m2, n2 + n1)
        else:
            self.jugs[self.i_jug] = (m1, n1 + n2 - m2)
            self.jugs[self.j_jug] = (m2, m2)
        self.randomize_indexes(r)

    @invariant()
    def jugs_constraints(self):
        for (m, n) in self.jugs:
            assert 0 <= n <= m

    @invariant()
    def solve(self) -> None:
        note(f"{self.jugs}")
        for (_, n) in self.jugs:
            assert n != 4



DieHard.TestCase.settings = settings(max_examples=200, stateful_step_count=100)
DieHardTest = DieHard.TestCase