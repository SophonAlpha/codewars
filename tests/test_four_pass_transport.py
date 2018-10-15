"""
Test suite for Four Pass Transport kata:
https://www.codewars.com/kata/four-pass-transport

coverage test:
py.test tests\test_four_pass_transport.py --cov=solutions.four_pass_transport --cov-report html
"""

import pytest

from solutions.four_pass_transport_Blind4Basics import four_pass
# from solutions.four_pass_transport import Factory
# from solutions.four_pass_transport import PathPlanner

TESTS = [
    [1, 69, 95, 70],
    [0, 49, 40, 99],
    [0, 99, 9, 90],
    [37, 61, 92, 36],
    [51, 24, 75, 57],
    [92, 59, 88, 11],
    [62, 67, 36, 86],
    [83, 79, 96, 7],
    [16, 10, 18, 14],
    [3, 75, 49, 2],
    [3, 7, 22, 6],
    [49, 41, 76, 12],
    [98, 4, 76, 79],
    [88, 41, 56, 91],
    [49, 74, 29, 77],
    [90, 27, 86, 15],
    [89, 41, 85, 6],
    [82, 50, 37, 63],
    [56, 28, 77, 94],
    [41, 34, 82, 15]]

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
     67, 57, 47, 37, 27, 17, 16, 15, 14, 13, 12, 11],
    [62, 63, 64, 65, 66, 67, 57, 56, 46, 36, 37, 38, 48, 58, 68, 78, 88, 87,
     86],
    [83, 73, 74, 75, 76, 77, 78, 79, 89, 88, 87, 86, 96, 95, 94, 93, 92, 82,
     72, 62, 52, 42, 32, 22, 12, 2, 3, 4, 5, 6, 7],
    [16, 26, 25, 24, 23, 22, 21, 11, 10, 20, 30, 31, 32, 33, 34, 35, 36, 37,
     38, 28, 18, 8, 7, 6, 5, 4, 14],
    [3, 4, 5, 15, 25, 35, 45, 55, 65, 75, 76, 77, 78, 68, 58, 48, 49, 59, 69,
     79, 89, 88, 87, 86, 85, 84, 83, 82, 72, 62, 52, 42, 32, 22, 12, 2],
    [3, 2, 1, 11, 21, 31, 32, 33, 34, 35, 36, 37, 38, 28, 18, 8, 7, 17, 27,
     26, 25, 24, 23, 22, 12, 13, 14, 15, 16, 6],
    [49, 48, 47, 46, 45, 44, 43, 42, 41, 51, 52, 53, 54, 55, 56, 66, 76, 75,
     65, 64, 63, 62, 61, 60, 50, 40, 30, 20, 10, 11, 12],
    [98, 88, 87, 86, 85, 84, 74, 64, 54, 44, 34, 24, 14, 4, 5, 6, 16, 26, 36,
     46, 56, 66, 76, 77, 78, 79],
    [88, 78, 68, 58, 48, 47, 46, 45, 44, 43, 42, 41, 51, 52, 53, 54, 55, 56,
     66, 65, 64, 63, 62, 61, 71, 81, 91],
    [49, 59, 69, 79, 89, 88, 87, 86, 85, 84, 74, 64, 54, 44, 34, 24, 25, 26,
     27, 28, 29, 39, 38, 37, 47, 57, 67, 77],
    [90, 91, 92, 93, 94, 95, 96, 97, 87, 77, 67, 57, 47, 37, 27, 26, 36, 46,
     56, 66, 76, 86, 85, 75, 65, 55, 45, 35, 25, 15],
    [89, 99, 98, 97, 96, 95, 94, 93, 92, 91, 81, 71, 61, 51, 41, 42, 43, 44,
     45, 55, 65, 75, 85, 86, 76, 66, 56, 46, 36, 26, 16, 6],
    [82, 72, 71, 61, 51, 50, 40, 41, 42, 43, 44, 45, 46, 36, 37, 47, 57, 56,
     55, 54, 53, 63],
    [56, 46, 47, 37, 27, 28, 38, 48, 58, 68, 67, 77, 87, 86, 85, 84, 94],
    [41, 31, 32, 33, 34, 44, 43, 42, 52, 62, 72, 82, 83, 84, 85, 75, 65, 55,
     45, 35, 25, 15]]

@pytest.mark.parametrize('stations, solution', zip(TESTS, SOLUTIONS))
def test_examples(stations, solution):
    """ tests """
    validate_solution(stations, solution)
    
# def test_show_state():
#     factory = Factory([1, 69, 95, 70])
#     path_planner = PathPlanner(factory)
#     path_planner.plan()
#     factory.show_state()
#     assert True

def validate_solution(stations, solution):
    """ helper function to validate solution path is the shortest """
    test_case_path = four_pass(stations)
    if solution:
        lenghts_sol = get_seg_lens(stations, solution)
        lenghts_test = get_seg_lens(stations, test_case_path)
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
