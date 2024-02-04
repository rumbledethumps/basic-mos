from lang.lex import parse
from lang.line import Line

line = Line(*parse("10 leti= 99"))
print(line)
print(line.number, line.tokens)

line = Line(*parse('A$="Foo"'))
print(line)
print(line.number, line.tokens)

line = Line(*parse("ifA%> =&hff00go sub 10"))
print(line)
print(line.number, line.tokens)

line = Line(*parse("A%=&z ' Comment  "))
print(line)
print(line.number, line.tokens)
