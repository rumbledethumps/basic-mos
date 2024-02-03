from lang.tokens import Token, Word, Operator, Ident, Literal
import unittest  # The test framework


class Test_TestToken(unittest.TestCase):
    def test_equality_of_different_objects(self):
        self.assertNotEqual(Token.Word(Word.Print), Token.Word(Word.Let))
        self.assertEqual(Token.Word(Word.Print), Token.Word(Word.Print))
        self.assertEqual(Token.LParen(), Token.LParen())
        self.assertEqual(f"{Token.Word(Word.Clear)}", f"{Token.Word(Word.Clear)}")
        self.assertEqual(f"{Token.RParen()}", f"{Token.RParen()}")
        self.assertEqual(f"{Token.Operator(Operator.Multiply)}", f"{Token.Operator(Operator.Multiply)}")
        self.assertEqual(f"{Token.Ident(Ident.Single("V1"))}", f"{Token.Ident(Ident.Single("V1"))}")
        self.assertEqual(f"{Token.Literal(Literal.Hex("1A3F"))}", f"{Token.Literal(Literal.Hex("1A3F"))}")


if __name__ == "__main__":
    unittest.main()
