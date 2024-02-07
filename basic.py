from lang.lex import lex
from lang.line import Line

line = Line(*lex("10 leti= 99"))
print(line)
print(line.number, line.tokens)
print(line.ast())

line = Line(*lex('A$="Foo"'))
print(line)
print(line.number, line.tokens)
print(line.ast())

line = Line(*lex("ifA%> =&hff00go to 10"))
print(line)
print(line.number, line.tokens)
print(line.ast())

line = Line(*lex("A%=&1234 ' Comment "))
print(line)
print(line.number, line.tokens)
print(line.ast())
