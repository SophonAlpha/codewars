"""
Test suite for The Lift kata:
https://www.codewars.com/kata/tiny-three-pass-compiler
"""

import pytest

from solutions.tiny_three_pass_compiler import Compiler

TESTS = [["[ x y ] ( x + y ) / 2",
          "{ 'op': '/', 'a': { 'op': '+', 'a': { 'op': 'arg', 'n': 0 }, \
                                          'b': { 'op': 'arg', 'n': 1 }}, \
                        'b': { 'op': 'imm', 'n': 2 }}"],
         ["[ x ] x + 2*5",
          "{ 'op': '+', 'a': { 'op': 'arg', 'n': 0 }, \
                        'b': { 'op': '*', 'a': { 'op': 'imm', 'n': 2 }, \
                                          'b': { 'op': 'imm', 'n': 5 } } }",
          "{ 'op': '+', 'a': { 'op': 'arg', 'n': 0 }, \
                        'b': { 'op': 'imm', 'n': 10 } }",
          [ 'IM 10', 'SW', 'AR 0', 'AD' ]],
         ["[ a b ] a*a + b*b",
          "pass1",
          "pass2",
          "pass3"],
         ["[ first second ] (first + second) / 2",
          "pass1",
          "pass2",
          "pass3"]]
