class Atom:
    def __init__(self, predicate, args=None, predicate_type="predicate_const"):
        self.predicate = predicate
        self.predicate_type = predicate_type
        self.args = args if args else []

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        args_str = ', '.join([str(arg) for arg in self.args])
        return f"{self.predicate}({args_str})" if self.args else self.predicate
