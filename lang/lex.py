import re
from lang.tokens import TokenScan, Token, Literal, Word, Ident, Operator
import lang.line
from collections import deque


class Re:
    line_number = re.compile("^\\s*(\\d+)(?:\\s|)(.*)", flags=re.ASCII)
    whitespace = re.compile("\\s", flags=re.ASCII)
    digit = re.compile("\\d", flags=re.ASCII)
    octal = re.compile("[0-7]", flags=re.ASCII)
    hex = re.compile("[0-9A-Fa-f]", flags=re.ASCII)
    alphabetic = re.compile("[A-Za-z]", flags=re.ASCII)
    not_minutia = re.compile("(?:[A-Za-z]|\\s|\\d)", flags=re.ASCII)


class BasicLexer:
    def __init__(self, chars):
        self.chars = deque(chars)
        self.pending = deque()
        self.remark = False

    def __iter__(self):
        return self

    def __next__(self) -> Token:
        try:
            return self.pending.popleft()
        except IndexError:
            pass
        if self.remark:
            token = Token.Unknown("".join(self.chars))
            self.chars = ""
            if token == Token.Unknown(""):
                raise StopIteration
            return token
        try:
            pk = self.chars[0]
        except IndexError:
            pk = ""
        if Re.whitespace.match(pk):
            return self.whitespace()
        if Re.digit.match(pk):
            return self.number()
        if Re.alphabetic.match(pk):
            token = self.alphabetic()
            if token == Token.Word(Word.Rem1):
                self.remark = True
            return token
        if pk == '"':
            return self.string()
        if pk == "&":
            return self.radix()
        minutia = self.minutia()
        if minutia == Token.Word(Word.Rem2):
            self.remark = True
        if minutia == Token.Unknown(""):
            raise StopIteration
        return minutia

    def whitespace(self) -> Token:
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

    def number(self) -> Token:
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
            if ch in ["E", "D"]:
                exp = True
                if pk in ["+", "-"]:
                    continue
                if not Re.digit.match(pk):
                    exp = False
                    s = s[:-1]
                    self.chars.pushleft(ch)
            if Re.digit.match(pk):
                continue
            if not exp and not decimal and pk == ".":
                continue
            if not exp and pk in ["E", "e", "D", "d"]:
                continue
            if pk in ["!", "#", "%"]:
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

    def alphabetic(self) -> Token:
        s = str()
        digit = False
        while True:
            try:
                ch = self.chars.popleft().upper()
            except IndexError:
                break
            s += ch
            if Re.digit.match(ch):
                digit = True
            if ch == "$":
                self.pending.append(Token.Ident(Ident.String(s)))
                break
            if ch == "!":
                self.pending.append(Token.Ident(Ident.Single(s)))
                break
            if ch == "#":
                self.pending.append(Token.Ident(Ident.Double(s)))
                break
            if ch == "%":
                self.pending.append(Token.Ident(Ident.Integer(s)))
                break
            try:
                pk = self.chars[0]
                if Re.alphabetic.match(pk):
                    if digit:
                        self.pending.append(Token.Ident(Ident.Plain(s)))
                        break
                    continue
                if Re.digit.match(pk) or pk in ["$", "!", "#", "%"]:
                    s = TokenScan.alphabetic(self.pending, s)
                    if s == "":
                        break
                    continue
            except IndexError:
                pass
            s = TokenScan.alphabetic(self.pending, s)
            if s != "":
                self.pending.append(Token.Ident(Ident.Plain(s)))
            break
        return self.pending.popleft()

    def string(self) -> Token:
        s = str()
        self.chars.popleft()
        while True:
            try:
                ch = self.chars.popleft()
                if ch == '"':
                    break
            except IndexError:
                break
            s += ch
        return Token.Literal(Literal.String(s))

    def radix(self) -> Token:
        self.chars.popleft()
        try:
            is_hex = False
            if self.chars[0] in ["h", "H"]:
                self.chars.popleft()
                is_hex = True
        except IndexError:
            pass
        s = str()
        while True:
            try:
                ch = self.chars.popleft()
            except IndexError:
                break
            if Re.octal.match(ch) or (is_hex and Re.hex.match(ch)):
                s += ch.upper()
            else:
                self.chars.appendleft(ch)
                break
        if is_hex:
            return Token.Literal(Literal.Hex(s))
        else:
            return Token.Literal(Literal.Octal(s))

    def minutia(self) -> Token:
        s = str()
        while True:
            try:
                ch = self.chars.popleft()
            except IndexError:
                break
            s += ch
            try:
                return TokenScan.match_minutia(s)
            except KeyError:
                pass
            try:
                pk = self.chars[0]
            except IndexError:
                break
            if Re.not_minutia.match(pk):
                break
        return Token.Unknown(s)


