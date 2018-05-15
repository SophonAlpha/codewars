'''
Created on 21 Mar 2017

@author: H155936
'''
even = [2, 4, 0, 100, 4, 11, 2602, 36]
odd = [3, 5, 1, 101, 5, 12, 2603, 37]
f = odd

b_f = [i%2 for i in f]
i = 0
if sum(b_f) == 1:
    i = 1
print f[b_f.index(i)]
