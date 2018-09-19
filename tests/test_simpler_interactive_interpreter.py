"""
running test with code coverage from command line:

py.test tests\test_very_simple_interactive_interpreter.py
--cov=solutions.simpler_interactive_interpreter --cov-report html
"""

import pytest

from solutions.simpler_interactive_interpreter import Interpreter

@pytest.fixture
def _interpreter():
    """ object for all test cases """
    return Interpreter()

@pytest.mark.parametrize('expr', [
    '',
    ' '
    ])
def test_empty_input(_interpreter, expr):
    """ test """
    assert _interpreter.input(expr) == ''

def test_error_invalid_syntax(_interpreter):
    """ test """
    with pytest.raises(Exception, match=r'ERROR: Invalid input.'):
        _interpreter.input('a => 5')

@pytest.mark.parametrize('expr', [
    '1 2',
    '1two'
    ])
def test_error_malformed_input(_interpreter, expr):
    """ test """
    with pytest.raises(Exception, match=r'ERROR: Invalid input.'):
        _interpreter.input(expr)

def test_error_messages(_interpreter):
    """ test """
    with pytest.raises(Exception, match=r'ERROR: Invalid identifier. No '
                       r'variable with name \'.*\' was found\.'):
        _interpreter.input('y + 7')

def test_variable_definition(_interpreter):
    """ test """
    for expr, expected_result in [
            ('x=7', 7),
            ('y=2.7', 2.7),
            ('x', 7),
            ('y', 2.7)]:
        assert _interpreter.input(expr) == expected_result

@pytest.mark.parametrize('expr, expected_result', [
    ('5 - - - 2', 3),
    ('5 + + + 2', 7),
    ('5 + - + 2', 3)])
def test_unary_operator(_interpreter, expr, expected_result):
    """ test """
    assert _interpreter.input(expr) == expected_result

def test_various_expressions(_interpreter):
    """ test """
    for expr, expected_result in [
            ('2 * 7 + 3', 17),
            ('2 * (7 + 3)', 20),
            ('7 + 3 * (10 / (12 / (3 + 1) - 1))', 22),
            ('7 + 3 * (10 / (12 / (3 + 1) - 1)) / (2 + 3) - 5 - 3 + (8)', 10),
            ('7 + (((3 + 2)))', 12),
            ('7 + 3', 10),
            ('first_var = 14 + 2 * 3 - 6 / 2', 17),
            ('second_var = 7 + 3 * (10 / (12 / (3 + 1) - 1))', 22),
            ('7 + 3 * (10 / (12 / (3 + first_var) - 1)) / '
             '(2 + 3) - 5 - second_var + (8)', -27),
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
        assert _interpreter.input(expr) == expected_result
