import re
import tokens


class Line:
    pass


def parse(source_line):
    line = Line()
    result = re.match("^\b*(\d+)(\b)(.*)", source_line, flags=re.ASCII)
    if result:
        line.number = int(result.group(1))
        source_line = result.group(3)
    print(result, line, source_line)
    return line
