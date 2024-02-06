from lang.ast import Statement, Variable, Expression, Ident
from lang.error import Error, ErrorCode
from lang.line import Line
from lang.lex import lex
import unittest


class Test_TestParse(unittest.TestCase):
    def test_equality_of_different_objects(self):
        line = Line(*lex("A%=1234 ' Comment "))
        self.assertEqual(
            [
                Statement.Let(
                    range(0, 2),
                    Variable.Unary(range(0, 2), Ident.Integer("A%")),
                    Expression.Integer(range(3, 7), 1234),
                )
            ],
            line.ast(),
        )


if __name__ == "__main__":
    unittest.main()
