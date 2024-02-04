from lang.lex import lex
from lang.line import Line

line = Line(*lex("10 leti= 99"))
print(line)
print(line.number, line.tokens)

line = Line(*lex('A$="Foo"'))
print(line)
print(line.number, line.tokens)

line = Line(*lex("ifA%> =&hff00go sub 10"))
print(line)
print(line.number, line.tokens)

line = Line(*lex("A%=&z ' Comment  "))
print(line)
print(line.number, line.tokens)
