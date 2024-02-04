class Ident:
    class Base:
        __match_args__ = ("text", "ident")

        def __init__(self, text: str):
            self.text = text

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
        __match_args__ = ("col", "var")

        def __init__(self, col: int, var: float):
            self.col = col
            self.var = var

    class Double(Base):
        __match_args__ = ("col", "var")

        def __init__(self, col: int, var: float):
            self.col = col
            self.var = var

    class Integer(Base):
        __match_args__ = ("col", "var")

        def __init__(self, col: int, var: int):
            self.col = col
            self.var = var

    class String(Base):
        __match_args__ = ("col", "var")

        def __init__(self, col: int, var: str):
            self.col = col
            self.var = var

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


class Statement:
    class Base:
        pass

    class _Col(Base):
        __match_args__ = "col"

        def __init__(self, col: int):
            self.col = col

    class _ColListExpr(Base):
        __match_args__ = ("col", "list_expr")

        def __init__(self, col: int, list_expr: list[Expression]):
            self.col = col
            self.list_expr = list_expr

    class Clear(_Col):
        pass

    class Cls(_Col):
        pass

    class Cont(_Col):
        pass

    class Data(_ColListExpr):
        pass

    def accept(self, visitor):
        match self:
            case Statement.Data(_, list_expr):
                for expr in list_expr:
                    expr.accept(visitor)
