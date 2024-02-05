class Ident:
    class Base:
        __match_args__ = "text"

        def __init__(self, text: str):
            self.text = text

        def __str__(self):
            return self.text

    class Plain(Base):
        pass

    class String(Base):
        pass

    class Single(Base):
        pass

    class Double(Base):
        pass

    class Integer(Base):
        pass


class Variable:
    class Base:
        pass

    class Unary(Base):
        __match_args__ = ("col", "ident")

        def __init__(self, col: int, ident: Ident.Base):
            self.col = col
            self.ident = ident

    class Array(Base):
        __match_args__ = ("col", "ident", "list_expr")

        def __init__(self, col: int, ident: Ident.Base, list_expr: list):
            self.col = col
            self.ident = ident
            self.list_expr = list_expr


class Expression:
    class Base:
        pass

    class Variable(Base):
        __match_args__ = "var"

        def __init__(self, var: int):
            self.var = var

    class Single(Base):
        __match_args__ = ("col", "f32")

        def __init__(self, col: int, f32: float):
            self.col = col
            self.f32 = f32

    class Double(Base):
        __match_args__ = ("col", "f64")

        def __init__(self, col: int, f64: float):
            self.col = col
            self.f64 = f64

    class Integer(Base):
        __match_args__ = ("col", "i16")

        def __init__(self, col: int, i16: int):
            self.col = col
            self.i16 = i16

    class String(Base):
        __match_args__ = ("col", "text")

        def __init__(self, col: int, text: str):
            self.col = col
            self.text = text

    class _ColExpr(Base):
        __match_args__ = ("col", "expr")

        def __init__(self, col: int, expr):
            self.col = col
            self.expr = expr

    class _ColExprExpr(Base):
        __match_args__ = ("col", "expr0", "expr1")

        def __init__(self, col: int, expr0, expr1):
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


class Statement:
    class Base:
        pass

    # Match patterns

    class _Col(Base):
        __match_args__ = "col"

        def __init__(self, col: int):
            self.col = col

    class _ColListExpr(Base):
        __match_args__ = ("col", "list_expr")

        def __init__(self, col: int, list_expr: list[Expression]):
            self.col = col
            self.list_expr = list_expr

    class _ColListVar(Base):
        __match_args__ = ("col", "list_var")

        def __init__(self, col: int, list_var: list[Variable]):
            self.col = col
            self.list_var = list_var

    class _ColVarVar(Base):
        __match_args__ = ("col", "var0", "var1")

        def __init__(self, col: int, var0: Variable, var1: Variable):
            self.col = col
            self.var0 = var0
            self.var1 = var1

    class _ColExpr(Base):
        __match_args__ = ("col", "expr")

        def __init__(self, col: int, expr: Expression):
            self.col = col
            self.expr = expr

    class _ColExprExpr(Base):
        __match_args__ = ("col", "expr0", "expr1")

        def __init__(self, col: int, expr0: Expression, expr1: Expression):
            self.col = col
            self.expr0 = expr0
            self.expr1 = expr1

    class _ColExprListExpr(Base):
        __match_args__ = ("col", "expr", "list_expr")

        def __init__(self, col: int, expr: Expression, list_expr: list[Expression]):
            self.col = col
            self.expr = expr
            self.list_expr = list_expr

    class _ColVarExprExprExpr(Base):
        __match_args__ = ("col", "var", "expr0", "expr1", "expr2")

        def __init__(
            self,
            col: int,
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
            self, col: int, var: Variable, list_var: list[Variable], expr: Expression
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
            col: int,
            expr: Expression,
            list_statement0: list,
            list_statement1: list,
        ):
            self.col = col
            self.expr = expr
            self.list_statement0 = list_statement0
            self.list_statement1 = list_statement1

    class Input(Base):
        __match_args__ = ("col", "expr0", "expr1", "list_var")

        def __init__(
            self,
            col: int,
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

        def __init__(self, col: int, var: Variable, expr: Expression):
            self.col = col
            self.var = var
            self.expr = expr

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
            col: int,
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
