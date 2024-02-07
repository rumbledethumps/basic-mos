from lang.tokens import Token, Word, Operator, Literal
from lang.error import Error, ErrorCode


class Ident:
    class Base:
        __match_args__ = "text"

        def __init__(self, text: str):
            self.text = text

        def __str__(self):
            return self.text

        def __eq__(self, other):
            return self.text == other.text

    class Plain(Base):
        def __repr__(self):
            return f"Ident.Plain({repr(self.text)})"

    class String(Base):
        def __repr__(self):
            return f"Ident.String({repr(self.text)})"

    class Single(Base):
        def __repr__(self):
            return f"Ident.Single({repr(self.text)})"

    class Double(Base):
        def __repr__(self):
            return f"Ident.Double({repr(self.text)})"

    class Integer(Base):
        def __repr__(self):
            return f"Ident.Integer({repr(self.text)})"


class Variable:
    class Base:
        pass

    class Unary(Base):
        __match_args__ = ("col", "ident")

        def __eq__(self, other):
            if not isinstance(other, type(self)):
                return False
            return self.ident == other.ident

        def __init__(self, col: range, ident: Ident.Base):
            self.col = col
            self.ident = ident

        def __repr__(self):
            return f"Variable.Unary({repr(self.col)}, {repr(self.ident)})"

    class Array(Base):
        __match_args__ = ("col", "ident", "list_expr")

        def __eq__(self, other):
            if not isinstance(other, type(self)):
                return False
            return self.ident == other.ident and self.list_expr == other.list_expr

        def __init__(self, col: range, ident: Ident.Base, list_expr: list):
            self.col = col
            self.ident = ident
            self.list_expr = list_expr

    # Accept visitors

    def accept(self, visitor):
        match self:
            case Variable.Array(_, _, list_expr):
                for expr in list_expr:
                    expr.accept(visitor)
        visitor.visit_variable(self)


