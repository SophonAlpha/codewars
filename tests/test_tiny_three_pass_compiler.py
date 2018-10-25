"""
Test suite for The Lift kata:
https://www.codewars.com/kata/tiny-three-pass-compiler
"""

import pytest

from solutions.tiny_three_pass_compiler import Compiler

PROGRAMS = ['[ x y z ] ( 2*3*x + 5*y - 3*z ) / (1 + 3 + 2*2)',
            '[ x y ] ( x + y ) / 2',
            '[ x ] x + 2*5',
            '[] 3 * (4 + 23) * 7 + (2 * (3 + 6 * 3))',
            '[ a b ] a*a + b*b',
            '[ first second ] (first + second) / 2']

RESULTS_PASS1 = [{'op': '/', 'a': {'op': '-', 'a': {'op': '+', 'a': {'op': '*', 'a': {'op': '*', 'a': {'op': 'imm', 'n': 2},
                                                                                                 'b': {'op': 'imm', 'n': 3}},
                                                                                'b': {'op': 'arg', 'n': 0}},
                                                               'b': {'op': '*', 'a': {'op': 'imm', 'n': 5},
                                                                                'b': {'op': 'arg', 'n': 1}}},
                                              'b': {'op': '*', 'a': {'op': 'imm', 'n': 3},
                                                               'b': {'op': 'arg', 'n': 2}}},
                             'b': {'op': '+', 'a': {'op': '+', 'a': {'op': 'imm', 'n': 1},
                                                               'b': {'op': 'imm', 'n': 3}},
                                              'b': {'op': '*', 'a': {'op': 'imm', 'n': 2},
                                                               'b': {'op': 'imm', 'n': 2}}}},
                 {'op': '/', 'a': {'op': '+', 'a': {'op': 'arg', 'n': 0}, \
                                              'b': {'op': 'arg', 'n': 1}}, \
                             'b': {'op': 'imm', 'n': 2}},
                 {'op': '+', 'a': {'op': 'arg', 'n': 0}, \
                             'b': {'op': '*', 'a': {'op': 'imm', 'n': 2}, \
                                              'b': {'op': 'imm', 'n': 5}}},
                 {'op': '+', 'a': {'op': '*', 'a': {'op': '*', 'a': {'op': 'imm', 'n': 3},
                                                               'b': {'op': '+', 'a': {'op': 'imm', 'n': 4},
                                                                                'b': {'op': 'imm', 'n': 23}}},
                                              'b': {'op': 'imm', 'n': 7}},
                             'b': {'op': '*', 'a': {'op': 'imm', 'n': 2},
                                              'b': {'op': '+', 'a': {'op': 'imm', 'n': 3},
                                                               'b': {'op': '*', 'a': {'op': 'imm', 'n': 6},
                                                                                'b': {'op': 'imm', 'n': 3}}}}},
                 {'op': '+', 'a': {'op': '*', 'a': {'op': 'arg', 'n': 0},
                                              'b': {'op': 'arg', 'n': 0}},
                             'b': {'op': '*', 'a': {'op': 'arg', 'n': 1},
                                              'b': {'op': 'arg', 'n': 1}}},
                 {'op': '/', 'a': {'op': '+', 'a': {'op': 'arg', 'n': 0},
                                              'b': {'op': 'arg', 'n': 1}},
                             'b': {'op': 'imm', 'n': 2}}]

