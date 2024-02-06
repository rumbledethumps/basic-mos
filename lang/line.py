from lang.tokens import Token
from lang.ast import Statement
from lang.parse import parse


class Line:
    max_number = 65529

    def __init__(self, number: int | None, tokens: list[Token]):
        self.number = number
        self.tokens = tokens

    def __str__(self):
        if self.number == None:
            return "".join([str(x) for x in self.tokens])
        else:
            return str(self.number) + " " + "".join([str(x) for x in self.tokens])

    def ast(self) -> list[Statement]:
        return parse(self.number, self.tokens)
