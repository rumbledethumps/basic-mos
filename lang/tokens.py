from enum import Enum, auto
from collections import deque


class Word(Enum):
    Clear = auto()
    Cls = auto()
    Cont = auto()
    Data = auto()
    Def = auto()
    Defdbl = auto()
    Defint = auto()
    Defsng = auto()
    Defstr = auto()
    Delete = auto()
    Dim = auto()
    Else = auto()
    End = auto()
    Erase = auto()
    For = auto()
    Gosub = auto()
    Goto = auto()
    If = auto()
    Input = auto()
    Let = auto()
    List = auto()
    Load = auto()
    New = auto()
    Next = auto()
    On = auto()
    Print = auto()
    Read = auto()
    Rem1 = auto()
    Rem2 = auto()
    Renum = auto()
    Restore = auto()
    Return = auto()
    Save = auto()
    Step = auto()
    Stop = auto()
    Swap = auto()
    Run = auto()
    Then = auto()
    To = auto()
    Troff = auto()
    Tron = auto()
    Wend = auto()
    While = auto()


class Operator(Enum):
    Caret = auto()
    Multiply = auto()
    Divide = auto()
    DivideInt = auto()
    Modulo = auto()
    Plus = auto()
    Minus = auto()
    Equal = auto()
    NotEqual = auto()
    Less = auto()
    LessEqual = auto()
    Greater = auto()
    GreaterEqual = auto()
    Not = auto()
    And = auto()
    Or = auto()
    Xor = auto()
    Imp = auto()
    Eqv = auto()


class Literal:
    class Base:
        __match_args__ = ("text", None)

        def __init__(self, text: str):
            self.text = text

        def __eq__(self, other):
            if not isinstance(other, type(self)):
                return False
            return self.text == other.text

        def __str__(self):
            return self.text

    class Single(Base):
        def __repr__(self):
            return f"Literal.Single({repr(self.text)})"

    class Double(Base):
        def __repr__(self):
            return f"Literal.Double({repr(self.text)})"

    class Integer(Base):
        def __repr__(self):
            return f"Literal.Integer({repr(self.text)})"

    class Hex(Base):
        def __repr__(self):
            return f"Literal.Hex({repr(self.text)})"

        def __str__(self):
            return f"&H{self.text}"

    class Octal(Base):
        def __repr__(self):
            return f"Literal.Octal({repr(self.text)})"

        def __str__(self):
            return f"&{self.text}"

    class String(Base):
        def __repr__(self):
            return f"Literal.String({repr(self.text)})"

        def __str__(self):
            return f'"{self.text}"'


class Ident:
    class Base:
        def __init__(self, text: str):
            self.text = text

        def __eq__(self, other):
            if not isinstance(other, type(self)):
                return False
            return self.text == other.text

        def __str__(self):
            return self.text

        def is_user_function(self):
            return self.text[0:2] == "FN"

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


