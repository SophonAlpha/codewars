"""

My solution for Become Immortal kata:
https://www.codewars.com/kata/become-immortal

Level: 1 kyu

"""
import numpy as np
np.seterr(over='raise')

def elder_age(m, n, l, t):
    donate_time = 0
    total_loss = 0
    m, n = (m, n) if m > n else (n, m)
    m_start, n_start = 0, 0
    m_end, n_end = m, n
    while n_start != n_end:
        dm = m_end - m_start
        dn = n_end - n_start
        m_level = largest_sqare_tile(dm)
        n_level = largest_sqare_tile(dn)
        dm = divmod(dm, 8**m_level)[0] * 8**m_level
        dn = divmod(dn, 8**n_level)[0] * 8**n_level
        cell_value = m_start ^ n_start
        level = max(m_level, n_level)
        time, loss = tile_time(m_start, dm, n_start, dn, cell_value, level, l)
        donate_time += time
        total_loss += loss
        m_start = m_start + dm
        m_end = m
        if m_start == m_end:
            m_start, n_start = 0, n_start + dn
            m_end, n_end = m, n
    donate_time = donate_time - total_loss
    donate_time = donate_time % t
    return donate_time

def largest_sqare_tile(size):
    exp = 1
    if size < 8**exp:
        return 0
    while True:
        fit, _ = divmod(size, 8**(exp + 1))
        if fit == 0:
            break
        exp += 1
    return exp

def tile_time(m_start, dm, n_start, dn, sub_sum, level, l):
    if dn > dm:
        m_start, dm, n_start, dn = n_start, dn, m_start, dm
    xor_arr = [value ^ n_start 
               for value in range(m_start, m_start + 8**(level + 1), 8**level)]
    if level > 0:
        sub_m_start = m_start + xor_arr.index(min(xor_arr)) * 8**level
        sub_sum = sub_tile_sum(dm, dn, sub_m_start, n_start, 0, level)
    else:
        sub_sum = m_start ^ n_start
    if dm > 8**level:
        positions = [(value - min(xor_arr))//8**level for value in xor_arr]
        rows = min(dn, 8**level)
        delta = (sum_seq(8**level, 8**level + 8**level - 1) - \
                 sum_seq(0, 8**level - 1)) * rows
        xor_arr = [(value * delta) + sub_sum for value in positions]
        val_col = divmod(dm, 8**level)[0]
        val_row = max(1, divmod(dn, 8**level)[0])
        xor_arr = map_row_to_array(xor_arr, val_row, val_col)
        time = sum([sum(row) for row in xor_arr])
    else:
        time = sub_sum
    loss = calculate_loss(m_start, dm, n_start, dn, level, l)
    return time, loss

def sub_tile_sum(dm, dn, m_start, n_start, sub_sum, level):
    if level > 1:
        xor_arr = [value ^ n_start 
                   for value in range(m_start, m_start + 8**level,
                                      8**(level - 1))]
        sub_dm = min(dm, 8**level)
        sub_dn = min(dn, 8**level)
        sub_m_start = m_start + xor_arr.index(min(xor_arr)) * 8**(level - 1)
        sub_sum = sub_tile_sum(sub_dm, sub_dn, sub_m_start, n_start, 
                               sub_sum, level - 1)
        positions = [(value - min(xor_arr))//8**(level - 1) for value in xor_arr]
    else:
        xor_arr = [value ^ n_start for value in range(m_start, m_start + 8)]
    tile_rows = divmod(dn, 8**(level - 1))[0]
    tile_rows = 1 if tile_rows == 0 else tile_rows
    tile_rows = 8 if tile_rows > 8 else tile_rows
    cell_rows = min(dn, 8**(level - 1))
    if level > 1:
        delta = (sum_seq(8**(level - 1),
                         8**(level - 1) + 8**(level - 1) - 1) - \
                 sum_seq(0, 
                         8**(level - 1) - 1)) * cell_rows
        xor_arr = [(value * delta) + sub_sum for value in positions]
    time = sum(xor_arr) * tile_rows
    return time

def map_row_to_array(row, num_rows, num_cols):
    VALUE_MAP = [[0, 1, 2, 3, 4, 5, 6, 7],
                 [1, 0, 3, 2, 5, 4, 7, 6],
                 [2, 3, 0, 1, 6, 7, 4, 5],
                 [3, 2, 1, 0, 7, 6, 5, 4],
                 [4, 5, 6, 7, 0, 1, 2, 3],
                 [5, 4, 7, 6, 1, 0, 3, 2],
                 [6, 7, 4, 5, 2, 3, 0, 1],
                 [7, 6, 5, 4, 3, 2, 1, 0]]
    array = []
    for row_index in range(0, num_rows):
        new_row = [row[VALUE_MAP[row_index][col_index]] 
                   for col_index in range(0, num_cols)]
        array.append(new_row)
    return array

def calculate_loss(m_start, dm, n_start, dn, level, l):
    cols = divmod(dm, 8**level)[0]
    cols = cols if cols > 0 else 1
    xor_arr = [value ^ n_start
               for value in range(m_start, m_start + 8**(level + 1), 8**level)]
    if level > 1:
        for index, value in enumerate(xor_arr[:cols]):
            if value <= l <= value + 8**level - 1:
                sub_m_start = value
                break
        sub_dm = min(dm, 8**level)
        sub_dn = min(dn, 8**level)
        sub_loss = calculate_loss(sub_m_start, sub_dm, n_start, sub_dn, level - 1, l)
        loss = sub_loss + \
               (cols - 1 - index) * 8**(level - 1)**2 * l * \
               dn
    else:
        seq_start = min(xor_arr[:cols])
        seq_end = min(l, seq_start + dm)
        all_below_loss = sum_seq(seq_start, seq_end) if seq_end > seq_start else 0
        if seq_end > seq_start:
            all_above_loss = ((seq_start + dm) - (min(l, seq_start + dm) + 1)) * l
        else:
            all_above_loss = dm * l
        no_rows = dn
        loss = (all_below_loss + all_above_loss) * no_rows
    return loss

def sum_seq(a_1, a_n):
    """
    Calculate sum of arithmetic sequence.
    """
    n = a_n - a_1 + 1
    return int((n * (a_1 + a_n)) / 2)

def xor_sum(m_s, m_e, n_s, n_e):
    rows, cols = np.array(np.meshgrid(np.arange(n_s, n_e, dtype=object), np.arange(m_s, m_e, dtype=object)))
    xor_arr = np.bitwise_xor(rows, cols)
    sum = np.sum(xor_arr)
    return sum

def loss_array(m_s, m_e, n_s, n_e, l, t):
    rows, cols = np.array(np.meshgrid(np.arange(n_s, n_e, dtype=object), np.arange(m_s, m_e, dtype=object)))
    xor_arr = np.bitwise_xor(rows, cols)
    trans_loss = np.subtract(xor_arr, l)
    trans_loss[trans_loss < 0] = 0
    loss = np.subtract(np.sum(xor_arr), np.sum(trans_loss))
    donate_time = np.sum(trans_loss) % t
    return np.sum(xor_arr), loss, donate_time

if __name__ == "__main__":
    print(elder_age(545, 435, 342, 1000007))
