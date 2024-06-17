class Argument:
    def __init__(self, value, arg_type):
        self.value = value
        self.arg_type = arg_type

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.value

    def __eq__(self, other):
        if isinstance(other, Argument):
            return self.value == other.value
        return False

    def __hash__(self):
        return hash(self.value)