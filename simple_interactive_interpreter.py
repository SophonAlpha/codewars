"""
Simple Interactive Interpreter kata:
https://www.codewars.com/kata/simple-interactive-interpreter

useful reading for this kata:
    https://ruslanspivak.com/lsbasi-part1/
    http://web.archive.org/web/20140328000415/http://www.evanfosmark.com:80/2009/02/sexy-lexing-with-python/
    https://tomassetti.me/parsing-in-python/
"""

import re

class Interpreter:
    """
    Implements EBNF:
    
    expr   ::= term ((PLUS | MINUS) term)*
    term   ::= factor ((MUL | DIV) factor)*
    factor ::= NUMBER | L_PAREN epr R_PAREN
    """

    def __init__(self):
        self.vars = {}
        self.functions = {}
        self.lex = Lexer()
        self.current_token = None

    def error(self):
        raise Exception('invalid syntax')

    def input(self, expression):
        self.lex.set_expression(expression)
        self.current_token = self.lex.get_next_token()
        result = self.expr()
        return result

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lex.get_next_token()
        else:
            self.error()

    def expr(self):
        result = self.term()
        while self.current_token.type in ('plus', 'minus'):
            token = self.current_token
            if token.type == 'plus':
                self.eat('plus')
                result = result + self.term()
            elif token.type == 'minus':
                self.eat('minus')
                result = result - self.term()
        return result

    def term(self):
        result = self.factor()
        while self.current_token.type in ('mul', 'div', 'mod'):
            token = self.current_token
            if token.type == 'mul':
                self.eat('mul')
                result = result * self.factor()
            elif token.type == 'div':
                self.eat('div')
                result = result / self.factor()
            elif token.type == 'mod':
                self.eat('mod')
                result = result % self.factor()
        return result

    def factor(self):
        token = self.current_token
        if token.type == 'number':
            self.eat('number')
            return float(token.value)
        elif token.type == 'l_paren':
            self.eat('l_paren')
            result = self.expr()
            self.eat('r_paren')
            return result

class Lexer:
    def __init__(self):
        self.rules = [
            ('fn_keyword', r'\s*fn\s*'),
            ('string', r'\s*[A-Za-z_][A-Za-z0-9_]*\s*'),
            ('fn_operator', r'\s*=>\s*'),
            ('assignment', r'\s*=\s*'),
            ('minus', r'\s*-\s*'),
            ('plus', r'\s*\+\s*'),
            ('mul', r'\s*\*\s*'),
            ('div', r'\s*\/\s*'),
            ('mod', r'\s*\%\s*'),
            ('l_paren', r'\s*\(\s*'),
            ('r_paren', r'\s*\)\s*'),
            ('number', r'\s*[0-9]*\.?[0-9]+\s*')
            ]
        parts = []
        for name, rule in self.rules:
            parts.append("(?P<{}>{})".format(name, rule))
        self.regexec = re.compile("|".join(parts))

    def set_expression(self, expression):
        self.scanner = Scanner(self, expression)

    def get_next_token(self):
        return self.scanner.next()

class Scanner:
    def __init__(self, lexer, expression):
        self.expression = expression
        self.position = 0
        self.lexer = lexer

    def next(self):
        if self.position >= len(self.expression):
            return Token("end of expression", None)
        match = self.lexer.regexec.match(self.expression, self.position)
        self.position = match.end()
        token_type = match.lastgroup
        value = match.group(match.lastgroup).strip()
        return Token(token_type, value)

class Token:
    def __init__(self, token_type, token_value):
        self.type = token_type
        self.value = token_value

interpreter = Interpreter()
print(interpreter.input('7 % 2')) # = 1
print(interpreter.input('7%2')) # = 1
print(interpreter.input('8 % 3')) # = 2
print(interpreter.input('14 + 2 * 3 - 6 / 2')) # = 17
print(interpreter.input('14.34 + 2.237 * 3.901 - 6.018 / 2.0893644')) # = 20.186235220186006
print(interpreter.input('7 + 3 * (10 / (12 / (3 + 1) - 1))')) # = 22
print(interpreter.input('7 + 3 * (10 / (12 / (3 + 1) - 1)) / (2 + 3) - 5 - 3 + (8)')) # = 10
print(interpreter.input('7 + (((3 + 2)))')) # = 12

print(interpreter.input("fn avg x y => (x + y) / 2"))
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