def lex(source_line: str) -> (int, list[Token]):
    line_number = None
    result = Re.line_number.match(source_line)
    if result:
        potential_line_number = int(result.group(1))
        if (
            potential_line_number >= 0
            and potential_line_number <= lang.line.Line.max_number
        ):
            line_number = potential_line_number
            source_line = result.group(2)
    tokens = list(BasicLexer(source_line))
    _trim_end(tokens)
    _collapse_triples(tokens)
    _collapse_doubles(tokens)
    _separate_words(tokens)
    return (line_number, tokens)


def _trim_end(tokens: list[Token]):
    # try code spaces first
    try:
        if type(tokens[-1]) == Token.Whitespace:
            tokens.pop()
    except IndexError:
        pass
    # get spaces in rems too
    try:
        if type(tokens[-1]) == Token.Unknown:
            s = str(tokens.pop()).rstrip()
            tokens.append(Token.Unknown(s))
    except IndexError:
        pass


def _collapse_triples(tokens: list[Token]):
    locs = list()
    for i in range(len(tokens) - 2):
        w0, w1, w2 = tokens[i : i + 3]
        if w0 == Token.Operator(Operator.Less):
            if type(w1) == Token.Whitespace:
                if w2 == Token.Operator(Operator.Greater):
                    locs.append((i, Token.Operator(Operator.NotEqual)))
                if w2 == Token.Operator(Operator.Equal):
                    locs.append((i, Token.Operator(Operator.LessEqual)))
        if w0 == Token.Operator(Operator.Equal):
            if type(w1) == Token.Whitespace:
                if w2 == Token.Operator(Operator.Greater):
                    locs.append((i, Token.Operator(Operator.GreaterEqual)))
                if w2 == Token.Operator(Operator.Less):
                    locs.append((i, Token.Operator(Operator.LessEqual)))
        if w0 == Token.Operator(Operator.Greater):
            if type(w1) == Token.Whitespace:
                if w2 == Token.Operator(Operator.Less):
                    locs.append((i, Token.Operator(Operator.NotEqual)))
                if w2 == Token.Operator(Operator.Equal):
                    locs.append((i, Token.Operator(Operator.GreaterEqual)))
        if str(w0) == "GO":
            if type(w1) == Token.Whitespace:
                if w2 == Token.Word(Word.To):
                    locs.append((i, Token.Word(Word.Goto)))
                if str(w2) == "SUB":
                    locs.append((i, Token.Word(Word.Gosub)))
    for index, token in reversed(locs):
        tokens[index : index + 3] = [token]


def _collapse_doubles(tokens: list[Token]):
    locs = list()
    for i in range(len(tokens) - 1):
        w0, w1 = tokens[i : i + 2]
        if w0 == Token.Operator(Operator.Equal):
            if w1 == Token.Operator(Operator.Greater):
                locs.append((i, Token.Operator(Operator.GreaterEqual)))
            if w1 == Token.Operator(Operator.Less):
                locs.append((i, Token.Operator(Operator.LessEqual)))
        if w1 == Token.Operator(Operator.Equal):
            if w0 == Token.Operator(Operator.Greater):
                locs.append((i, Token.Operator(Operator.GreaterEqual)))
            if w0 == Token.Operator(Operator.Less):
                locs.append((i, Token.Operator(Operator.LessEqual)))
        if w0 == Token.Operator(Operator.Less):
            if w1 == Token.Operator(Operator.Greater):
                locs.append((i, Token.Operator(Operator.NotEqual)))
    for index, token in reversed(locs):
        tokens[index : index + 2] = [token]


def _separate_words(tokens: list[Token]):
    locs = list()
    for i in range(len(tokens) - 1):
        window = tokens[i : i + 2]
        if window[0].is_word() and window[1].is_word():
            locs.append(i)
    for loc in reversed(locs):
        tokens.insert(loc + 1, Token.Whitespace(1))
