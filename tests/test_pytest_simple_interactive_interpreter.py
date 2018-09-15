import pytest

from solutions.simple_interactive_interpreter import Interpreter

class Test:

    def setup_method(self):
        self.interpreter = Interpreter()
    
    @pytest.mark.parametrizes(
        'i', ['', ' '])
    def test_empty_input(self, i):
        assert self.interpreter.input(i) == ''


#     def test_ERROR_malformed_input_string(self):
#         self.interpreter.input('fn add x y => x + y')
#         for i in ['1 2',
#                   '1two',
#                   'add 3 7 11']:
#             with self.subTest(msg=i):
#                 self.assertRaisesRegex(Exception, r'ERROR: Invalid input.',
#                                        self.interpreter.input, i)
# 
#     def test_ERROR_function_duplicate_params(self):
#         self.assertRaisesRegex(Exception, r'ERROR: Duplicate variable \'.*\' in function declaration\.',
#                                self.interpreter.input, 'fn add x x => x + x')
# 
#     def test_ERROR_function_unknown_identifier(self):
#         self.assertRaisesRegex(Exception, r'ERROR: Unknown identifier \'.*\'',
#                                self.interpreter.input, 'fn add => x + z')
# 
#     def test_ERROR_function_invalid_identifier(self):
#         self.assertRaisesRegex(Exception, r'ERROR: Invalid identifier \'.*\' in function body\.',
#                                self.interpreter.input, 'fn add x y => x + z')
# 
#     def test_ERROR_function_wrong_number_params(self):
#         self.interpreter.input('fn add x y => x + y')
#         self.assertRaisesRegex(Exception, r'ERROR: Function \'add\' expects \'2\' parameters. \'1\' given\.',
#                                self.interpreter.input, 'add 5')
# 
#     def test_ERROR_no_variable_found(self):
#         self.assertRaisesRegex(Exception, r'ERROR: Invalid identifier. No variable with name \'.*\' was found\.',
#                                self.interpreter.input, 'y + 7')
# 
#     def test_ERROR_name_already_defined(self):
#         i = 'fn add x y => x + y'
#         self.interpreter.input(i)
#         with self.subTest(msg=i):
#             self.assertRaisesRegex(Exception, r'ERROR: Variable name \'add\' already defined as function name\.',
#                                    self.interpreter.input, 'add = 2')
#         i = 'bub = 7'
#         self.interpreter.input(i)
#         with self.subTest(msg=i):
#             self.assertRaisesRegex(Exception, r'ERROR: Function name \'bub\' already defined as variable name\.',
#                                    self.interpreter.input, 'fn bub x y => x + y')
# 
#     def test_variable_definition(self):
#         for i, out in [('x=7', 7),
#                        ('y=2.7', 2.7),
#                        ('x', 7),
#                        ('y', 2.7)]:
#             with self.subTest(msg=i):
#                 self.assertEqual(self.interpreter.input(i), out)
# 
#     def test_function_definition(self):
#         for i in ['fn echo x => x',
#                   'fn avg x y => (x + y) / 2',
#                   'fn add x y => x + y']:
#             with self.subTest(msg=i):
#                 self.assertEqual(self.interpreter.input(i), '')
# 
#     def test_function_call(self):
#         self.interpreter.input('fn avg x y => (x + y) / 2')
#         self.interpreter.input('a = 7')
#         self.interpreter.input('b = 3')
#         self.assertEqual(self.interpreter.input('avg a b'), 5)
# 
#     def test_nested_function_call(self):
#         self.interpreter.input('fn echo x => x')
#         self.interpreter.input('fn avg x y => (x + y) / 2')
#         self.assertEqual(self.interpreter.input('avg echo 4 echo 2'), 3)
# 
#     def test_unary_operator(self):
#         self.assertEqual(self.interpreter.input('5 - - - 2'), 3)
# 
#     def test_various_expressions(self):
#         for i, out in [('2 * 7 + 3', 17),
#                        ('2 * (7 + 3)', 20),
#                        ('7 + 3 * (10 / (12 / (3 + 1) - 1))', 22),
#                        ('7 + 3 * (10 / (12 / (3 + 1) - 1)) / (2 + 3) - 5 - 3 + (8)', 10),
#                        ('7 + (((3 + 2)))', 12),
#                        ('7 + 3', 10),
#                        ('first_var = 14 + 2 * 3 - 6 / 2', 17),
#                        ('second_var = 7 + 3 * (10 / (12 / (3 + 1) - 1))', 22),
#                        ('7 + 3 * (10 / (12 / (3 + first_var) - 1)) / (2 + 3) - 5 - second_var + (8)', -27),
#                        ('a = b = 12', 12),
#                        ('x = 13 + (y = 3)', 16),
#                        ('7 % 2', 1),
#                        ('7%2', 1),
#                        ('8 % 3', 2),
#                        ('14 + 2 * 3 - 6 / 2', 17),
#                        ('14.34 + 2.237 * 3.901 - 6.018 / 2.0893644', 20.186235220186006),
#                        ('7 + 3 * (10 / (12 / (3 + 1) - 1))', 22),
#                        ('7 + 3 * (10 / (12 / (3 + 1) - 1)) / (2 + 3) - 5 - 3 + (8)', 10),
#                        ('7 + (((3 + 2)))', 12),
#                        ('1 + 1', 2),
#                        ('2 - 1', 1),
#                        ('2 * 3', 6),
#                        ('8 / 4', 2),
#                        ('7 % 4', 3)]:
#             with self.subTest(msg=i):
#                 self.assertEqual(self.interpreter.input(i), out)
