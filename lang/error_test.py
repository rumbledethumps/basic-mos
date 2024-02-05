from lang.error import Error, ErrorCode
import unittest  # The test framework


class Test_TestError(unittest.TestCase):
    def test_printing(self):
        self.assertEqual(str(Error(ErrorCode.Break)), "?BREAK")
        self.assertEqual(
            str(Error(ErrorCode.Break).add_line_number(10)), "?BREAK IN 10"
        )
        self.assertEqual(
            str(Error(ErrorCode.Break).add_line_number(10).add_column(range(5, 10))),
            "?BREAK IN 10:6",
        )
        self.assertEqual(
            str(
                Error(ErrorCode.Break)
                .add_line_number(10)
                .add_column(range(5, 10))
                .add_message("OVERLOAD")
            ),
            "?BREAK IN 10:6; OVERLOAD",
        )


if __name__ == "__main__":
    unittest.main()
