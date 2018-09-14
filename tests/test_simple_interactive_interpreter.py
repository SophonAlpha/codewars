import unittest

from solutions.simple_interactive_interpreter import Interpreter

class Tests(unittest.TestCase):
    def setUp(self):
        self.interpreter = Interpreter()
    
    def test_empty_input(self):
        for i in ['', ' ']:
            with self.subTest(msg=i):
                self.assertEqual(self.interpreter.input(i), '')

    def test_ERROR_malformed_input_string(self):
        for i in ['1 2', '1two']:
            with self.subTest(msg=i):
                self.assertRaisesRegex(Exception, r'ERROR: Invalid i.',
                                       self.interpreter.input, i)

    def test_ERROR_function_duplicate_params(self):
        self.assertRaisesRegex(Exception, r'ERROR: Duplicate variable \'.*\' in function declaration\.',
                               self.interpreter.input, 'fn add x x => x + x')

    def test_ERROR_function_unknown_identifier(self):
        self.assertRaisesRegex(Exception, r'ERROR: Unknown identifier \'.*\'',
                               self.interpreter.input, 'fn add => x + z')

    def test_ERROR_function_invalid_identifier(self):
        self.assertRaisesRegex(Exception, r'ERROR: Invalid identifier \'.*\' in function body\.',
                               self.interpreter.input, 'fn add x y => x + z')

    def test_ERROR_function_wrong_number_params(self):
        self.interpreter.input('fn add x y => x + y')
        self.assertRaisesRegex(Exception, r'ERROR: Function \'add\' expects \'2\' parameters. \'1\' given\.',
                               self.interpreter.input, 'add 5')

    def test_ERROR_no_variable_found(self):
        self.assertRaisesRegex(Exception, r'ERROR: Invalid identifier. No variable with name \'.*\' was found\.',
                               self.interpreter.input, 'y + 7')

    def test_ERROR_name_already_defined(self):
        i = 'fn add x y => x + y'
        self.interpreter.input(i)
        with self.subTest(msg=i):
            self.assertRaisesRegex(Exception, r'ERROR: Variable name \'add\' already defined as function name\.',
                                   self.interpreter.input, 'add = 2')
        i = 'bub = 7'
        self.interpreter.input(i)
        with self.subTest(msg=i):
            self.assertRaisesRegex(Exception, r'ERROR: Function name \'bub\' already defined as variable name\.',
                                   self.interpreter.input, 'fn bub x y => x + y')

    def test_variable_definition(self):
        for i, out in [('x=7', 7),
                       ('y=2.7', 2.7),
                       ('x', 7),
                       ('y', 2.7)]:
            with self.subTest(msg=i):
                self.assertEqual(self.interpreter.input(i), out)

    def test_function_definition(self):
        for i in ['fn echo x => x',
                  'fn avg x y => (x + y) / 2',
                  'fn add x y => x + y']:
            with self.subTest(msg=i):
                self.assertEqual(self.interpreter.input(i), '')

    def test_function_call(self):
        self.interpreter.input('fn avg x y => (x + y) / 2')
        self.interpreter.input('a = 7')
        self.interpreter.input('b = 3')
        self.assertEqual(self.interpreter.input('avg a b'), 5)

    def test_nested_function_call(self):
        self.interpreter.input('fn echo x => x')
        self.interpreter.input('fn avg x y => (x + y) / 2')
        self.assertEqual(self.interpreter.input('avg echo 4 echo 2'), 3)

# 
# print(interpreter.i('5 - - - 2')) # 3
# 
# print(interpreter.i('2 * 7 + 3')) # 17
# print(interpreter.i('2 * (7 + 3)')) # 20
# print(interpreter.i('7 + 3 * (10 / (12 / (3 + 1) - 1))')) # 22
# print(interpreter.i('7 + 3 * (10 / (12 / (3 + 1) - 1)) / (2 + 3) - 5 - 3 + (8)')) # 10
# print(interpreter.i('7 + (((3 + 2)))')) # 12
# print(interpreter.i('7 + 3')) # 10
# 
# print(interpreter.i('b = 8'))
# print(interpreter.i('a + b'))
# print(interpreter.i('first_var = 14 + 2 * 3 - 6 / 2')) # = 17
# print(interpreter.i('second_var = 7 + 3 * (10 / (12 / (3 + 1) - 1))')) # = 22
# print(interpreter.i('7 + 3 * (10 / (12 / (3 + first_var) - 1)) / (2 + 3) - 5 - second_var + (8)')) # = -27
# print(interpreter.i('a = b = 12')) # = 12
# print(interpreter.i('x = 13 + (y = 3)')) # = 16
# 
# print(interpreter.i('7 % 2')) # = 1
# print(interpreter.i('7%2')) # = 1
# print(interpreter.i('8 % 3')) # = 2
# print(interpreter.i('14 + 2 * 3 - 6 / 2')) # = 17
# print(interpreter.i('14.34 + 2.237 * 3.901 - 6.018 / 2.0893644')) # = 20.186235220186006
# print(interpreter.i('7 + 3 * (10 / (12 / (3 + 1) - 1))')) # = 22
# print(interpreter.i('7 + 3 * (10 / (12 / (3 + 1) - 1)) / (2 + 3) - 5 - 3 + (8)')) # = 10
# print(interpreter.i('7 + (((3 + 2)))')) # = 12

#
# # Basic arithmetic
# assert interpreter.i("1 + 1"), 2
# assert interpreter.i("2 - 1"), 1
# assert interpreter.i("2 * 3"), 6
# assert interpreter.i("8 / 4"), 2
# assert interpreter.i("7 % 4"), 3
#
# # Variables
# assert interpreter.i("x = 1"), 1
# assert interpreter.i("x"), 1
# assert interpreter.i("x + 3"), 4
# print(interpreter.i("y"))
#
# # Functions
# print(interpreter.i("fn avg x y => (x + y) / 2"))
# assert interpreter.i("avg 4 2"), 3
# print(interpreter.i("avg 7"))
# print(interpreter.i("avg 7 2 4"))
#
# # Conflicts
# print(interpreter.i("fn x => 0"))
# print(interpreter.i("avg = 5"))

