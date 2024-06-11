class Rule:
    def __init__(self, head, body):
        self.head = head
        self.body = body

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        body_str = ', '.join([str(literal) for literal in self.body])
        return f"{self.head} :- {body_str}."
