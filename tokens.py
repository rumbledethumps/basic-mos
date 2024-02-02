from enum import Enum, auto, verify, UNIQUE


@verify(UNIQUE)
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


@verify(UNIQUE)
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


class Token:
    class Base:
        pass

    class Word(Base):
        def __init__(self, word: Word):
            self.word = word

        def __eq__(self, other):
            if not isinstance(other, Token.Word):
                return False
            return self.word == other.word

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

    class Operator(Base):
        def __init__(self, operator: Operator):
            self.operator = operator

        def __eq__(self, other):
            if not isinstance(other, Token.Operator):
                return False
            return self.operator == other.operator

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

    class LParen(Base):
        def __eq__(self, other):
            return isinstance(other, Token.LParen)

        def __str__(self):
            return "("

    class RParen(Base):
        def __eq__(self, other):
            return isinstance(other, Token.RParen)

        def __str__(self):
            return ")"

    class Comma(Base):
        def __eq__(self, other):
            return isinstance(other, Token.Comma)

        def __str__(self):
            return ","

    class Colon(Base):
        def __eq__(self, other):
            return isinstance(other, Token.Colon)

        def __str__(self):
            return ":"

    class Semicolon(Base):
        def __eq__(self, other):
            return isinstance(other, Token.Semicolon)

        def __str__(self):
            return ";"
