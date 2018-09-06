"""
Simple Interactive Interpreter kata:
https://www.codewars.com/kata/simple-interactive-interpreter

good introduction to building an interpreter, was very helpful learning for this kata:
https://ruslanspivak.com/lsbasi-part1/

    Implements EBNF:

    expression     ::= function | assignment | additive
    additive       ::= multiplicative ((PLUS | MINUS) multiplicative)*
    multiplicative ::= factor ((MUL | DIV | MOD) factor)*
    factor         ::= (PLUS | MINUS) factor | NUMBER | assignment | IDENTIFIER | L_PAREN additive R_PAREN | function-call
    assignment     ::= IDENTIFIER '=' additive
    function       ::= fn-keyword fn-name { identifier } fn-operator expression
    fn-name        ::= identifier
    fn-operator    ::= '=>'
    fn-keyword     ::= 'fn'
"""

import re
import collections

class Symbol():
    def __init__(self, name, type=None):
        self.name = name
        self.type = type

class BuiltinTypeSymbol(Symbol):
    def __init__(self, name):
        super(BuiltinTypeSymbol, self).__init__(name)

class VarSymbol(Symbol):
    def __init__(self, name, type):
        super(VarSymbol, self).__init__(name, type)

class SymbolTable():
    def __init__(self):
        self._symbols = collections.OrderedDict()
    
    def define(self, symbol):
        self._symbols[symbol.name] = symbol
    
    def lookup(self, name):
        return self._symbols[name]

#-------------------------------------------------------------------------------
# Lexer
#-------------------------------------------------------------------------------

class Token:
    def __init__(self, token_type, token_value):
        self.type = token_type
        self.value = token_value

class Lexer:
    def __init__(self):
        self.rules = [
            ('fn_keyword', r'\s*fn\s*'),
            ('identifier', r'\s*[A-Za-z_][A-Za-z0-9_]*\s*'),
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
        self.expression = None
        self.position = 0

    def set_expression(self, expression):
        self.expression = expression
        self.position = 0

    def get_next_token(self):
        if self.position >= len(self.expression):
            return Token("end of expression", None)
        match = self.regexec.match(self.expression, self.position)
        self.position = match.end()
        token_type = match.lastgroup
        value = match.group(match.lastgroup).strip()
        return Token(token_type, value)

    def peek(self):
        if self.position >= len(self.expression):
            return Token("end of expression", None)
        match = self.regexec.match(self.expression, self.position)
        token_type = match.lastgroup
        value = match.group(match.lastgroup).strip()
        return Token(token_type, value)

#-------------------------------------------------------------------------------
# Parser
#-------------------------------------------------------------------------------

class AST():
    pass

class BinOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right

class Num(AST):
    def __init__(self, token):
        self.token = token
        self.value = float(token.value)
        
class UnaryOp(AST):
    def __init__(self, op, right):
        self.token = self.op = op
        self.right = right

class Parser():
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = None

    def error(self):
        raise Exception('invalid syntax')

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def expression(self):
        """
        expression ::= function | assignment | additive
        """
        self.current_token = self.lexer.get_next_token() # read the very first token
        current_token = self.current_token
        next_token = self.lexer.peek()
        if current_token.type == 'fn_keyword':
            return self.function()
        elif current_token.type == 'identifier' and next_token.type == 'assignment':
            # TODO: move variable creation to separate function
            var_name = current_token.value
            self.eat('identifier')
            self.eat('assignment')
            var_value = self.expression()
            result = self.create_var(var_name, var_value)
            return result
        elif current_token.type in ('number', 'identifier', 'l_paren'):
            result = self.additive()
        return result

    def additive(self):
        """
        additive ::= multiplicative ((PLUS | MINUS) multiplicative)*
        """
        node = self.multiplicative()
        while self.current_token.type in ('plus', 'minus'):
            token = self.current_token
            if token.type == 'plus':
                self.eat('plus')
            elif token.type == 'minus':
                self.eat('minus')
            node = BinOp(left=node, op=token, right=self.multiplicative())
        return node

    def multiplicative(self):
        """
        multiplicative ::= factor ((MUL | DIV | MOD) factor)*
        """
        node = self.factor()
        while self.current_token.type in ('mul', 'div', 'mod'):
            token = self.current_token
            if token.type == 'mul':
                self.eat('mul')
            elif token.type == 'div':
                self.eat('div')
            elif token.type == 'mod':
                self.eat('mod')
            node = BinOp(left=node, op=token, right=self.factor())
        return node

    def factor(self):
        """
        factor ::= (PLUS | MINUS) factor | NUMBER | assignment | IDENTIFIER | 
                   L_PAREN additive R_PAREN | function-call
        """
        current_token = self.current_token
        next_token = self.lexer.peek()
        if current_token.type == 'plus':
            self.eat('plus')
            node = UnaryOp(op=current_token, right=self.factor())
        elif current_token.type == 'minus':
            self.eat('minus')
            node = UnaryOp(op=current_token, right=self.factor())
        elif current_token.type == 'number':
            self.eat('number')
            node = Num(current_token)
        elif current_token.type == 'identifier' and next_token.type == 'assignment':
            var_name = current_token.value
            self.eat('identifier')
            self.eat('assignment')
            var_value = self.expression()
            result = self.create_var(var_name, var_value)
            return result
        elif current_token.type == 'identifier':
            self.eat('identifier')
#             return self.vars[current_token.value]
        elif current_token.type == 'l_paren':
            self.eat('l_paren')
            node = self.additive()
            self.eat('r_paren')
        return node

    def function(self):
        """
        function ::= fn-keyword fn-name { identifier } fn-operator expression
        """
        self.eat('fn_keyword')
        fn_name = self.current_token
        self.eat('identifier')
        self.eat('fn_operator')
        fn_vars = {}
        while self.current_token.type == 'identifier':
            fn_vars[self.current_token] = None
        self.eat('fn_operator')

    def create_var(self, var_name, var_value):
#         self.vars[var_name] = var_value
        return var_value

#-------------------------------------------------------------------------------
# Interpreter
#-------------------------------------------------------------------------------

class NodeVisitor():
    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)
    
    def generic_visit(self, node):
        raise Exception('No visit_{} method'.format(type(node).__name__))

