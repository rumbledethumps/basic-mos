from lang.lex import parse
from lang.line import Line

line = Line(*parse("10 leti= 99"))
print(line)
print(line.number, line.tokens)

line = Line(*parse("fori=1to99"))
print(line)
print(line.number, line.tokens)
