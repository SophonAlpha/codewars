"""
Visualisation Module for nonogram solver.
"""


def show(nonogram_ones, nonogram_zeros, col_clues, row_clues):
    nonogram = [[' ', ] * len(col_clues) for _ in row_clues]
    nonogram = transform_bin2str(nonogram,
                                 nonogram_ones,
                                 nonogram_zeros)
    # transform column clues

    col_clues = transform_col_clues(col_clues)
    # transform row clues
    row_clues_strs = transform_row_clues(row_clues)
    nonogram_view = [' ' * (len(row_clues_strs[0]) + 1) + line
                     for line in col_clues]
    for idx, row in enumerate(nonogram):
        nonogram_view.append(
            row_clues_strs[idx] + '|' + '|'.join([' ' + item + ' '
                                                  for item in row]) + '|'
        )
    # print nonogram
    for line in nonogram_view:
        print(line)


def transform_col_clues(clues):
    col_clues_rows = max([len(clue) for clue in clues])
    col_clues = clues[:]
    col_clues = [(0,) * (col_clues_rows - len(item)) + item
                 for item in col_clues]
    col_clues = zip(*[item for item in col_clues])
    col_clues = [[str(item) if item != 0 else ' '
                  for item in line] for line in col_clues]
    col_clues = [' '.join([str(item).rjust(2, ' ') + ' ' for item in line])
                 for line in col_clues]
    return col_clues


def transform_row_clues(clues):
    row_clues = [', '.join([str(item) for item in clue])
                 for clue in clues]
    row_clue_max = max([len(item) for item in row_clues])
    row_clues = [' ' * (row_clue_max - len(item)) + item + ' '
                 for item in row_clues]
    return row_clues


def transform_bin2str(nonogram, nonogram_ones, nonogram_zeros):
    num_cols = len(nonogram[0])
    fmt = '{0:0' + str(num_cols) + 'b}'
    for row, item in enumerate(nonogram_ones):
        for col, cell in enumerate(fmt.format(item)):
            nonogram[row][col] = cell if cell == '1' \
                else nonogram[row][col]
    for row, item in enumerate(nonogram_zeros):
        for col, cell in enumerate(fmt.format(item)):
            nonogram[row][col] = '0' if cell == '1' \
                else nonogram[row][col]
    return nonogram