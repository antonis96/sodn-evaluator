class Fact:
    def __init__(self, head):
        self.head = head

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"{self.head}."
