import numpy

def persistence(n):
    ret = 0
    if len(str(n)) > 1:
        ret = 1
        while True:
            n = get_prod(n)
            if len(str(n)) <= 1:
                break
            ret += 1
    return ret
        
def get_prod(n):
    n_int = [int(char) for char in str(n)]
    result = numpy.prod(n_int)
    return result

print(persistence(39)) # 3
print(persistence(4)) # 0
print(persistence(25)) # 2
print(persistence(999)) # 4