class Token:
    class Base:
        def is_word(self):
            return False

    class Unknown(Base):
        def __init__(self, text: str):
            self.text = text

        def __eq__(self, other):
            if not isinstance(other, type(self)):
                return False
            return self.text == other.text

        def __repr__(self):
            return f"Token.Unknown({repr(self.text)})"

        def __str__(self):
            return self.text

    class Whitespace(Base):
        __match_args__ = ("length", None)

        def __init__(self, length: int):
            self.length = length

        def __eq__(self, other):
            if not isinstance(other, type(self)):
                return False
            return self.length == other.length

        def __repr__(self):
            return f"Token.Whitespace({repr(self.length)})"

        def __str__(self):
            return self.length * " "

    class Literal(Base):
        __match_args__ = ("literal", None)

        def __init__(self, literal: Literal):
            self.literal = literal

        def __eq__(self, other):
            if not isinstance(other, type(self)):
                return False
            return self.literal == other.literal

        def __repr__(self):
            return f"Token.Literal({repr(self.literal)})"

        def __str__(self):
            return str(self.literal)

        def is_word(self):
            return True

    class Ident(Base):
        __match_args__ = ("id", None)

        def __init__(self, ident: Ident):
            self.id = ident

        def __eq__(self, other):
            if not isinstance(other, type(self)):
                return False
            return self.id == other.id

        def __repr__(self):
            return f"Token.Ident({repr(self.id)})"

        def __str__(self):
            return str(self.id)

        def is_word(self):
            return True

    class Word(Base):
        __match_args__ = ("word", None)

        def __init__(self, word: Word):
            self.word = word

        def __eq__(self, other):
            if not isinstance(other, type(self)):
                return False
            return self.word == other.word

        def __repr__(self):
            return f"Token.Word({self.word})"

        def __str__(self):
            match self.word:
                case Word.Clear:
                    return "CLEAR"
                case Word.Cls:
                    return "CLS"
                case Word.Cont:
                    return "CONT"
                case Word.Data:
                    return "DATA"
                case Word.Def:
                    return "DEF"
                case Word.Defdbl:
                    return "DEFDBL"
                case Word.Defint:
                    return "DEFINT"
                case Word.Defsng:
                    return "DEFSNG"
                case Word.Defstr:
                    return "DEFSTR"
                case Word.Delete:
                    return "DELETE"
                case Word.Dim:
                    return "DIM"
                case Word.Else:
                    return "ELSE"
                case Word.End:
                    return "END"
                case Word.Erase:
                    return "ERASE"
                case Word.For:
                    return "FOR"
                case Word.Gosub:
                    return "GOSUB"
                case Word.Goto:
                    return "GOTO"
                case Word.If:
                    return "IF"
                case Word.Input:
                    return "INPUT"
                case Word.Let:
                    return "LET"
                case Word.List:
                    return "LIST"
                case Word.Load:
                    return "LOAD"
                case Word.New:
                    return "NEW"
                case Word.Next:
                    return "NEXT"
                case Word.On:
                    return "ON"
                case Word.Print:
                    return "PRINT"
                case Word.Read:
                    return "READ"
                case Word.Rem1:
                    return "REM"
                case Word.Rem2:
                    return "'"
                case Word.Renum:
                    return "RENUM"
                case Word.Restore:
                    return "RESTORE"
                case Word.Return:
                    return "RETURN"
                case Word.Save:
                    return "SAVE"
                case Word.Step:
                    return "STEP"
                case Word.Stop:
                    return "STOP"
                case Word.Swap:
                    return "SWAP"
                case Word.Run:
                    return "RUN"
                case Word.Then:
                    return "THEN"
                case Word.To:
                    return "TO"
                case Word.Troff:
                    return "TROFF"
                case Word.Tron:
                    return "TRON"
                case Word.Wend:
                    return "WEND"
                case Word.While:
                    return "WHILE"

        def is_word(self):
            return True

    class Operator(Base):
        __match_args__ = ("operator", None)

        def __init__(self, operator: Operator):
            self.operator = operator

        def __eq__(self, other):
            if not isinstance(other, type(self)):
                return False
            return self.operator == other.operator

        def __repr__(self):
            return f"Token.Operator({self.operator})"

        def __str__(self):
            match self.operator:
                case Operator.Caret:
                    return "^"
                case Operator.Multiply:
                    return "*"
                case Operator.Divide:
                    return "/"
                case Operator.DivideInt:
                    return "\\"
                case Operator.Modulo:
                    return "MOD"
                case Operator.Plus:
                    return "+"
                case Operator.Minus:
                    return "-"
                case Operator.Equal:
                    return "="
                case Operator.NotEqual:
                    return "<>"
                case Operator.Less:
                    return "<"
                case Operator.LessEqual:
                    return "<="
                case Operator.Greater:
                    return ">"
                case Operator.GreaterEqual:
                    return ">="
                case Operator.Not:
                    return "NOT"
                case Operator.And:
                    return "AND"
                case Operator.Or:
                    return "OR"
                case Operator.Xor:
                    return "XOR"
                case Operator.Imp:
                    return "IMP"
                case Operator.Eqv:
                    return "EQV"

        def is_word(self):
            return (
                self.operator == Operator.Modulo
                or self.operator == Operator.Not
                or self.operator == Operator.And
                or self.operator == Operator.Or
                or self.operator == Operator.Xor
                or self.operator == Operator.Imp
                or self.operator == Operator.Eqv
            )

    class LParen(Base):
        def __eq__(self, other):
            return isinstance(other, type(self))

        def __repr__(self):
            return f"Token.LParen()"

        def __str__(self):
            return "("

    class RParen(Base):
        def __eq__(self, other):
            return isinstance(other, type(self))

        def __repr__(self):
            return f"Token.RParen()"

        def __str__(self):
            return ")"

    class Comma(Base):
        def __eq__(self, other):
            return isinstance(other, type(self))

        def __repr__(self):
            return f"Token.Comma()"

        def __str__(self):
            return ","

    class Colon(Base):
        def __eq__(self, other):
            return isinstance(other, type(self))

        def __repr__(self):
            return f"Token.Colon()"

        def __str__(self):
            return ":"

    class Semicolon(Base):
        def __eq__(self, other):
            return isinstance(other, type(self))

        def __repr__(self):
            return f"Token.Semicolon()"

        def __str__(self):
            return ";"


