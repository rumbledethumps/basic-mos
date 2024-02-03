import lex
from line import Line

line = Line(*lex.parse("10 leti= 99"))
print(line)
print(line.number, line.tokens)

line = Line(*lex.parse("fori=1to99"))
print(line)
print(line.number, line.tokens)
