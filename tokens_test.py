from tokens import Token, Word, Operator
import unittest  # The test framework


class Test_TestToken(unittest.TestCase):
    def test_equality(self):
        self.assertEqual(Token.Word(Word.Print), Token.Word(Word.Print))
        self.assertNotEqual(Token.Word(Word.Print), Token.Word(Word.Let))
        self.assertEqual(Token.Word(Word.Print), Token.Word(Word.Print))
        self.assertEqual(Token.LParen(), Token.LParen())
        self.assertEqual(f"{Token.Word(Word.Clear)}", f"{Token.Word(Word.Clear)}")
        self.assertEqual(f"{Token.RParen()}", f"{Token.RParen()}")
        self.assertEqual(f"{Token.Operator(Operator.Multiply)}", f"{Token.Operator(Operator.Multiply)}")


if __name__ == "__main__":
    unittest.main()