class Expression:
    class Base:
        pass

    class Variable(Base):
        __match_args__ = "var"

        def __init__(self, var: int):
            self.var = var

        def __eq__(self, other):
            if not isinstance(other, type(self)):
                return False
            return self.var == other.var

    class Single(Base):
        __match_args__ = ("col", "f32")

        def __init__(self, col: range, f32: float):
            self.col = col
            self.f32 = f32

        def __eq__(self, other):
            if not isinstance(other, type(self)):
                return False
            return self.f32 == other.f32

    class Double(Base):
        __match_args__ = ("col", "f64")

        def __init__(self, col: range, f64: float):
            self.col = col
            self.f64 = f64

        def __eq__(self, other):
            if not isinstance(other, type(self)):
                return False
            return self.f64 == other.f64

    class Integer(Base):
        __match_args__ = ("col", "i16")

        def __init__(self, col: range, i16: int):
            self.col = col
            self.i16 = i16

        def __eq__(self, other):
            if not isinstance(other, type(self)):
                return False
            return self.i16 == other.i16

        def __repr__(self):
            return f"Expression.Integer({repr(self.col)}, {repr(self.i16)})"

    class String(Base):
        __match_args__ = ("col", "text")

        def __init__(self, col: range, text: str):
            self.col = col
            self.text = text

        def __eq__(self, other):
            if not isinstance(other, type(self)):
                return False
            return self.text == other.text

        def __repr__(self):
            return f"Expression.String({repr(self.col)}, {repr(self.text)})"

    class _ColExpr(Base):
        __match_args__ = ("col", "expr")

        def __init__(self, col: range, expr):
            self.col = col
            self.expr = expr

    class _ColExprExpr(Base):
        __match_args__ = ("col", "expr0", "expr1")

        def __init__(self, col: range, expr0, expr1):
            self.col = col
            self.expr0 = expr0
            self.expr1 = expr1

    class Negation(_ColExpr):
        pass

    class Power(_ColExprExpr):
        pass

    class Multiply(_ColExprExpr):
        pass

    class Divide(_ColExprExpr):
        pass

    class DivideInt(_ColExprExpr):
        pass

    class Modulo(_ColExprExpr):
        pass

    class Add(_ColExprExpr):
        pass

    class Subtract(_ColExprExpr):
        pass

    class Equal(_ColExprExpr):
        pass

    class NotEqual(_ColExprExpr):
        pass

    class Less(_ColExprExpr):
        pass

    class LessEqual(_ColExprExpr):
        pass

    class Greater(_ColExprExpr):
        pass

    class GreaterEqual(_ColExprExpr):
        pass

    class Not(_ColExpr):
        pass

    class And(_ColExprExpr):
        pass

    class Or(_ColExprExpr):
        pass

    class Xor(_ColExprExpr):
        pass

    class Imp(_ColExprExpr):
        pass

    class Eqv(_ColExprExpr):
        pass

    # Accept visitors

    def accept(self, visitor):
        match self:
            case Expression.Variable(var):
                var.accept(visitor)
            case Expression.Negation(_, expr) | Expression.Not(_, expr):
                expr.accept(visitor)
            case (
                Expression.Power(_, expr0, expr1)
                | Expression.Multiply(_, expr0, expr1)
                | Expression.Divide(_, expr0, expr1)
                | Expression.DivideInt(_, expr0, expr1)
                | Expression.Modulo(_, expr0, expr1)
                | Expression.Add(_, expr0, expr1)
                | Expression.Subtract(_, expr0, expr1)
                | Expression.Equal(_, expr0, expr1)
                | Expression.NotEqual(_, expr0, expr1)
                | Expression.Less(_, expr0, expr1)
                | Expression.LessEqual(_, expr0, expr1)
                | Expression.Greater(_, expr0, expr1)
                | Expression.GreaterEqual(_, expr0, expr1)
                | Expression.And(_, expr0, expr1)
                | Expression.Or(_, expr0, expr1)
                | Expression.Xor(_, expr0, expr1)
                | Expression.Imp(_, expr0, expr1)
                | Expression.Eqv(_, expr0, expr1)
            ):
                expr0.accept(visitor)
                expr1.accept(visitor)
        visitor.visit_expression(self)

    def expect(parse, var_map: dict[Ident, Variable]) -> Base:
        def descend(parse, var_map, precedence):
            match parse.next():  # lhs =
                case Token.LParen:
                    expr = descend(parse, var_map, 0)
                    parse.expect(Token.RParen)
                    lhs = expr
                case Token.Ident(tok_ident):
                    col = range(parse.col.start, parse.col.stop)
                    match parse.peek():
                        case Token.LParen:
                            parse.expect(Token.LParen)
                            list_expr = list()
                            if not parse.maybe(Token.RParen):
                                list_expr = parse.expect_fn_expression_list(var_map)
                                parse.expect(Token.RParen)
                            col = range(col.start, parse.col.stop)
                            lhs = Expression.Variable(
                                Variable.Array(col, tok_ident, list_expr)
                            )
                        case _:
                            if tok_ident.is_user_function():
                                raise Error(ErrorCode.SyntaxError).add_column(
                                    col
                                ).add_message("FN RESERVED FOR FUNCTIONS")
                            if tok_ident in var_map:
                                lhs = Expression.Variable(var_map[tok_ident])
                            else:
                                lhs = Expression.Variable(
                                    Variable.Unary(col, tok_ident)
                                )
                case Token.Operator(Operator.Plus):
                    op_prec = Expression.unary_op_precedence(Operator.Plus)
                    lhs = descend(parse, var_map, op_prec)
                case Token.Operator(Operator.Minus):
                    col = range(parse.col.start, parse.col.stop)
                    op_prec = Expression.unary_op_precedence(Operator.Minus)
                    expr = descend(parse, var_map, op_prec)
                    lhs = Expression.Negation(col, expr)
                case Token.Operator(Operator.Not):
                    col = range(parse.col.start, parse.col.stop)
                    op_prec = Expression.unary_op_precedence(Operator.Not)
                    expr = descend(parse, var_map, op_prec)
                    lhs = Expression.Not(col, expr)
                case Token.Literal(lit):
                    lhs = Expression.literal(parse.col, lit)
                case _:
                    raise Error(ErrorCode.SyntaxError).add_column(
                        parse.col
                    ).add_message("EXPECTED EXPRESSION")
            while True:
                match parse.peek():
                    case Token.Operator(op):
                        op_prec = Expression.binary_op_precedence(op)
                        if op_prec <= precedence:
                            break
                        parse.next()
                        column = range(parse.col.start, parse.col.stop)
                        rhs = descend(parse, var_map, op_prec)
                        lhs = Expression.binary_op(column, op, lhs, rhs)
                    case _:
                        break
            return lhs

        return descend(parse, var_map, 0)

    def binary_op(col: range, op: Operator, lhs: Base, rhs: Base) -> Base:
        match op:
            case Operator.Caret:
                return (Expression.Power(col, lhs, rhs),)
            case Operator.Multiply:
                return (Expression.Multiply(col, lhs, rhs),)
            case Operator.Divide:
                return (Expression.Divide(col, lhs, rhs),)
            case Operator.DivideInt:
                return (Expression.DivideInt(col, lhs, rhs),)
            case Operator.Modulo:
                return (Expression.Modulo(col, lhs, rhs),)
            case Operator.Plus:
                return (Expression.Add(col, lhs, rhs),)
            case Operator.Minus:
                return (Expression.Subtract(col, lhs, rhs),)
            case Operator.Equal:
                return (Expression.Equal(col, lhs, rhs),)
            case Operator.NotEqual:
                return (Expression.NotEqual(col, lhs, rhs),)
            case Operator.Less:
                return (Expression.Less(col, lhs, rhs),)
            case Operator.LessEqual:
                return (Expression.LessEqual(col, lhs, rhs),)
            case Operator.Greater:
                return (Expression.Greater(col, lhs, rhs),)
            case Operator.GreaterEqual:
                return (Expression.GreaterEqual(col, lhs, rhs),)
            case Operator.And:
                return (Expression.And(col, lhs, rhs),)
            case Operator.Or:
                return (Expression.Or(col, lhs, rhs),)
            case Operator.Xor:
                return (Expression.Xor(col, lhs, rhs),)
            case Operator.Imp:
                return (Expression.Imp(col, lhs, rhs),)
            case Operator.Eqv:
                return (Expression.Eqv(col, lhs, rhs),)
        raise Error(ErrorCode.InternalError).add_column(col)

    def unary_op_precedence(op: Operator) -> int:
        match op:
            case Operator.Plus | Operator.Minus:
                return 12
            case Operator.Not:
                return 6
        return 0

    def binary_op_precedence(op: Operator) -> int:
        match op:
            case Operator.Caret:
                return 13
            case Operator.Multiply | Operator.Divide:
                return 11
            case Operator.DivideInt:
                return 10
            case Operator.Modulo:
                return 9
            case Operator.Plus | Operator.Minus:
                return 8
            case (
                Operator.Equal
                | Operator.NotEqual
                | Operator.Less
                | Operator.LessEqual
                | Operator.Greater
                | Operator.GreaterEqual
            ):
                return 7
            case Operator.And:
                return 5
            case Operator.Or:
                return 4
            case Operator.Xor:
                return 3
            case Operator.Imp:
                return 2
            case Operator.Eqv:
                return 1
        return 0

    def literal(col: range, lit) -> Base:
        # TODO validate parsers
        def parse_float(s: str):
            s = s.replace("D", "E")
            if s[-1] in ["!", "#", "%"]:
                s = s[:-1]
            return float(s)

        def parse_radix(s: str, radix: int):
            return int(s, radix)

        match lit:
            case Literal.Hex(s):
                return Expression.Integer(col, parse_radix(s, 16))
            case Literal.Octal(s):
                return Expression.Integer(col, parse_radix(s, 8))
            case Literal.Single(s):
                return Expression.Single(col, parse_float(s))
            case Literal.Double(s):
                return Expression.Double(col, parse_float(s))
            case Literal.Integer(s):
                return Expression.Integer(col, parse_radix(s, 10))
            case Literal.String(s):
                if len(s) > 255:
                    raise Error(ErrorCode.StringTooLong).add_column(col).add_message(
                        "MAXIMUM LITERAL LENGTH IS 255"
                    )
                return Expression.String(col, s)


