"""

My solution for The Lift kata:
https://www.codewars.com/kata/tiny-three-pass-compiler

Level: 1 kyu

"""

import re

def simulate(asm, argv):
    r0, r1 = None, None
    stack = []
    for ins in asm:
        if ins[:2] == 'IM' or ins[:2] == 'AR':
            ins, n = ins[:2], int(ins[2:])
        if ins == 'IM':   r0 = n
        elif ins == 'AR': r0 = argv[n]
        elif ins == 'SW': r0, r1 = r1, r0
        elif ins == 'PU': stack.append(r0)
        elif ins == 'PO': r0 = stack.pop()
        elif ins == 'AD': r0 += r1
        elif ins == 'SU': r0 -= r1
        elif ins == 'MU': r0 *= r1
        elif ins == 'DI': r0 /= r1
    return r0

class Token:

    def __init__(self, token_type, token_value):
        self.type = token_type
        self.value = token_value

class Parser:
    """
    Parser for EBNF:
    
    function   ::= '[' arg-list ']' expression

    arg-list   ::= /* nothing */
                   | variable arg-list

    expression ::= term (( '+' | '-' ) term)*

    term       ::= factor (( '*' | '/' ) factor)*

    factor     ::= number
                   | variable
                   | '(' expression ')'
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
        ast = self.function()
        return ast
    
    def function(self):
        if self.current_token.type == 'L_BRACK':
            self.eat('L_BRACK')
            self.arg_list()
            self.eat('R_BRACK')
            ast = self.expression()
        return ast
    
    def arg_list(self):
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
            ast = {'op': op, 'a': ast, 'b': self.term()}
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
            ast = {'op': op, 'a': ast, 'b': self.factor()}
        return ast
    
    def factor(self):
        """
        factor ::= number
                   | variable
                   | '(' expression ')'
        """
        if self.current_token.type == 'NUM':
            ast = {'op': 'imm', 'n': self.current_token.value}
            self.eat('NUM')
            return ast
        elif self.current_token.type == 'VAR':
            ast = {'op': 'arg', 'n': self.var_list.index(self.current_token.value)}
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
        tokens = [Token(m.lastgroup, int(m.group(0)) if m.group(0).isdigit() else m.group(0))
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
        pass

    def pass3(self, ast):
        """Returns assembly instructions"""
        pass

if __name__ == "__main__":
    pass
