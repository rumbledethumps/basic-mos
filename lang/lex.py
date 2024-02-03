import re
from lang.tokens import Token, Literal
from collections import deque


class Re:
    line_number = re.compile("^\s*(\d+)(?:\s|)(.*)", flags=re.ASCII)
    whitespace = re.compile("\s", flags=re.ASCII)
    digit = re.compile("\d", flags=re.ASCII)


class BasicLexer:
    def __init__(self, chars):
        self.chars = deque(chars)
        self.pending = deque()
        self.remark = False

    def __iter__(self):
        return self

    def __next__(self):
        try:
            return self.pending.popleft()
        except IndexError:
            pass

        if self.remark:
            return Token.Unknown(str(self.chars))

        try:
            pk = self.chars[0]
        except IndexError:
            pk = ""

        if Re.whitespace.match(pk):
            return self.whitespace()

        if Re.digit.match(pk):
            return self.number()

        try:
            return self.chars.popleft()
        except IndexError:
            raise StopIteration

    def whitespace(self):
        length = 0
        while True:
            self.chars.popleft()
            length += 1

            try:
                if Re.whitespace.match(self.chars[0]):
                    continue
            except IndexError:
                pass
            return Token.Whitespace(length)

    def number(self):
        s = str()
        digits = 0
        decimal = False
        exp = False
        while True:
            try:
                ch = self.chars.popleft()
            except IndexError:
                break
            if ch == "e":
                ch = "E"
            if ch == "d":
                ch = "D"
            s += ch
            if not exp and Re.digit.match(ch):
                digits += 1
            if ch == ".":
                decimal = True
            if ch == "D":
                digits += 8
            if ch == "!":
                return Token.Literal(Literal.Single(s))
            if ch == "#":
                return Token.Literal(Literal.Double(s))
            if ch == "%":
                return Token.Literal(Literal.Integer(s))
            try:
                pk = self.chars[0]
            except IndexError:
                continue
            if ch == "E" or ch == "D":
                exp = True
                if pk == "+" or pk == "-":
                    continue
                if not Re.digit.match(pk):
                    exp = False
                    s = s[:-1]
                    self.chars.pushleft(ch)
            if Re.digit.match(pk):
                continue
            if not exp and not decimal and pk == ".":
                continue
            if not exp and (pk == "E" or pk == "e" or pk == "D" or pk == "d"):
                continue
            if pk == "!" or pk == "#" or pk == "%":
                continue
            break
        if digits > 7:
            return Token.Literal(Literal.Double(s))
        try:
            i = int(s)
            if i <= 32767 and i >= -32768 and str(i) == s:
                return Token.Literal(Literal.Integer(s))
        except:
            pass
        return Token.Literal(Literal.Single(s))


def parse(source_line: str) -> (int, list[Token]):
    line_number = None
    result = Re.line_number.match(source_line)
    if result:
        line_number = int(result.group(1))
        source_line = result.group(2)
    return (line_number, list(BasicLexer(source_line)))
