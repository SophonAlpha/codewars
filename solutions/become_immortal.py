"""

My solution for Become Immortal kata:
https://www.codewars.com/kata/become-immortal

Level: 1 kyu

"""

import numpy as np

np.set_printoptions(threshold=np.inf)

def elder_age(m, n, l, t):
    m, n, l, t = 8, 5, 1, 100
    rows, cols = np.array(np.meshgrid(np.arange(m), np.arange(n))).reshape(2, -1)
    mask = np.ones(len(rows), dtype=bool)
    mask[[]] = False
    
    
    iu = np.triu_indices(n, 1)
    np.array(np.meshgrid(np.arange(n), np.arange(m))).T.reshape(-1, 2)
    iu = np.triu_indices(5, 1, m=8)
    
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
    elder_age(128, 128, 0, 10000)
#     sum_array()

"""
Notes:

  8 x   8 = 8**1
  
 64 x  64 = 8**2:
    t1 = elder_age(n_s=m_s=0, n_e=m_e=7)
    t2 = elder_age(n_s=m_s=8, n_e=m_e=15)
    t3 = elder_age(n_s=m_s=16, n_e=m_e=23)
    t4 = elder_age(n_s=m_s=24, n_e=m_e=31)
    t5 = elder_age(n_s=m_s=32, n_e=m_e=39)
    t6 = elder_age(n_s=m_s=40, n_e=m_e=47)
    t7 = elder_age(n_s=m_s=48, n_e=m_e=55)
    t8 = elder_age(n_s=m_s=56, n_e=m_e=63)

    note that the XOR only needs to be done for one half of the square

    donation_time_tile = t1 * 8 + 
                         t2 * 8 + 
                         t3 * 4 + 
                         t4 * 8 +
                         t5 * 8 +
                         t6 * 8 +
                         t7 * 4 +
                         t8 * 8








512 x 512


"""
