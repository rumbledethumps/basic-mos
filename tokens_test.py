import tokens  # The code to test
import unittest  # The test framework


class Test_TestTokenOverrides(unittest.TestCase):
    def test_print_statement_override(self):
        token = next(x for x in tokens.tokens_minutia if x.token_text == "?")
        self.assertEqual(f"{token}", "print")


if __name__ == "__main__":
    unittest.main()