class TokenScan:

    words = [
        ("RESTORE", Token.Word(Word.Restore)),
        ("DEFDBL", Token.Word(Word.Defdbl)),
        ("DEFINT", Token.Word(Word.Defint)),
        ("DEFSNG", Token.Word(Word.Defsng)),
        ("DEFSTR", Token.Word(Word.Defstr)),
        ("DELETE", Token.Word(Word.Delete)),
        ("RETURN", Token.Word(Word.Return)),
        ("CLEAR", Token.Word(Word.Clear)),
        ("ERASE", Token.Word(Word.Erase)),
        ("GOSUB", Token.Word(Word.Gosub)),
        ("INPUT", Token.Word(Word.Input)),
        ("PRINT", Token.Word(Word.Print)),
        ("RENUM", Token.Word(Word.Renum)),
        ("TROFF", Token.Word(Word.Troff)),
        ("WHILE", Token.Word(Word.While)),
        ("CONT", Token.Word(Word.Cont)),
        ("DATA", Token.Word(Word.Data)),
        ("ELSE", Token.Word(Word.Else)),
        ("GOTO", Token.Word(Word.Goto)),
        ("NEXT", Token.Word(Word.Next)),
        ("LIST", Token.Word(Word.List)),
        ("LOAD", Token.Word(Word.Load)),
        ("READ", Token.Word(Word.Read)),
        ("SAVE", Token.Word(Word.Save)),
        ("STEP", Token.Word(Word.Step)),
        ("STOP", Token.Word(Word.Stop)),
        ("SWAP", Token.Word(Word.Swap)),
        ("THEN", Token.Word(Word.Then)),
        ("TRON", Token.Word(Word.Tron)),
        ("WEND", Token.Word(Word.Wend)),
        ("AND", Token.Operator(Operator.And)),
        ("CLS", Token.Word(Word.Cls)),
        ("DEF", Token.Word(Word.Def)),
        ("DIM", Token.Word(Word.Dim)),
        ("END", Token.Word(Word.End)),
        ("EQV", Token.Operator(Operator.Eqv)),
        ("FOR", Token.Word(Word.For)),
        ("IMP", Token.Operator(Operator.Imp)),
        ("LET", Token.Word(Word.Let)),
        ("MOD", Token.Operator(Operator.Modulo)),
        ("NEW", Token.Word(Word.New)),
        ("NOT", Token.Operator(Operator.Not)),
        ("REM", Token.Word(Word.Rem1)),
        ("RUN", Token.Word(Word.Run)),
        ("XOR", Token.Operator(Operator.Xor)),
        ("IF", Token.Word(Word.If)),
        ("ON", Token.Word(Word.On)),
        ("OR", Token.Operator(Operator.Or)),
        ("TO", Token.Word(Word.To)),
    ]

    def alphabetic(v: deque[Token], s: str) -> str:
        for word, token in TokenScan.words:
            idx = s.find(word)
            if idx == 0:
                v.append(token)
                s = s[len(word) :]
            if idx > 0:
                v.append(Token.Ident(Ident.Plain(s[:idx])))
                v.append(token)
                s = s[idx + len(word) :]
        return s

    minutia = {
        "(": Token.LParen,
        ")": Token.RParen,
        ",": Token.Comma,
        ":": Token.Colon,
        ";": Token.Semicolon,
        "?": Token.Word(Word.Print),
        "'": Token.Word(Word.Rem2),
        "^": Token.Operator(Operator.Caret),
        "*": Token.Operator(Operator.Multiply),
        "/": Token.Operator(Operator.Divide),
        "\\": Token.Operator(Operator.DivideInt),
        "+": Token.Operator(Operator.Plus),
        "-": Token.Operator(Operator.Minus),
        "=": Token.Operator(Operator.Equal),
        "<": Token.Operator(Operator.Less),
        ">": Token.Operator(Operator.Greater),
    }

    def match_minutia(s: str) -> Token:
        return TokenScan.minutia[s]
