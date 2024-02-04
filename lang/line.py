from lang.tokens import Token
from lang.ast import Statement


class Line:
    def __init__(self, number: int | None, tokens: list[Token]):
        self.number = number
        self.tokens = tokens

    def __str__(self):
        if self.number == None:
            return "".join([str(x) for x in self.tokens])
        else:
            return str(self.number) + " " + "".join([str(x) for x in self.tokens])

    def parse(self) -> list[Statement]:
        return []