class Interpreter(NodeVisitor):
    def __init__(self):
        self.lexer = Lexer()
        self.parser = Parser(self.lexer)

    def input(self, expression):
        self.lexer.set_expression(expression)
        tree = self.parser.expression()
        result = self.visit(tree)
        return result
    
    def visit_BinOp(self, node):
        if node.op.type == 'plus':
            return self.visit(node.left) + self.visit(node.right)
        elif node.op.type == 'minus':
            return self.visit(node.left) - self.visit(node.right)
        elif node.op.type == 'mul':
            return self.visit(node.left) * self.visit(node.right)
        elif node.op.type == 'div':
            return self.visit(node.left) / self.visit(node.right)
        elif node.op.type == 'mod':
            return self.visit(node.left) % self.visit(node.right)

    def visit_Num(self, node):
        return node.value
    
    def visit_UnaryOp(self, node):
        if node.op.type == 'plus':
            return +self.visit(node.right)
        elif node.op.type == 'minus':
            return -self.visit(node.right)

#-------------------------------------------------------------------------------
# Main
#-------------------------------------------------------------------------------

interpreter = Interpreter()

print(interpreter.input('5 - - - 2')) # 3

print(interpreter.input('2 * 7 + 3')) # 17
print(interpreter.input('2 * (7 + 3)')) # 20
print(interpreter.input('7 + 3 * (10 / (12 / (3 + 1) - 1))')) # 22
print(interpreter.input('7 + 3 * (10 / (12 / (3 + 1) - 1)) / (2 + 3) - 5 - 3 + (8)')) # 10
print(interpreter.input('7 + (((3 + 2)))')) # 12
print(interpreter.input('7 + 3')) # 10

print(interpreter.input('b = 8'))
print(interpreter.input('a + b'))
print(interpreter.input('first_var = 14 + 2 * 3 - 6 / 2')) # = 17
print(interpreter.input('second_var = 7 + 3 * (10 / (12 / (3 + 1) - 1))')) # = 22
print(interpreter.input('7 + 3 * (10 / (12 / (3 + first_var) - 1)) / (2 + 3) - 5 - second_var + (8)')) # = -27
print(interpreter.input('a = b = 12')) # = 12
print(interpreter.input('x = 13 + (y = 3)')) # = 16

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
