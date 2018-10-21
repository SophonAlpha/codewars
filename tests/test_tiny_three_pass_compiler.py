"""
Test suite for The Lift kata:
https://www.codewars.com/kata/tiny-three-pass-compiler
"""

import pytest

from solutions.tiny_three_pass_compiler import Compiler

TESTS = [["[ x y ] ( x + y ) / 2",
          "{ 'op': '/', 'a': { 'op': '+', 'a': { 'op': 'arg', 'n': 0 }, \
                                          'b': { 'op': 'arg', 'n': 1 }}, \
                        'b': { 'op': 'imm', 'n': 2 }}",
          "pass2",
          "pass3"],
         ["[ x ] x + 2*5",
          "{ 'op': '+', 'a': { 'op': 'arg', 'n': 0 }, \
                        'b': { 'op': '*', 'a': { 'op': 'imm', 'n': 2 }, \
                                          'b': { 'op': 'imm', 'n': 5 } } }",
          "{ 'op': '+', 'a': { 'op': 'arg', 'n': 0 }, \
                        'b': { 'op': 'imm', 'n': 10 } }",
         ['IM 10', 'SW', 'AR 0', 'AD']],
         ["[ a b ] a*a + b*b",
          "pass1",
          "pass2",
          "pass3"],
         ["[ first second ] (first + second) / 2",
          "pass1",
          "pass2",
          "pass3"]]

TEST_IDs = [str(i) for i in range(1, len(TESTS) + 1)]

@pytest.mark.parametrize('program, unoptimized_AST, optimized_AST, assem_instr',
                         TESTS, ids=TEST_IDs)
def test_cases(program, unoptimized_AST, optimized_AST, assem_instr):
    """ test """
    _test_id = TESTS.index([program, unoptimized_AST,
                           optimized_AST, assem_instr]) + 1
    compiler = Compiler()
    result = compiler.pass1(program)
    assert result == unoptimized_AST
