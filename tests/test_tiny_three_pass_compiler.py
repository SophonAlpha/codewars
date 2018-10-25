"""
Test suite for The Lift kata:
https://www.codewars.com/kata/tiny-three-pass-compiler
"""

import pytest

from solutions.tiny_three_pass_compiler import Compiler

TESTS = [["[ x y ] ( x + y ) / 2",
          { 'op': '/', 'a': { 'op': '+', 'a': { 'op': 'arg', 'n': 0 }, \
                                         'b': { 'op': 'arg', 'n': 1 }}, \
                       'b': { 'op': 'imm', 'n': 2 }},
          { 'op': '/', 'a': { 'op': '+', 'a': { 'op': 'arg', 'n': 0 }, \
                                         'b': { 'op': 'arg', 'n': 1 }}, \
                       'b': { 'op': 'imm', 'n': 2 }},
          "pass3"],
         ["[ x ] x + 2*5",
          {'op': '+', 'a': {'op': 'arg', 'n': 0}, \
                      'b': {'op': '*', 'a': {'op': 'imm', 'n': 2}, \
                                       'b': {'op': 'imm', 'n': 5}}},
          {'op': '+', 'a': {'op': 'arg', 'n': 0}, \
                      'b': {'op': 'imm', 'n': 10}},
         ['IM 10', 'SW', 'AR 0', 'AD']],
         ["[] 3 * (4 + 23) * 7 + (2 * (3 + 6 * 3))",
          {'op': '+', 'a': {'op': '*', 'a': {'op': '*', 'a': {'op': 'imm', 'n': 3},
                                                        'b': {'op': '+', 'a': {'op': 'imm', 'n': 4},
                                                                         'b': {'op': 'imm', 'n': 23}}},
                                       'b': {'op': 'imm', 'n': 7}},
                      'b': {'op': '*', 'a': {'op': 'imm', 'n': 2},
                                       'b': {'op': '+', 'a': {'op': 'imm', 'n': 3},
                                                        'b': {'op': '*', 'a': {'op': 'imm', 'n': 6},
                                                                         'b': {'op': 'imm', 'n': 3}}}}},
          {'op': 'imm', 'n': 609},
          "pass3"],
         ["[ a b ] a*a + b*b",
          "pass1",
          "pass2",
          "pass3"],
         ["[ first second ] (first + second) / 2",
          "pass1",
          "pass2",
          "pass3"]]

TEST_IDs = [str(i) for i in range(1, len(TESTS) + 1)]
START = 0
END = 3

@pytest.mark.parametrize('program, unoptimized_AST, optimized_AST, assem_instr',
                         TESTS[START:END], ids=TEST_IDs[START:END])
def test_pass1(program, unoptimized_AST, optimized_AST, assem_instr):
    """ test """
    _test_id = TESTS.index([program, unoptimized_AST,
                           optimized_AST, assem_instr]) + 1
    compiler = Compiler()
    result = compiler.pass1(program)
    assert dicts_equal(result, unoptimized_AST)

@pytest.mark.parametrize('program, unoptimized_AST, optimized_AST, assem_instr',
                         TESTS[START:END], ids=TEST_IDs[START:END])
def test_pass2(program, unoptimized_AST, optimized_AST, assem_instr):
    """ test """
    _test_id = TESTS.index([program, unoptimized_AST,
                           optimized_AST, assem_instr]) + 1
    compiler = Compiler()
    pass1 = compiler.pass1(program)
    result = compiler.pass2(pass1)
    assert dicts_equal(result, optimized_AST)

def dicts_equal(dict1, dict2):
    for k1, v1 in dict1.items():
        if k1 in dict2.keys():
            v2 = dict2[k1]
        else:
            return False
        if isinstance(v1, dict) and isinstance(v2, dict):
            if not dicts_equal(v1, v2):
                return False
        elif not v1 == v2:
            return False
    return True
