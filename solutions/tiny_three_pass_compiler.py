"""

My solution for The Lift kata:
https://www.codewars.com/kata/tiny-three-pass-compiler

Level: 1 kyu

"""

import re

class Token:

    def __init__(self, token_type, token_value):
        self.type = token_type
        self.value = token_value

class AST():
    pass

class BinOp(AST):
    def __init__(self, op, a, b):
        self.op = op
        self.a = a
        self.b = b
        
    def JSON(self):
        return {'op': self.op, 'a': self.a.JSON(), 'b': self.b.JSON()}

class Num(AST):
    def __init__(self, op, n):
        self.op = op
        self.n = n
        
    def JSON(self):
        return {'op': 'imm', 'n': self.n}

class Var(AST):
    def __init__(self, op, n):
        self.op = op
        self.n = n
        
    def JSON(self):
        return {'op': 'arg', 'n': self.n}

class Parser:
    """
    Parser for EBNF:
    
    function   ::= '[' arg-list ']' expression

    arg-list   ::= /* nothing */ | variable arg-list

    expression ::= term (( '+' | '-' ) term)*

    term       ::= factor (( '*' | '/' ) factor)*

    factor     ::= number | variable | '(' expression ')'
    """
    
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = None
        self.position = 0
        self.var_list = []
    
    def error(self):
        raise Exception('invalid syntax')
    
    def eat(self, token):
        if self.current_token.type == token:
            self.current_token = self.get_next_token()
        else:
            self.error()
            
    def get_next_token(self):
        if self.position >= len(self.tokens):
            return Token('end of expression', None)
        token = self.tokens[self.position]
        self.position += 1
        return token
    
    def peek(self):
        if self.position >= len(self.tokens):
            return Token('end of expression', None)
        token = self.tokens[self.position]
        return token

    def parse(self):
        self.current_token = self.get_next_token()
        ast = self.function().JSON()
        return ast
    
    def function(self):
        """
        function ::= '[' arg-list ']' expression
        """
        if self.current_token.type == 'L_BRACK':
            self.eat('L_BRACK')
            self.arg_list()
            self.eat('R_BRACK')
            ast = self.expression()
        return ast
    
    def arg_list(self):
        """
        arg-list ::= /* nothing */ | variable arg-list
        """
        while self.current_token.type == 'VAR':
            self.var_list.append(self.current_token.value)
            self.eat('VAR')
        return
    
    def expression(self):
        """
        expression ::= term (( '+' | '-' ) term)*
        """
        ast = self.term()
        while self.current_token.type in ['PLUS', 'MINUS']:
            if self.current_token.type == 'PLUS':
                self.eat('PLUS')
                op = '+'
            elif self.current_token.type == 'MINUS':
                self.eat('MINUS')
                op = '-'
            ast = BinOp(op, ast, self.term())
        return ast
    
    def term(self):
        """
        term ::= factor (( '*' | '/' ) factor)*
        """
        ast = self.factor()
        while self.current_token.type in ['MUL', 'DIV']:
            if self.current_token.type == 'MUL':
                self.eat('MUL')
                op = '*'
            elif self.current_token.type == 'DIV':
                self.eat('DIV')
                op = '/'
            ast = BinOp(op, ast, self.factor())
        return ast
    
    def factor(self):
        """
        factor ::= number | variable | '(' expression ')'
        """
        if self.current_token.type == 'NUM':
            ast = Num('imm', self.current_token.value)
            self.eat('NUM')
            return ast
        elif self.current_token.type == 'VAR':
            ast = Var('arg', self.var_list.index(self.current_token.value))
            self.eat('VAR')
            return ast
        elif self.current_token.type == 'L_PAREN':
            self.eat('L_PAREN')
            ast = self.expression()
            self.eat('R_PAREN')
            return ast

class Compiler(object):
    
    def compile(self, program):
        return self.pass3(self.pass2(self.pass1(program)))
        
    def tokenize(self, program):
        """Turn a program string into an array of tokens.  Each token
           is either '[', ']', '(', ')', '+', '-', '*', '/', a variable
           name or a number (as a string)"""
        patterns  = re.compile(r'(?P<MINUS>-)'
                               r'|(?P<PLUS>\+)'
                               r'|(?P<MUL>\*)'
                               r'|(?P<DIV>/)'
                               r'|(?P<L_BRACK>\[)'
                               r'|(?P<R_BRACK>\])'
                               r'|(?P<L_PAREN>\()'
                               r'|(?P<R_PAREN>\))'
                               r'|(?P<VAR>)[A-Za-z]+'
                               r'|(?P<NUM>)\d+')
        tokens = [Token(m.lastgroup,
                        int(m.group(0)) if m.group(0).isdigit() else m.group(0))
                  for m in patterns.finditer(program)]
        return tokens

    def pass1(self, program):
        """Returns an un-optimized AST"""
        tokens = self.tokenize(program)
        parser = Parser(tokens)
        ast = parser.parse()
        return ast
        
    def pass2(self, ast):
        """Returns an AST with constant expressions reduced"""
        ast = reduce(ast)
        return ast

    def pass3(self, ast):
        """Returns assembly instructions"""
        asm = assembly(ast)
        return asm

def reduce(ast):
    for _, v in ast.items():
        if v in ['+', '-', '*', '/']:
            a = reduce(ast['a'])
            b = reduce(ast['b'])
            if a['op'] == 'imm' and b['op'] == 'imm':
                if v == '+':
                    return {'op': 'imm', 'n': a['n'] + b['n']}
                if v == '-':
                    return {'op': 'imm', 'n': a['n'] - b['n']}
                if v == '*':
                    return {'op': 'imm', 'n': a['n'] * b['n']}
                if v == '/':
                    return {'op': 'imm', 'n': a['n'] / b['n']}
            ast['a'] = a
            ast['b'] = b
    return ast

def assembly(ast):
    op_asm_map = {'+': 'AD',
                  '-': 'SU',
                  '*': 'MU',
                  '/': 'DI'}
    for _, v in ast.items():
        if v in op_asm_map.keys():
            a = assembly(ast['a'])
            b = assembly(ast['b'])
            return a + ['PU'] + b + ['SW'] + ['PO'] + [op_asm_map[v]]
        if v == 'imm':
            return ['IM {}'.format(ast['n'])]
        if v == 'arg':
            return ['AR {}'.format(ast['n'])]

if __name__ == "__main__":
    pass