RESULTS_PASS2 = [{'op': '/', 'a': {'op': '-', 'a': {'op': '+', 'a': {'op': '*', 'a': {'op': 'imm', 'n': 6},
                                                                                'b': {'op': 'arg', 'n': 0}},
                                                               'b': {'op': '*', 'a': {'op': 'imm', 'n': 5},
                                                                                'b': {'op': 'arg', 'n': 1}}},
                                              'b': {'op': '*', 'a': {'op': 'imm', 'n': 3},
                                                               'b': {'op': 'arg', 'n': 2}}},
                             'b': {'op': 'imm', 'n': 8}},
                 {'op': '/', 'a': {'op': '+', 'a': {'op': 'arg', 'n': 0}, \
                                              'b': {'op': 'arg', 'n': 1}}, \
                             'b': {'op': 'imm', 'n': 2}},
                 {'op': '+', 'a': {'op': 'arg', 'n': 0}, \
                             'b': {'op': 'imm', 'n': 10}},
                 {'op': 'imm', 'n': 609},
                 {'op': '+', 'a': {'op': '*', 'a': {'op': 'arg', 'n': 0},
                                              'b': {'op': 'arg', 'n': 0}},
                             'b': {'op': '*', 'a': {'op': 'arg', 'n': 1},
                                              'b': {'op': 'arg', 'n': 1}}},
                 {'op': '/', 'a': {'op': '+', 'a': {'op': 'arg', 'n': 0},
                                              'b': {'op': 'arg', 'n': 1}},
                             'b': {'op': 'imm', 'n': 2}}]

TESTS_ASM = [('[ x y z ] 2 * 3 * x + 5 * y', [2, 3], 27),
             ('[ x y z ] ( 2*3*x + 5*y - 3*z ) / (1 + 3 + 2*2)', [2, 3, 5], 1.5),
             ('[ x y z ] ( 2*3*x + 5*y - 3*z ) / (1 + 3 + 2*2)', [4, 0, 0], 3),
             ('[ x y z ] ( 2*3*x + 5*y - 3*z ) / (1 + 3 + 2*2)', [4, 8, 0], 8),
             ('[ x y z ] ( 2*3*x + 5*y - 3*z ) / (1 + 3 + 2*2)', [4, 8, 6], 5.75),
             ('[ x y ] ( x + y ) / 2', [4, 2], 3),
             ('[ x y ] ( x + y ) / 2', [7, 3], 5),
             ('[ x y ] ( x + y ) / 2', [6, 6], 6),
             ('[] 3 * (4 + 23) * 7 + (2 * (3 + 6 * 3))', [], 609),
             ('[ x ] x + 2*5', [7], 17),
             ('[ x ] x + 2*5', [3], 13),
             ('[ a b ] a*a + b*b', [2, 4], 20),
             ('[ first second ] (first + second) / 2', [3, 1], 2),
             ('[ first second ] (first + second) / 2', [3, 2], 2.5)]
"""
 6 * x + 5 * y

1.)
  6*x
  'IM 6', 'PU', 'AR 0', 'SW', 'PO', 'MU', 'PU',  
  5*y
  'IM 5', 'PU', 'AR 1', 'SW', 'PO', 'MU', 'SW',
  
['PO', 'AD']

"""
TEST_IDs = [str(i) for i in range(1, len(PROGRAMS) + 1)]
START = 0
END = 5

@pytest.mark.parametrize('program, unoptimized_AST',
                         zip(PROGRAMS[START:END], RESULTS_PASS1[START:END]),
                         ids=TEST_IDs[START:END])
def test_pass1(program, unoptimized_AST):
    """ test """
    compiler = Compiler()
    result = compiler.pass1(program)
    assert dicts_equal(result, unoptimized_AST)

@pytest.mark.parametrize('program, optimized_AST',
                         zip(PROGRAMS[START:END], RESULTS_PASS2[START:END]),
                         ids=TEST_IDs[START:END])
def test_pass2(program, optimized_AST):
    """ test """
    compiler = Compiler()
    pass1 = compiler.pass1(program)
    result = compiler.pass2(pass1)
    assert dicts_equal(result, optimized_AST)

@pytest.mark.parametrize('program, argv, r0', TESTS_ASM)
def test_pass3(program, argv, r0):
    """ test """
    compiler = Compiler()
    pass1 = compiler.pass1(program)
    pass2 = compiler.pass2(pass1)
    asm = compiler.pass3(pass2)
    result = simulate(asm, argv)
    assert result == r0
    
@pytest.mark.parametrize('program, argv, r0', TESTS_ASM)
def test_compile(program, argv, r0):
    """ test """
    compiler = Compiler()
    asm = compiler.compile(program)
    result = simulate(asm, argv)
    assert result == r0

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
