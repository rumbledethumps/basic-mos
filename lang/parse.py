from lang.ast import Statement, Variable, Expression
from lang.tokens import TokenScan, Token, Literal, Word, Ident, Operator
from lang.error import Error, ErrorCode
import lang.line


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

    def next(self) -> Token:
        if self.peeked != None:
            rv = self.peeked
            self.peeked = None
            return rv
        while True:
            self.col = range(self.col.stop, self.col.stop)
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

    def peek(self) -> Token:
        if self.peeked == None:
            try:
                self.peeked = self.next()
            except StopIteration:
                self.peeked = None
            return self.peeked
        return self.peeked

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

    def expect_expression(self) -> Expression:
        return self.expect_fn_expression(dict())

    def expect_expression_list(self) -> list[Expression]:
        return self.expect_fn_expression_list(dict())

    def expect_fn_expression(self, var_map: dict[Ident, Variable]) -> Expression:
        return Expression.expect(self, var_map)

    def expect_fn_expression_list(
        self, var_map: dict[Ident, Variable]
    ) -> list[Expression]:
        expressions = list()
        while True:
            expressions.append(self.expect_fn_expression(var_map))
            if self.maybe(Token.Comma):
                continue
            return expressions

    def expect_print_list(self) -> list[Expression]:
        expressions = list()
        linefeed = True
        while True:
            match self.peek():
                case None | Token.Colon | Token.Word(Word.Else):
                    column = range(self.col.stop, self.col.stop)
                    if linefeed:
                        expressions.append(Expression.String("\n"))
                    return expressions
                case Token.Semicolon:
                    linefeed = False
                    self.next()
                case Token.Comma:
                    linefeed = False
                    self.next()
                    expressions.append(
                        Expression.Variable(
                            Variable.Array(
                                self.col,
                                Ident.String("TAB"),
                                [Expression.Integer(self.col, -14)],
                            )
                        )
                    )
                case _:
                    linefeed = True
                    expressions.append(self.expect_expression())

    def expect_ident(self) -> (range, Ident):
        match self.next():
            case Token.Ident(ident):
                pass
            case _:
                raise Error(ErrorCode.SyntaxError).add_column(self.col).add_message(
                    "EXPECTED VARIABLE"
                )
        col = range(self.col.start, self.col.stop)
        if ident.is_user_function():
            raise Error(ErrorCode.SyntaxError).add_column(col).add_message(
                "FN RESERVED FOR FUNCTIONS"
            )
        match self.peek():
            case Token.LParen:
                raise Error(ErrorCode.SyntaxError).add_column(col).add_message(
                    "ARRAY NOT ALLOWED"
                )
        return (col, ident)

    def expect_ident_list(self) -> list[range, Ident]:
        idents = list()
        expecting = False
        while True:
            match self.peek():
                case None | Token.Colon | Token.Word(Word.Else) if not expecting:
                    break
                case _:
                    idents.append(self.expect_ident)
            if self.maybe(Token.Comma):
                expecting = True
            else:
                break
        return idents

    def expect_var(self) -> Variable:
        match self.next():
            case Token.Ident(ident):
                ident = ident
            case _:
                raise Error(ErrorCode.SyntaxError).add_column(self.col).add_message(
                    "EXPECTED VARIABLE"
                )
        col = range(self.col.start, self.col.stop)
        if ident.is_user_function():
            raise Error(ErrorCode.SyntaxError).add_column(self.col).add_message(
                "FN RESERVED FOR FUNCTIONS"
            )
        match self.peek():
            case Token.LParen:
                self.expect(Token.LParen)
                list_expr = self.expect_expression_list()
                self.expect(Token.RParen)
                return Variable.Array(col, ident, list_expr)
        return Variable.Unary(col, ident)

    def expect_var_list(self) -> list[Variable]:
        list_var = list()
        while True:
            list_var.append(self.expect_var())
            if self.maybe(Token.Comma):
                continue
            break
        return list_var

    def maybe_line_number(self) -> int | None:
        match self.peek():
            case (
                Token.Literal(Literal.Integer(s))
                | Token.Literal(Literal.Single(s))
                | Token.Literal(Literal.Double(s))
            ):
                self.next()
                # TODO validate parse
                num = int(s)
                if num <= lang.line.Line.max_number:
                    return num
                raise Error(ErrorCode.UndefinedLine).add_column(self.col).add_message(
                    "INVALID LINE NUMBER"
                )
        return None

    def expect_line_number(self) -> Expression:
        line_no = self.maybe_line_number()
        if line_no == None:
            raise Error(ErrorCode.SyntaxError).add_column(self.col).add_message(
                "EXPECTED LINE NUMBER"
            )
        return Expression.Single(self.col, float(line_no))

    def expect_line_number_list(self) -> list[Expression]:
        vars = list()
        expecting = False
        while True:
            match self.peek():
                case None | Token.Colon | Token.Word(Word.Else) if not expecting:
                    break
            vars.append(self.expect_line_number)
            if self.maybe(Token.Comma):
                expecting = True
            else:
                break
        return vars


def parse(line_number: int | None, tokens: list[Token]) -> list[Statement]:
    try:
        return BasicParser.parse(tokens)
    except Error as e:
        raise e.add_line_number(line_number)
