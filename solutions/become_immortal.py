"""

My solution for Become Immortal kata:
https://www.codewars.com/kata/become-immortal

Level: 1 kyu

"""

import numpy as np

np.set_printoptions(threshold=np.inf)

def elder_age(m, n, l, t):
    rows, cols = np.array(np.meshgrid(np.arange(m), np.arange(n))).reshape(2, m*n)
    xor_arr = np.bitwise_xor(rows, cols).reshape(n, m)
    trans_loss = np.subtract(xor_arr, l)
    trans_loss[trans_loss < 0] = 0
    np.savetxt("trans_loss.csv", trans_loss, fmt='%i', delimiter=",")
    print(trans_loss)
    donate_time = np.sum(trans_loss) % t
    print('donate_time = {}'.format(donate_time))
    return donate_time

def sum_array():
    max_m, max_n, l, t = 40, 40, 0, 10000
    sum_arr = np.zeros(shape=(max_n, max_m))
    input_arr = np.array(np.meshgrid(np.arange(max_n),
                                     np.arange(max_m))).reshape(2, max_n*max_m).T
    for _, (n, m) in enumerate(input_arr):
        donate_time = elder_age(m, n, l, t)
        sum_arr[n, m] = donate_time
    print(sum_arr)

if __name__ == "__main__":
    elder_age(48, 48, 0, 10000)
#     sum_array()
    