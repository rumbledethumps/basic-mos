import re
from lang.tokens import Token
from collections import deque


class Re:
    line_number = re.compile("^\s*(\d+)(?:\s|)(.*)", flags=re.ASCII)
    whitespace = re.compile("\s", flags=re.ASCII)


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


def parse(source_line: str) -> (int, list[Token]):
    line_number = None
    result = Re.line_number.match(source_line)
    if result:
        line_number = int(result.group(1))
        source_line = result.group(2)
    return (line_number, list(BasicLexer(source_line)))
