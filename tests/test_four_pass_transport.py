"""
Test suite for Four Pass Transport kata:
https://www.codewars.com/kata/four-pass-transport

coverage test:
py.test tests\test_four_pass_transport.py --cov=solutions.four_pass_transport --cov-report html
"""

import pytest

from solutions.four_pass_transport import four_pass

TESTS = [
    [1, 69, 95, 70],
    [0, 49, 40, 99],
    [0, 99, 9, 90],
    [37, 61, 92, 36],
    [51, 24, 75, 57],
    [92, 59, 88, 11]]

SOLUTIONS = [
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 19, 29, 39, 49, 59,
     69, 79, 78, 77, 76, 75, 85, 95, 94, 93, 92, 91, 81, 71, 70],
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 19, 29, 39, 49, 48, 47, 46, 45, 44, 43, 42,
     41, 40, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 69, 79, 89, 99],
    None,
    [37, 27, 26, 25, 24, 23, 22, 21, 31, 41, 51,
     61, 71, 81, 91, 92, 93, 94, 95, 96, 86, 76, 66, 56, 46, 36],
    [51, 41, 42, 43, 44, 34, 24, 25, 35, 45, 55,
     65, 75, 76, 77, 67, 57],
    [92, 93, 94, 95, 96, 97, 98, 99, 89, 79, 69, 59, 58, 68, 78, 88, 87, 77,
     67, 57, 47, 37, 27, 17, 16, 15, 14, 13, 12, 11]]

@pytest.mark.parametrize('stations, solution', zip(TESTS, SOLUTIONS))
def test_examples(stations, solution):
    """ tests """
    validate_solution(stations, solution)

def validate_solution(stations, solution):
    """ helper function to validate solution path is the shortest """
    if solution:
        lenghts_sol = get_seg_lens(stations, solution)
        lenghts_test = get_seg_lens(stations, four_pass(stations))
    else:
        lenghts_sol = solution
        lenghts_test = four_pass(stations)
    assert lenghts_test == lenghts_sol

def get_seg_lens(stations, solution):
    """ helper function to calculate individual path lengths """
    path_lens = []
    for i, _ in enumerate(stations[:-1]):
        start_index = solution.index(stations[i])
        end_index = solution.index(stations[i + 1])
        path_lens.append(len(solution[start_index:end_index]))
    return path_lens
