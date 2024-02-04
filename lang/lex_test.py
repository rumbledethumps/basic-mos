import unittest
from lang.lex import parse
from lang.line import Line
from lang.tokens import Token, Literal, Word, Ident, Operator


class Test_LexParse(unittest.TestCase):
    def test_fori1to99(self):
        line = Line(*parse("fori=1to99"))
        self.assertEqual(str(line), "FOR I=1 TO 99")
        self.assertEqual(line.number, None)
        self.assertEqual(
            line.tokens,
            [
                Token.Word(Word.For),
                Token.Whitespace(1),
                Token.Ident(Ident.Plain("I")),
                Token.Operator(Operator.Equal),
                Token.Literal(Literal.Integer("1")),
                Token.Whitespace(1),
                Token.Word(Word.To),
                Token.Whitespace(1),
                Token.Literal(Literal.Integer("99")),
            ],
        )


if __name__ == "__main__":
    unittest.main()
