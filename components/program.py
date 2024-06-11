class Program:
    def __init__(self):
        self.rules = []
        self.facts = []
        self.types = {}
        self.predicates = set()

    def add_rule(self, rule):
        self.rules.append(rule)

    def add_fact(self, fact):
        self.facts.append(fact)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        result = "Rules:\n"
        for rule in self.rules:
            result += f"  {rule}\n"
        result += "Facts:\n"
        for fact in self.facts:
            result += f"  {fact}\n"
        return result
