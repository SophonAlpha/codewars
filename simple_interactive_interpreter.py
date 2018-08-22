"""
Simple Interactive Interpreter kata:
https://www.codewars.com/kata/simple-interactive-interpreter

useful reading for this kata:
    https://ruslanspivak.com/lsbasi-part1/
    http://web.archive.org/web/20140328000415/http://www.evanfosmark.com:80/2009/02/sexy-lexing-with-python/
    https://tomassetti.me/parsing-in-python/
"""

import re

def tokenize(expression):
    if expression == "":
        return []

    regex = re.compile(r"""\s*                       # any white spaces
                           (=>|                      # the function operator
                            [-+*\/\%=\(\)]|          # all the math operators
                            [A-Za-z_][A-Za-z0-9_]*|  # names (variables and functions)
                            [0-9]*\.?[0-9]+)         # numbers
                           \s*                       # any white spaces""", re.VERBOSE)
    tokens = regex.findall(expression)
    return [s for s in tokens if not s.isspace()]
        
class Lexer:
    def __init__(self, text):
        self.text = text
        self.position = 0
        self.rules = [
            ("string",  r"\s*[A-Za-z_][A-Za-z0-9_]*\s*"),
            ("fn_operator", r"\s*=>\s*"),
            ("assignment",  r"\s*=\s*"),
            ("operator", r"\s*[-+*\/\%]\s*"),
            ("open_bracket", r"\s*\(\s*"),
            ("close_bracket", r"\s*\)\s*"),
            ("number", r"\s*[0-9]*\.?[0-9]+\s*")
            ]
        parts = []
        for name, rule in self.rules:
            parts.append("(?P<{}>{})".format(name, rule))
        self.regexec = re.compile("|".join(parts))

    def __iter__(self):
        return self

    def __next__(self):
        if self.position >= len(self.text):
            raise StopIteration
        match = self.regexec.match(self.text, self.position)
        self.position = match.end()
        token_type = match.lastgroup
        value = match.group(match.lastgroup).strip()
        return token_type, value

class Interpreter:
    def __init__(self):
        self.vars = {}
        self.functions = {}

    def input(self, expression):
        tokens = tokenize(expression)
        print(tokens)

lex = Lexer("fn avg x y => (x + y) / 2")
for token in lex:
    print(token)



# interpreter = Interpreter()
# 
# print(interpreter.input("fn avg x y => (x + y) / 2"))
# 
# # Basic arithmetic
# assert interpreter.input("1 + 1"), 2
# assert interpreter.input("2 - 1"), 1
# assert interpreter.input("2 * 3"), 6
# assert interpreter.input("8 / 4"), 2
# assert interpreter.input("7 % 4"), 3
# 
# # Variables
# assert interpreter.input("x = 1"), 1
# assert interpreter.input("x"), 1
# assert interpreter.input("x + 3"), 4
# print(interpreter.input("y"))
# 
# # Functions
# print(interpreter.input("fn avg x y => (x + y) / 2"))
# assert interpreter.input("avg 4 2"), 3
# print(interpreter.input("avg 7"))
# print(interpreter.input("avg 7 2 4"))
# 
# # Conflicts
# print(interpreter.input("fn x => 0"))
# print(interpreter.input("avg = 5"))
