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
    floor = 0
    segments = tries
    max_level = min(eggs, tries)
    level_count = {}
    for level in range(1, max_level):
        for segment in range(segments):
            attempt = segment + level
            if level > 1:
                start = segment if segment < segments - 2 else segments - 2
                segment_count = sum(level_count[level - 1][start:: -1])
            else:
                segment_count = 1
            if level not in level_count:
                level_count[level] = []
            level_count[level].append(segment_count)
            if eggs - 1 <= 1 or tries - attempt <= 1:
                floor_height = tries - attempt + 1
            else:
                floor_height = 1
            floor += floor_height * segment_count
        segments -= 1
        eggs -= 1
    return floor

if __name__ == "__main__":
#     print(height(5, 6))
#     print(height(19, 3))
    # print(height(5, 6)) # 62
    # print(height(7, 20)) # 137979
    print(height(477, 500))
