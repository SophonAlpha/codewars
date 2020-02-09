USE_BREAK_DISPLAY = True

v = lambda c: {(c[0] + 1, c[1]), (c[0] - 1, c[1])}
h = lambda c: {(c[0], c[1] + 1), (c[0], c[1] - 1)}
neig = lambda c: {(c[0] + 1, c[1]), (c[0] - 1, c[1]), (c[0], c[1] + 1), (c[0], c[1] - 1)}
neig2 = lambda c: {(c[0] + i, c[1] + j) for i in {1, -1, 0} for j in {1, -1, 0}}


def break_evil_pieces(shape):
    if not shape.strip():
        return []
    (rows, cols, shape) = interpolate(shape)
    S = {(i, j) for i in range(rows) for j in range(cols) if shape[i][j] == ' '}
    regions = []
    while S:
        R = {S.pop()}
        R_ = R
        while R_:
            R_ = {j for i in R_ for j in neig(i) & S} - R
            R.update(R_)
        S = S - R
        boundary = {j for i in R for j in neig2(i)} - R
        min_i = min(i for i, j in boundary)
        max_i = max(i for i, j in boundary) + 1
        min_j = min(j for i, j in boundary)
        max_j = max(j for i, j in boundary) + 1
        if min_i < 0 or min_j < 0 or max_i > rows or max_j > cols:
            continue
        region = [list(row[min_j:max_j]) for row in shape[min_i:max_i]]
        for i in range(len(region)):
            for j in range(len(region[i])):
                if region[i][j] != ' ' and (i + min_i, j + min_j) not in boundary:
                    region[i][j] = ' '
                elif region[i][j] == '+':
                    c = (i + min_i, j + min_j)
                    if not (h(c) & boundary and v(c) & boundary):
                        region[i][j] = '-' if h(c) & boundary else '|'
        regions.append('\n'.join(''.join(row[::2]).rstrip() for row in region[::2]))
    return regions


def interpolate(s):
    shape = s.split('\n')
    while not shape[0].strip():
        shape = shape[1:]
    while not shape[-1].strip():
        shape = shape[:-1]
    lines = len(shape)
    max_line_len = max(len(shape[i]) for i in range(lines))
    for row in range(lines):
        shape[row] += ' ' * (max_line_len - len(shape[row]))
    new_shape = [[]] * (2 * lines - 1)
    for row in range(2 * lines - 1):
        new_shape[row] = [' '] * (2 * max_line_len - 1)
        if row % 2:
            for col in range(max_line_len):
                if shape[row // 2][col] in '|+' and shape[row // 2 + 1][col] in '|+':
                    new_shape[row][2 * col] = '|'
        else:
            for col in range(2 * max_line_len - 1):
                if col % 2:
                    if shape[row // 2][col // 2] in '-+' and shape[row // 2][col // 2 + 1] in '-+':
                        new_shape[row][col] = '-'
                else:
                    new_shape[row][col] = shape[row // 2][col // 2]
    return 2 * lines - 1, 2 * max_line_len - 1, new_shape


if __name__ == '__main__':
    INPUT_SHAPE = """
    +--+
    |  |
    +--+
    """.strip('\n')

    ALL_PIECES = break_evil_pieces(INPUT_SHAPE)
    for counter, text_piece in enumerate(ALL_PIECES):
        print('\n{}.) piece:\n'.format(counter))
        print(text_piece)
    print()
