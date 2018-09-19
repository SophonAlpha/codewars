"""

My solution for Simpler Interactive Interpreter kata:
https://www.codewars.com/kata/simpler-interactive-interpreter

Level: 2 kyu

"""

import re
import collections

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
            ('identifier', r'\s*[A-Za-z_][A-Za-z0-9_]*\s*'),
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
        self.expression = expression.strip()
        self.position = 0

    def get_next_token(self):
        if self.position >= len(self.expression):
            return Token("end of expression", None)
        match = self.regexec.match(self.expression, self.position)
        if not match:
            # something is wrong with the input string
            raise Exception('ERROR: Invalid input.')
        self.position = match.end()
        token_type = match.lastgroup
        value = match.group(match.lastgroup).strip()
        value = value if token_type != 'number' else self.handle_number(value)
        return Token(token_type, value)

    def handle_number(self, value):
        try:
            value = int(value)
        except ValueError:
            value = float(value)
        return value

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
        self.value = token.value

class UnaryOp(AST):
    def __init__(self, op, expr):
        self.token = self.op = op
        self.right = expr

class Identifier(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

class VarName(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

class Assign(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right

class Parser():
    """
    Implements EBNF:

    expression     ::= assignment | additive

    assignment     ::= var-name '=' additive

    additive       ::= multiplicative ((PLUS | MINUS) multiplicative)*
    multiplicative ::= factor ((MUL | DIV | MOD) factor)*
    factor         ::= (PLUS | MINUS) factor | NUMBER |
                       assignment | IDENTIFIER |
                       L_PAREN additive R_PAREN

    var-name       ::= IDENTIFIER
    """

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

    def set_expression(self, expression):
        self.lexer.set_expression(expression)
        self.current_token = self.lexer.get_next_token()

    def parse(self):
        node = self.expression()
        if self.current_token.type != 'end of expression':
            # some other stuff is in the input string
            raise Exception('ERROR: Invalid input.')
        return node

    def expression(self):
        """
        expression ::= assignment | additive
        """
        current_token = self.current_token
        next_token = self.lexer.peek()
        if current_token.type == 'identifier' and \
        next_token.type == 'assignment':
            return self.assignment()
        elif current_token.type in ('number', 'identifier', 'l_paren'):
            return self.additive()

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
        factor ::= (PLUS | MINUS) factor | NUMBER |
                   assignment | IDENTIFIER |
                   L_PAREN additive R_PAREN
        """
        current_token = self.current_token
        next_token = self.lexer.peek()
        if current_token.type == 'plus':
            self.eat('plus')
            node = UnaryOp(op=current_token, expr=self.factor())
        elif current_token.type == 'minus':
            self.eat('minus')
            node = UnaryOp(op=current_token, expr=self.factor())
        elif current_token.type == 'number':
            self.eat('number')
            node = Num(current_token)
        elif current_token.type == 'identifier' and next_token.type == 'assignment':
            return self.assignment()
        elif current_token.type == 'identifier':
            return self.identifier()
        elif current_token.type == 'l_paren':
            self.eat('l_paren')
            node = self.additive()
            self.eat('r_paren')
        return node

    def assignment(self):
        """
        assignment ::= var-name '=' additive
        """
        node = Identifier(self.current_token)
        self.eat('identifier')
        op = self.current_token
        self.eat('assignment')
        node = Assign(left=node, op=op, right=self.additive())
        return node

    def identifier(self):
        """
        IDENTIFIER
        """
        node = VarName(self.current_token)
        self.eat('identifier')
        return node

#-------------------------------------------------------------------------------
# abstract syntax tree walker
#-------------------------------------------------------------------------------

class NodeVisitor():
    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception('No visit_{} method'.format(type(node).__name__))

    def visit_NoneType(self, _):
        return ''

#-------------------------------------------------------------------------------
# Variable Table, Semantic Analyser
#-------------------------------------------------------------------------------

class Variable():
    def __init__(self, name, value):
        self.name = name
        self.value = value

class ScopedVarTable():
    def __init__(self):
        self.vars = collections.OrderedDict()

    def insert(self, var):
        self.vars[var.name] = var

    def lookup(self, var_name):
        var = self.vars.get(var_name)
        if not self.vars or not var_name in self.vars.keys():
            # No variables defined.
            raise Exception('ERROR: Invalid identifier. No variable with '
                            'name \'{}\' was found.'.format(var_name))
        return var

    def exists(self, var_name):
        return var_name in self.vars.keys()

class SemanticAnalyser(NodeVisitor):
    def __init__(self):
        self.var_table = ScopedVarTable()
        self.current_scope = self.var_table
        self.functions = {}

    def visit_BinOp(self, node):
        self.visit(node.left)
        self.visit(node.right)

    def visit_Num(self, node):
        pass

    def visit_UnaryOp(self, node):
        self.visit(node.right)

    def visit_VarName(self, node):
        self.current_scope.lookup(node.value)

    def visit_Assign(self, node):
        var_name = node.left.value
        if var_name in self.functions.keys():
            raise Exception('ERROR: Variable name \'{}\' already defined as '
                            'function name.'.format(var_name))
        var_value = self.visit(node.right)
        var = Variable(name=var_name, value=var_value)
        self.current_scope.insert(var)

#-------------------------------------------------------------------------------
# Interpreter
#-------------------------------------------------------------------------------

class Interpreter(NodeVisitor):
    def __init__(self):
        self.var_table = ScopedVarTable()
        self.current_scope = self.var_table
        self.functions = {}
        self.lexer = Lexer()
        self.parser = Parser(self.lexer)
        self.semantic_analyser = SemanticAnalyser()

    def input(self, expression):
        self.parser.set_expression(expression)
        tree = self.parser.parse()
        self.semantic_analyser.visit(tree)
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

    def visit_VarName(self, node):
        var = self.current_scope.lookup(node.value)
        return var.value

    def visit_Assign(self, node):
        var = Variable(name=node.left.value, value=self.visit(node.right))
        self.current_scope.insert(var)
        return var.value