class Statement:
    class Base:
        pass

    # Match patterns

    class _Col(Base):
        __match_args__ = "col"

        def __init__(self, col: range):
            self.col = col

    class _ColListExpr(Base):
        __match_args__ = ("col", "list_expr")

        def __init__(self, col: range, list_expr: list[Expression]):
            self.col = col
            self.list_expr = list_expr

    class _ColListVar(Base):
        __match_args__ = ("col", "list_var")

        def __init__(self, col: range, list_var: list[Variable]):
            self.col = col
            self.list_var = list_var

    class _ColVarVar(Base):
        __match_args__ = ("col", "var0", "var1")

        def __init__(self, col: range, var0: Variable, var1: Variable):
            self.col = col
            self.var0 = var0
            self.var1 = var1

    class _ColExpr(Base):
        __match_args__ = ("col", "expr")

        def __init__(self, col: range, expr: Expression):
            self.col = col
            self.expr = expr

    class _ColExprExpr(Base):
        __match_args__ = ("col", "expr0", "expr1")

        def __init__(self, col: range, expr0: Expression, expr1: Expression):
            self.col = col
            self.expr0 = expr0
            self.expr1 = expr1

    class _ColExprListExpr(Base):
        __match_args__ = ("col", "expr", "list_expr")

        def __init__(self, col: range, expr: Expression, list_expr: list[Expression]):
            self.col = col
            self.expr = expr
            self.list_expr = list_expr

    class _ColVarExprExprExpr(Base):
        __match_args__ = ("col", "var", "expr0", "expr1", "expr2")

        def __init__(
            self,
            col: range,
            var: Variable,
            expr0: Expression,
            expr1: Expression,
            expr2: Expression,
        ):
            self.col = col
            self.var = var
            self.expr0 = expr0
            self.expr1 = expr1
            self.expr2 = expr2

    # Statements

    class Clear(_Col):
        pass

    class Cls(_Col):
        pass

    class Cont(_Col):
        pass

    class Data(_ColListExpr):
        pass

    class Def(Base):
        __match_args__ = ("col", "var", "list_var", "expr")

        def __init__(
            self, col: range, var: Variable, list_var: list[Variable], expr: Expression
        ):
            self.col = col
            self.var = var
            self.list_var = list_var
            self.expr = expr

    class Defdbl(_ColVarVar):
        pass

    class Defint(_ColVarVar):
        pass

    class Defsng(_ColVarVar):
        pass

    class Defstr(_ColVarVar):
        pass

    class Delete(_ColExprExpr):
        pass

    class Dim(_ColListVar):
        pass

    class End(_Col):
        pass

    class Erase(_ColListVar):
        pass

    class For(_ColVarExprExprExpr):
        pass

    class Gosub(_ColExpr):
        pass

    class Goto(_ColExpr):
        pass

    class If(Base):
        __match_args__ = ("col", "expr", "list_statement0", "list_statement1")

        def __init__(
            self,
            col: range,
            expr: Expression,
            list_statement0: list,
            list_statement1: list,
        ):
            self.col = col
            self.expr = expr
            self.list_statement0 = list_statement0
            self.list_statement1 = list_statement1

        def __repr__(self):
            return f"Statement.If({repr(self.col)}, {repr(self.expr)}, {repr(self.list_statement0)}, {repr(self.list_statement1)})"

        def expect(parse):
            column = range(parse.col.start, parse.col.stop)
            predicate = parse.expect_expression()
            if parse.maybe(Token.Word(Word.Goto)):
                then_stmt = [Statement.Goto(parse.col, parse.expect_line_number())]
            else:
                parse.expect(Token.Word(Word.Then))
                match parse.maybe_line_number():
                    case None:
                        then_stmt = parse.expect_statements()
                    case n:
                        then_stmt = [
                            Statement.Goto(
                                column, Expression.Single(parse.col, float(n))
                            )
                        ]
            if parse.maybe(Token.Word(Word.Else)):
                match parse.maybe_line_number():
                    case None:
                        else_stmt = parse.expect_statements()
                    case n:
                        else_stmt = [
                            Statement.Goto(
                                column, Expression.Single(parse.col, float(n))
                            )
                        ]
            else:
                else_stmt = []
            return Statement.If(column, predicate, then_stmt, else_stmt)

    class Input(Base):
        __match_args__ = ("col", "expr0", "expr1", "list_var")

        def __init__(
            self,
            col: range,
            expr0: Expression,
            expr1: Expression,
            list_var: list[Variable],
        ):
            self.col = col
            self.expr0 = expr0
            self.expr1 = expr1
            self.list_var = list_var

    class Let(Base):
        __match_args__ = ("col", "var", "expr")

        def __init__(self, col: range, var: Variable, expr: Expression):
            self.col = col
            self.var = var
            self.expr = expr

        def __repr__(self):
            return (
                f"Statement.Let({repr(self.col)}, {repr(self.var)}, {repr(self.expr)})"
            )

        def __eq__(self, other):
            if not isinstance(other, type(self)):
                return False
            return self.var == other.var and self.expr == other.expr

        def expect(parse, is_shortcut):
            pk = parse.peek()
            column = range(parse.col.start, parse.col.stop)
            match pk:
                case Token.Ident(Ident.String(s)) if s == "MID$":
                    parse.next()
                    parse.expect(Token.LParen)
                    var = parse.expect_var()
                    parse.expect(Token.Comma)
                    pos = parse.expect_expression()
                    if parse.maybe(Token.Comma):
                        length = parse.expect_expression()
                    else:
                        length = Expression.Integer(parse.col, 32767)
                    parse.expect(Token.RParen)
                    parse.expect(Token.Operator(Operator.Equal))
                    expr = parse.expect_expression()
                    return Statement.Mid(column, var, pos, length, expr)
            var = parse.expect_var()
            match parse.next():
                case Token.Operator(Operator.Equal):
                    return Statement.Let(column, var, parse.expect_expression())
            if is_shortcut:
                raise Error(ErrorCode.SyntaxError).add_column(column).add_message(
                    "UNKNOWN STATEMENT"
                )
            else:
                raise Error(ErrorCode.SyntaxError).add_column(parse.col).add_message(
                    "EXPECTED EQUALS SIGN"
                )

    class List(_ColExprExpr):
        pass

    class Load(_ColExpr):
        pass

    class Mid(_ColVarExprExprExpr):
        pass

    class New(_Col):
        pass

    class Next(_ColListVar):
        pass

    class OnGoto(_ColExprListExpr):
        pass

    class OnGosub(_ColExprListExpr):
        pass

    class Print(_ColListExpr):
        pass

    class Read(_ColListVar):
        pass

    class Renum(Base):
        __match_args__ = ("col", "expr0", "expr1", "expr2")

        def __init__(
            self,
            col: range,
            expr0: Expression,
            expr1: Expression,
            expr2: Expression,
        ):
            self.col = col
            self.expr0 = expr0
            self.expr1 = expr1
            self.expr2 = expr2

    class Restore(_ColExpr):
        pass

    class Return(_Col):
        pass

    class Run(_ColExpr):
        pass

    class Save(_ColExpr):
        pass

    class Stop(_Col):
        pass

    class Swap(_ColVarVar):
        pass

    class Troff(_Col):
        pass

    class Tron(_Col):
        pass

    class Wend(_Col):
        pass

    class While(_ColExpr):
        pass

    # Accept visitors

    def accept(self, visitor):
        match self:
            case Statement.Data(_, list_expr):
                for expr in list_expr:
                    expr.accept(visitor)
            case Statement.Def(_, var, list_var, expr):
                var.accept(visitor)
                for v in list_var:
                    v.accept(visitor)
                expr.accept(visitor)
            case (
                Statement.Defdbl(_, var0, var1)
                | Statement.Defint(_, var0, var1)
                | Statement.Defsng(_, var0, var1)
                | Statement.Defstr(_, var0, var1)
                | Statement.Swap(_, var0, var1)
            ):
                var0.accept(visitor)
                var1.accept(visitor)
            case Statement.Mid(_, var, expr0, expr1, expr2) | Statement.For(
                _, var, expr0, expr1, expr2
            ):
                var.accept(visitor)
                expr0.accept(visitor)
                expr1.accept(visitor)
                expr2.accept(visitor)
            case (
                Statement.Gosub(_, expr)
                | Statement.Goto(_, expr)
                | Statement.Load(_, expr)
                | Statement.Restore(_, expr)
                | Statement.Run(_, expr)
                | Statement.Save(_, expr)
                | Statement.While(_, expr)
            ):
                expr.accept(visitor)
            case Statement.If(_, expr, list_statement0, list_statement1):
                expr.accept(visitor)
                for statement in list_statement0:
                    statement.accept(visitor)
                for statement in list_statement1:
                    statement.accept(visitor)
            case Statement.Let(_, var, expr):
                var.accept(visitor)
                expr.accept(visitor)
            case Statement.Delete(_, expr0, expr1) | Statement.List(_, expr0, expr1):
                expr0.accept(visitor)
                expr1.accept(visitor)
            case Statement.Input(_, expr0, expr1, list_var):
                expr0.accept(visitor)
                expr1.accept(visitor)
                for var in list_var:
                    var.accept(visitor)
            case Statement.OnGoto(_, expr, list_expr):
                expr.accept(visitor)
                for expr in list_expr:
                    expr.accept(visitor)
            case Statement.Renum(_, var, expr0, expr1, expr2):
                var.accept(visitor)
                expr0.accept(visitor)
                expr1.accept(visitor)
                expr2.accept(visitor)
            case (
                Statement.Dim(_, list_var)
                | Statement.Erase(_, list_var)
                | Statement.Next(_, list_var)
                | Statement.Read(_, list_var)
            ):
                for var in list_var:
                    var.accept(visitor)
        visitor.visit_statement(self)

    def expect(parse) -> Base:
        pk = parse.peek()
        match pk:
            case Token.Ident(_):
                return Statement.Let.expect(parse, True)
            case Token.Word(word):
                parse.next()
                match word:
                    case Word.Clear:
                        return Statement.Clear.expect(parse)
                    case Word.Cls:
                        return Statement.Cls.expect(parse)
                    case Word.Cont:
                        return Statement.Cont.expect(parse)
                    case Word.Data:
                        return Statement.Data.expect(parse)
                    case Word.Def:
                        return Statement.Def.expect(parse)
                    case Word.Defdbl:
                        return Statement.Defdbl.expect(parse)
                    case Word.Defint:
                        return Statement.Defint.expect(parse)
                    case Word.Defsng:
                        return Statement.Defsng.expect(parse)
                    case Word.Defstr:
                        return Statement.Defstr.expect(parse)
                    case Word.Delete:
                        return Statement.Delete.expect(parse)
                    case Word.Dim:
                        return Statement.Dim.expect(parse)
                    case Word.End:
                        return Statement.End.expect(parse)
                    case Word.Erase:
                        return Statement.Erase.expect(parse)
                    case Word.For:
                        return Statement.For.expect(parse)
                    case Word.Gosub:
                        return Statement.Gosub.expect(parse)
                    case Word.Goto:
                        return Statement.Goto.expect(parse)
                    case Word.If:
                        return Statement.If.expect(parse)
                    case Word.Input:
                        return Statement.Input.expect(parse)
                    case Word.Let:
                        return Statement.Let.expect(parse, False)
                    case Word.List:
                        return Statement.List.expect(parse)
                    case Word.Load:
                        return Statement.Load.expect(parse)
                    case Word.New:
                        return Statement.New.expect(parse)
                    case Word.Next:
                        return Statement.Next.expect(parse)
                    case Word.On:
                        return Statement.On.expect(parse)
                    case Word.Print:
                        return Statement.Print.expect(parse)
                    case Word.Read:
                        return Statement.Read.expect(parse)
                    case Word.Renum:
                        return Statement.Renum.expect(parse)
                    case Word.Restore:
                        return Statement.Restore.expect(parse)
                    case Word.Return:
                        return Statement.Return.expect(parse)
                    case Word.Save:
                        return Statement.Save.expect(parse)
                    case Word.Stop:
                        return Statement.Stop.expect(parse)
                    case Word.Swap:
                        return Statement.Swap.expect(parse)
                    case Word.Run:
                        return Statement.Run.expect(parse)
                    case Word.Troff:
                        return Statement.Troff.expect(parse)
                    case Word.Tron:
                        return Statement.Tron.expect(parse)
                    case Word.Wend:
                        return Statement.Wend.expect(parse)
                    case Word.While:
                        return Statement.While.expect(parse)
        raise Error(ErrorCode.SyntaxError).add_column(parse.col).add_message(
            "EXPECTED STATEMENT"
        )
