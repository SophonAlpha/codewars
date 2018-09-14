def find_even_index(arr):
    n = -1
    for i,_ in enumerate(arr):
        if sum(arr[:i]) == sum(arr[i+1:]):
            n = i
            break
    return n
    
print(find_even_index([1,2,3,4,3,2,1]))
print(find_even_index([1,100,50,-51,1,1]))
print(find_even_index([1,2,3,4,5,6]))
print(find_even_index([20,10,30,10,10,15,35]))
print(find_even_index([20,10,-80,10,10,15,35]))
print(find_even_index([10,-80,10,10,15,35,20]))
print(find_even_index(range(1,100)))
print(find_even_index([0,0,0,0,0]))
print(find_even_index([-1,-2,-3,-4,-3,-2,-1]))
print(find_even_index(range(-100,-1)))
