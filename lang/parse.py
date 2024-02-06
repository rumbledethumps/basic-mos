from lang.ast import Statement
from lang.tokens import TokenScan, Token, Literal, Word, Ident, Operator
from lang.error import Error, ErrorCode


class BasicParser:
    def parse(tokens: list[Token]) -> list[Statement]:
        parse = BasicParser(tokens)
        match parse.peek():
            case (
                Token.Literal(Literal.Integer(_))
                | Token.Literal(Literal.Single(_))
                | Token.Literal(Literal.Double(_))
            ):
                raise Error(ErrorCode.UndefinedLine).add_column(parse.col).add_message(
                    "INVALID LINE NUMBER"
                )
        return parse.expect_statements()

    def __init__(self, tokens: list[Token]):
        self.token_stream = iter(tokens)
        self.peeked = None
        self.rem = False
        self.col = range(0)

    def peek(self) -> Token:
        if self.peeked == None:
            try:
                self.peeked = self.next()
            except StopIteration:
                self.peeked = None
            return self.peeked
        return self.peeked

    def next(self) -> Token:
        if self.peeked != None:
            rv = self.peeked
            self.peeked = None
            return rv
        while True:
            self.col = range(self.col.stop)
            token = next(self.token_stream)
            if token in (Token.Word(Word.Rem1), Token.Word(Word.Rem2)):
                self.rem = True
            if self.rem:
                continue
            self.col = range(self.col.start, self.col.stop + len(str(token)))
            match token:
                case Token.Whitespace(_):
                    continue
                case _:
                    return token

    def expect_statements(self) -> list[Statement]:
        statements = list()
        expect_colon = False
        while True:
            pk = self.peek()
            match pk:
                case None | Token.Word(Word.Else):
                    return statements
                case Token.Colon:
                    expect_colon = False
                    self.next()
                    continue
                case _:
                    if expect_colon:
                        raise Error(ErrorCode.SyntaxError).add_column(
                            self.col
                        ).add_message("UNEXPECTED TOKEN")
                    statements.append(Statement.expect(self))
                    expect_colon = True


def parse(line_number: int | None, tokens: list[Token]) -> list[Statement]:
    try:
        return BasicParser.parse(tokens)
    except Error as e:
        raise e.add_line_number(line_number)
