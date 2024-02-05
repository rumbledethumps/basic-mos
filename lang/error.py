from enum import IntEnum, verify, UNIQUE


@verify(UNIQUE)
class ErrorCode(IntEnum):
    Break = 0
    NextWithoutFor = 1
    SyntaxError = 2
    ReturnWithoutGosub = 3
    OutOfData = 4
    IllegalFunctionCall = 5
    Overflow = 6
    OutOfMemory = 7
    UndefinedLine = 8
    SubscriptOutOfRange = 9
    RedimensionedArray = 10
    DivisionByZero = 11
    IllegalDirect = 12
    TypeMismatch = 13
    OutOfStringSpace = 14
    StringTooLong = 15
    CantContinue = 17
    UndefinedUserFunction = 18
    RedoFromStart = 21
    LineBufferOverflow = 23
    ForWithoutNext = 26
    WhileWithoutWend = 29
    WendWithoutWhile = 30
    InternalError = 51
    FileNotFound = 53
    FileAlreadyExists = 58
    BadFileName = 64
    DirectStatementInFile = 66


class Error(Exception):
    def __init__(self, code: ErrorCode):
        self.code = code
        self.line_number = None
        self.column = range(0)
        self.message = str()

    def add_line_number(self, line_number: int | None):
        self.line_number = line_number
        return self

    def add_column(self, column: range):
        self.column = column
        return self

    def add_message(self, message: str):
        self.message = message
        return self

    def __str__(self):
        match self.code:
            case 0:
                code_str = "BREAK"
            case 1:
                code_str = "NEXT WITHOUT FOR"
            case 2:
                code_str = "SYNTAX ERROR"
            case 3:
                code_str = "RETURN WITHOUT GOSUB"
            case 4:
                code_str = "OUT OF DATA"
            case 5:
                code_str = "ILLEGAL FUNCTION CALL"
            case 6:
                code_str = "OVERFLOW"
            case 7:
                code_str = "OUT OF MEMORY"
            case 8:
                code_str = "UNDEFINED LINE"
            case 9:
                code_str = "SUBSCRIPT OUT OF RANGE"
            case 10:
                code_str = "REDIMENSIONED ARRAY"
            case 11:
                code_str = "DIVISION BY ZERO"
            case 12:
                code_str = "ILLEGAL DIRECT"
            case 13:
                code_str = "TYPE MISMATCH"
            case 14:
                code_str = "OUT OF STRING SPACE"
            case 15:
                code_str = "STRING TOO LONG"
            case 16:
                code_str = "STRING FORMULA TOO COMPLEX"
            case 17:
                code_str = "CAN'T CONTINUE"
            case 18:
                code_str = "UNDEFINED USER FUNCTION"
            case 19:
                code_str = "NO RESUME"
            case 20:
                code_str = "RESUME WITHOUT ERROR"
            case 21:
                code_str = "REDO FROM START"
            case 22:
                code_str = "MISSING OPERAND"
            case 23:
                code_str = "LINE BUFFER OVERFLOW"
            case 26:
                code_str = "FOR WITHOUT NEXT"
            case 29:
                code_str = "WHILE WITHOUT WEND"
            case 30:
                code_str = "WEND WITHOUT WHILE"
            case 50:
                code_str = "FIELD OVERFLOW"
            case 51:
                code_str = "INTERNAL ERROR"
            case 52:
                code_str = "BAD FILE NUMBER"
            case 53:
                code_str = "FILE NOT FOUND"
            case 54:
                code_str = "BAD FILE MODE"
            case 55:
                code_str = "FILE ALREADY OPEN"
            case 56:
                code_str = "DISK NOT MOUNTED"
            case 57:
                code_str = "DISK I/O ERROR"
            case 58:
                code_str = "FILE ALREADY EXISTS"
            case 59:
                code_str = "SET TO NON-DISK STRING"
            case 60:
                code_str = "DISK ALREADY MOUNTED"
            case 61:
                code_str = "DISK FULL"
            case 62:
                code_str = "INPUT PAST END"
            case 63:
                code_str = "BAD RECORD NUMBER"
            case 64:
                code_str = "BAD FILE NAME"
            case 65:
                code_str = "MODE-MISMATCH"
            case 66:
                code_str = "DIRECT STATEMENT IN FILE"
            case 67:
                code_str = "TOO MANY FILES"
            case 68:
                code_str = "OUT OF RANDOM BLOCKS"
            case _:
                code_str = str()
        suffix = str()
        if self.line_number:
            suffix += f" {str(self.line_number)}"
            if self.column != range(0):
                suffix += f":{self.column.start+1}"
        if suffix != "":
            suffix = " IN" + suffix
        if self.message != "":
            suffix = suffix + "; " + self.message
        if code_str == "":
            return f"?PROGRAM ERROR {self.code}{suffix}"
        else:
            return f"?{code_str}{suffix}"
