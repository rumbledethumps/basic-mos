class Token:
    def __str__(self):
        if hasattr(self, "printable_text"):
            return self.printable_text
        else:
            return self.token_text


class Word(Token):
    def __init__(self, text):
        self.token_text = text
        if text == "?":
            self.printable_text = "print"


class Operator(Token):
    def __init__(self, text):
        self.token_text = text


class LParen(Token):
    def __init__(self, text):
        self.token_text = text


class RParen:
    def __init__(self, text):
        self.token_text = text


class Comma:
    def __init__(self, text):
        self.token_text = text


class Colon:
    def __init__(self, text):
        self.token_text = text


class Semicolon:
    def __init__(self, text):
        self.token_text = text


tokens_alpha = [
    Word("RESTORE"),
    Word("DEFDBL"),
    Word("DEFINT"),
    Word("DEFSNG"),
    Word("DEFSTR"),
    Word("DELETE"),
    Word("RETURN"),
    Word("CLEAR"),
    Word("ERASE"),
    Word("GOSUB"),
    Word("INPUT"),
    Word("PRINT"),
    Word("RENUM"),
    Word("TROFF"),
    Word("WHILE"),
    Word("CONT"),
    Word("DATA"),
    Word("ELSE"),
    Word("GOTO"),
    Word("NEXT"),
    Word("LIST"),
    Word("LOAD"),
    Word("READ"),
    Word("SAVE"),
    Word("STEP"),
    Word("STOP"),
    Word("SWAP"),
    Word("THEN"),
    Word("TRON"),
    Word("WEND"),
    Operator("AND"),
    Word("CLS"),
    Word("DEF"),
    Word("DIM"),
    Word("END"),
    Operator("EQV"),
    Word("FOR"),
    Operator("IMP"),
    Word("LET"),
    Operator("MOD"),
    Word("NEW"),
    Operator("NOT"),
    Word("REM"),
    Word("RUN"),
    Operator("XOR"),
    Word("IF"),
    Word("ON"),
    Operator("OR"),
    Word("TO"),
]

tokens_minutia = [
    LParen("("),
    RParen(")"),
    Comma(","),
    Colon(":"),
    Semicolon(";"),
    Word("?"),
    Word("'"),
    Operator("^"),
    Operator("*"),
    Operator("/"),
    Operator("\\"),
    Operator("+"),
    Operator("-"),
    Operator("="),
    Operator("<"),
    Operator(">"),
]


print(next(x for x in tokens_minutia if x.token_text == "?"))
