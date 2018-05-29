# https://www.codewars.com/kata/build-tower

def tower_builder(n_floors):
    tower = [('*' * (2 * l + 1)).center(2*n_floors - 1) for l in range(n_floors)]
    return tower

print(tower_builder(1))
print(tower_builder(2))
print(tower_builder(3))
