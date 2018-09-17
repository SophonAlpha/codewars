"""
running test with code coverage from command line:

py.test tests\test_pytest_simple_interactive_interpreter.py --cov=solutions.simple_interactive_interpreter --cov-report html
"""

import pytest

from solutions.simple_interactive_interpreter import Interpreter

@pytest.fixture
def interpreter():
    return Interpreter()

@pytest.mark.parametrize('expr', [
    '',
    ' '
    ])
def test_empty_input(interpreter, expr):
    assert interpreter.input(expr) == ''

def test_ERROR_invalid_syntax(interpreter):
    with pytest.raises(Exception, match=r'invalid syntax'):
        interpreter.input('fn => x + y')

@pytest.mark.parametrize('expr', [
    '1 2',
    '1two',
    'add 3 7 11'
    ])
def test_ERROR_malformed_input_string(interpreter, expr):
    interpreter.input('fn add x y => x + y')
    with pytest.raises(Exception, match=r'ERROR: Invalid input.'):
        interpreter.input(expr)

@pytest.mark.parametrize('expr, error_msg', [
    ('fn add x x => x + x', r'ERROR: Duplicate variable \'.*\' in function declaration\.'),
    ('fn add => x + z', r'ERROR: Unknown identifier \'.*\''),
    ('fn add x y => x + z', r'ERROR: Invalid identifier \'.*\' in function body\.'),
    ('y + 7', r'ERROR: Invalid identifier. No variable with name \'.*\' was found\.')
    ])
def test_ERROR_messages(interpreter, expr, error_msg):
    with pytest.raises(Exception, match=error_msg):
        interpreter.input(expr)

def test_ERROR_function_wrong_number_params(interpreter):
    interpreter.input('fn add x y => x + y')
    with pytest.raises(Exception, match=r'ERROR: Function \'add\' expects \'2\' parameters. \'1\' given\.'):
        interpreter.input('add 5')

 
def test_ERROR_name_already_defined(interpreter):
    expr = 'fn add x y => x + y'
    interpreter.input(expr)
    with pytest.raises(Exception, match=r'ERROR: Variable name \'add\' already defined as function name\.'):
        interpreter.input('add = 2')
    expr = 'bub = 7'
    interpreter.input(expr)
    with pytest.raises(Exception, match=r'ERROR: Function name \'bub\' already defined as variable name\.'):
        interpreter.input('fn bub x y => x + y')

def test_variable_definition(interpreter):
    for expr, expected_result in [
                                   ('x=7', 7),
                                   ('y=2.7', 2.7),
                                   ('x', 7),
                                   ('y', 2.7)
                                ]:
        assert interpreter.input(expr) == expected_result

def test_function_definition(interpreter):
    for expr in ['fn echo x => x',
              'fn avg x y => (x + y) / 2',
              'fn add x y => x + y']:
        assert interpreter.input(expr) == ''

def test_function_call(interpreter):
    interpreter.input('fn avg x y => (x + y) / 2')
    interpreter.input('a = 7')
    interpreter.input('b = 3')
    assert interpreter.input('avg a b') == 5
 
def test_nested_function_call(interpreter):
    interpreter.input('fn echo x => x')
    interpreter.input('fn avg x y => (x + y) / 2')
    assert interpreter.input('avg echo 4 echo 2') == 3


@pytest.mark.parametrize('expr, expected_result', [
    ('5 - - - 2', 3),
    ('5 + + + 2', 7),
    ('5 + - + 2', 3)
    ]) 
def test_unary_operator(interpreter, expr, expected_result):
    assert interpreter.input(expr) == expected_result

def test_various_expressions(interpreter):
    for expr, expected_result in [
                ('2 * 7 + 3', 17),
                ('2 * (7 + 3)', 20),
                ('7 + 3 * (10 / (12 / (3 + 1) - 1))', 22),
                ('7 + 3 * (10 / (12 / (3 + 1) - 1)) / (2 + 3) - 5 - 3 + (8)', 10),
                ('7 + (((3 + 2)))', 12),
                ('7 + 3', 10),
                ('first_var = 14 + 2 * 3 - 6 / 2', 17),
                ('second_var = 7 + 3 * (10 / (12 / (3 + 1) - 1))', 22),
                ('7 + 3 * (10 / (12 / (3 + first_var) - 1)) / (2 + 3) - 5 - second_var + (8)', -27),
                ('a = b = 12', 12),
                ('x = 13 + (y = 3)', 16),
                ('7 % 2', 1),
                ('7%2', 1),
                ('8 % 3', 2),
                ('14 + 2 * 3 - 6 / 2', 17),
                ('14.34 + 2.237 * 3.901 - 6.018 / 2.0893644', 20.186235220186006),
                ('7 + 3 * (10 / (12 / (3 + 1) - 1))', 22),
                ('7 + 3 * (10 / (12 / (3 + 1) - 1)) / (2 + 3) - 5 - 3 + (8)', 10),
                ('7 + (((3 + 2)))', 12),
                ('1 + 1', 2),
                ('2 - 1', 1),
                ('2 * 3', 6),
                ('8 / 4', 2),
                ('7 % 4', 3)]:
        assert interpreter.input(expr) == expected_result
