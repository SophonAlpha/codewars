"""

My solution for Simple Interactive Interpreter kata:
https://www.codewars.com/kata/simple-interactive-interpreter

Level: 1 kyu

Good introduction to building an interpreter, was very helpful learning for this kata:
https://ruslanspivak.com/lsbasi-part1/

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

class FuncName(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value
        
class FuncCall():
    def __init__(self, fn_name, fn_params):
        self.fn_name = fn_name
        self.fn_params = {var: None for var in fn_params}

class Function(AST):
    def __init__(self, op, fn_name, fn_vars, expr):
        self.token = op
        self.fn_name = fn_name
        self.fn_vars = collections.OrderedDict({var: None for var in fn_vars})
        self.expr = expr

class Assign(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right

class Parser():
    """
    Implements EBNF:

    expression     ::= function | assignment | additive

    function       ::= fn-keyword fn-name { var-table-name } fn-operator additive

    assignment     ::= var-table-name '=' additive

    additive       ::= multiplicative ((PLUS | MINUS) multiplicative)*
    multiplicative ::= factor ((MUL | DIV | MOD) factor)*
    factor         ::= (PLUS | MINUS) factor | NUMBER | 
                       assignment | IDENTIFIER | 
                       L_PAREN additive R_PAREN | function-call

    function-call  ::= fn-name { additive }

    var-table-name ::= IDENTIFIER
    fn-name        ::= IDENTIFIER
    fn-operator    ::= '=>'
    fn-keyword     ::= 'fn'

    """
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = None
        self.functions = [] # keep track of functions, required to differentiate
                            # between variables and function calls

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

    def expression(self):
        """
        expression ::= function | assignment | additive
        """
        current_token = self.current_token
        next_token = self.lexer.peek()
        if current_token.type == 'fn_keyword':
            return self.function()
        elif current_token.type == 'identifier' and next_token.type == 'assignment':
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
                   L_PAREN additive R_PAREN | function-call
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

    def function(self):
        """
        function ::= fn-keyword fn-name { var_table-name } fn-operator additive
        """
        op = self.current_token
        self.eat('fn_keyword')
        node = Identifier(self.current_token)
        self.functions.append(node.value)
        self.eat('identifier')
        fn_vars = []
        while self.current_token.type == 'identifier':
            fn_vars.append(self.current_token.value)
            self.eat('identifier')
        self.eat('fn_operator')
        node = Function(op, fn_name=node, fn_vars=fn_vars, expr=self.additive())
        return node

    def assignment(self):
        """
        assignment ::= var-table-name '=' additive
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
        
        Checks whether 'identifier' points to a variable or function name.
        """
        # TODO: Check how others figured out during parsing whether an 
        #       identifier is a variable or a function call.
        if self.current_token.value in self.functions:
            node = self.function_call()
        else:
            node = VarName(self.current_token)
            self.eat('identifier')
        return node
    
    def function_call(self):
        """
        function-call ::= fn-name { additive }
        """
        node = FuncName(self.current_token)
        self.eat('identifier')
        fn_params = []
        while self.current_token.type in ('number', 'identifier', 'l_paren'):
            fn_params.append(self.additive())
        node = FuncCall(fn_name=node, fn_params=fn_params)
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

#-------------------------------------------------------------------------------
# Variable Table, Semantic Analyser
#-------------------------------------------------------------------------------

class Variable():
    def __init__(self, name, value):
        self.name = name
        self.value = value

class ScopedVarTable():
    def __init__(self, scope_name, enclosing_scope=None):
        self.vars = collections.OrderedDict()
        self.scope_name = scope_name
        self.enclosing_scope = enclosing_scope
        
    def insert(self, var):
        self.vars[var.name] = var
    
    def lookup(self, var_name):
        var = self.vars.get(var_name)
        if not self.vars and \
           not self.scope_name == 'global':
            # No function parameter variables defined but variables in
            # function body
            raise Exception('ERROR: Unknown identifier \'{}\''.format(var_name))
        elif self.vars and \
             not var_name in self.vars.keys() and \
             not self.scope_name == 'global':
            # Function parameter variables do not match variables used in 
            # function body.
            raise Exception('ERROR: Invalid identifier \'{}\' in function body.'.format(var_name))
        if not self.vars and self.scope_name == 'global':
            # No variables defined.
            raise Exception('ERROR: Invalid identifier. No variable with name \'{}\' was found.'.format(var_name))
        return var

class SemanticAnalyser(NodeVisitor):
    def __init__(self):
        self.var_table = ScopedVarTable('global')
        self.current_scope = self.var_table
        self.functions = {}

    def visit_BinOp(self, node):
        self.visit(node.left)
        self.visit(node.right)

    def visit_Num(self, node):
        pass

    def visit_UnaryOp(self, node):
        self.visit(node.expr)

    def visit_VarName(self, node):
        self.current_scope.lookup(node.value)

    def visit_FuncCall(self, node):
        # TODO: anything to do here?
        pass

    def visit_Function(self, node):
        self.functions[node.fn_name.value] = node
        # TODO: verify parameter variables matching variables within the expression part

    def visit_Assign(self, node):
        var = Variable(name=node.left.value, value=self.visit(node.right))
        self.current_scope.insert(var)

#-------------------------------------------------------------------------------
# Interpreter
#-------------------------------------------------------------------------------

class Interpreter(NodeVisitor):
    def __init__(self):
        self.var_table = ScopedVarTable('global')
        self.current_scope = self.var_table
        self.functions = {}
        self.lexer = Lexer()
        self.parser = Parser(self.lexer)

    def input(self, expression):
        self.parser.set_expression(expression)
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
            return +self.visit(node.expr)
        elif node.op.type == 'minus':
            return -self.visit(node.expr)

    def visit_VarName(self, node):
        var = self.current_scope.lookup(node.value)
        return var.value

    def visit_FuncCall(self, node):
        param_values = []
        for param in node.fn_params:
            value = self.visit(param)
            param_values.append(value)
        function = self.functions[node.fn_name.value]
        func_var_table = ScopedVarTable(function.fn_name.value,
                                        enclosing_scope=self.current_scope)
        func_var_table.enclosing_scope = self.current_scope
        variables = collections.OrderedDict(zip(function.fn_vars.keys(), param_values))
        for name in variables:
            func_var_table.insert(Variable(name=name, value=variables[name]))
        self.current_scope = func_var_table
        result = self.visit(function.expr)
        self.current_scope = self.current_scope.enclosing_scope
        return result

    def visit_Function(self, node):
        self.functions[node.fn_name.value] = node
        func_var_table = ScopedVarTable(node.fn_name.value,
                                        enclosing_scope=self.current_scope)
        func_var_table.vars = node.fn_vars
        self.current_scope = func_var_table
        self.visit(node.expr)
        self.current_scope = self.current_scope.enclosing_scope

    def visit_Assign(self, node):
        var = Variable(name=node.left.value, value=self.visit(node.right))
        self.current_scope.insert(var)
        return var.name

#-------------------------------------------------------------------------------
# Main
#-------------------------------------------------------------------------------

interpreter = Interpreter()

# print(interpreter.input('fn add => x + z')) # ERROR: Unknown identifier 'x'
print(interpreter.input('fn add x y => x + z')) # ERROR: Invalid identifier 'z' in function body.
print(interpreter.input('y + 7')) # ERROR: Invalid identifier. No variable with name 'y' was found.

print(interpreter.input('fn avg x y => (x + y) / 2')) # None
print(interpreter.input('a = 7')) # 7
print(interpreter.input('b = 3')) # 3
print(interpreter.input('avg a b')) # 5


print(interpreter.input('x=7')) # 7
print(interpreter.input('y=2.7')) # 2.7
print(interpreter.input('x')) # 7
print(interpreter.input('y')) # 2.7

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
