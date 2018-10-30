"""

My solution for Become Immortal kata:
https://www.codewars.com/kata/become-immortal

Level: 1 kyu

"""
import timeit
import numpy as np

def elder_age(m_s, m_e, n_s, n_e, l, t):
    rows, cols = np.array(np.meshgrid(np.arange(n_s, n_e),
                                      np.arange(m_s, m_e))).reshape(2, -1)
    mask = np.zeros(len(rows), dtype=bool)
    mask[[8, 16, 17, 24, 25, 26, 32, 33, 34, 35, 40, 41, 42, 43, 44, 48, 49,
          50, 51, 52, 53, 56, 57, 58, 59, 60, 61, 62]] = True
    rows = rows[mask]
    cols = cols[mask]

    # upper triangle    
    xor_arr = np.bitwise_xor(rows, cols)
    trans_loss = np.subtract(xor_arr, l)
    trans_loss[trans_loss < 0] = 0
    utri_time = np.sum(trans_loss)
    # diagonal
    diag_time = (m_s | n_s) - l
    diag_time = diag_time if diag_time >= 0 else 0
    # donate time
    donate_time = (2 * utri_time + 8 * diag_time) % t
    return donate_time

def elder_age2(m_s, m_e, n_s, n_e, l, t):
#     m_s, m_e, n_s, n_e, l, t = 0, 8, 0, 8, 1, 100
    rows, cols = np.array(np.meshgrid(np.arange(n_s, n_e),
                                      np.arange(m_s, m_e))).reshape(2, -1)

    
    xor_arr = np.bitwise_xor(rows, cols)
    trans_loss = np.subtract(xor_arr, l)
    trans_loss[trans_loss < 0] = 0
    donate_time = np.sum(trans_loss) % t
    return donate_time

if __name__ == "__main__":
    print(timeit.timeit('elder_age(0, 8, 0, 8, 1, 100)',
                        'from __main__ import elder_age, elder_age2',
                        number=10000))
    print(timeit.timeit('elder_age2(0, 8, 0, 8, 1, 100)',
                        'from __main__ import elder_age, elder_age2',
                        number=10000))
