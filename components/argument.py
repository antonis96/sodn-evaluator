class Argument:
    def __init__(self, value, arg_type):
        self.value = value
        self.arg_type = arg_type

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.value
