"""

My solution for 'Faberge Easter Eggs crush test' kata:
https://www.codewars.com/kata/faberge-easter-eggs-crush-test

Level: 3 kyu

"""

def height(eggs, tries):
    floor = 0
    if eggs > 0 and tries > 0:
        floor = get_floor(eggs, tries)
    return floor

def get_floor(eggs, tries):
    total_floors = 0
    segments = tries
    max_level = min(eggs, tries)
    level_count_prev = []
    for level in range(1, max_level + 1):
#         if level == 1:
#             floor += segments + (tries - segments) + 1
#         else:
#             floor += sum_arith_seq(segments - 1, level, segments - 1)
        level_count_curr = []
        segment_floors = 0
        for segment in range(segments):
            attempt = segment + level
            print(level, attempt, eggs)
            if level > 1:
                segment_count = sum(level_count_prev[segment:: -1])
            else:
                segment_count = 1
            level_count_curr.append(segment_count)
            segment_floors += segment_count
        total_floors += segment_floors
        level_count_prev = level_count_curr[:]
        segments -= 1
        eggs -= 1
    return total_floors

def sum_arith_seq(num, start, end):
    return (num * (start + end)) / 2

if __name__ == "__main__":
    
    print(height(5, 6))
#     print(height(5, 6))
#     print(height(19, 3))
#     print(height(477, 500))
#     print(height(477, 600))
    # print(height(5, 6)) # 62
    # print(height(7, 20)) # 137979
#     print(height(477, 500))
