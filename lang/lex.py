import re
from lang.tokens import Token
from collections import deque


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
        except:
            pass

        if self.remark:
            return Token.Unknown(str(self.chars))

        try:
            pk = self.chars[0]
        except:
            pk = ""

        if re.match("\s", pk, flags=re.ASCII):
            self.chars.popleft()
            return Token.Whitespace(2)

        try:
            return self.chars.popleft()
        except IndexError:
            raise StopIteration


def parse(source_line: str) -> (int, list[Token]):
    line_number = None
    result = re.match("^\s*(\d+)(\s|)(.*)", source_line, flags=re.ASCII)
    if result:
        line_number = int(result.group(1))
        source_line = result.group(3)
    return (line_number, list(BasicLexer(source_line)))
