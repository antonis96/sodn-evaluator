class Literal:
    def __init__(self, atom, negated=False):
        self.atom = atom
        self.negated = negated

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"not {self.atom}" if self.negated else str(self.atom)
