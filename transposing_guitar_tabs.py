import re

def transpose_v3(amount, tab):
    
    fret_pos = {}
    pattern = re.compile('[0-9]+')
    for i in range(len(tab)):
        pos = 0
        match = True
        while match:
            match = pattern.search(tab[i], pos)
            if match:
                # transpose fret
                fret = match.group(0)
                new_fret = int(fret) + amount
                new_fret_len = len(str(new_fret))
                # check if out of frets
                if new_fret > 22 or new_fret < 0:
                    return 'Out of frets!'
                # replace old with new fret in the tablature
                tab[i] = tab[i][:match.start()] + \
                                str(new_fret) + \
                                tab[i][match.end():]
                pos = match.start() + new_fret_len
                # save new fret position and length for later
                # padding of the other tab strings
#                pad_len = new_fret_len - len(str(fret))
                if match.start() in fret_pos.keys():
                    if fret_pos[match.start()] < new_fret_len:
                        # we save the length of the fret with most
                        # characters
                        fret_pos[match.start()] = new_fret_len
                else:
                    fret_pos[match.start()] = new_fret_len

    # add additional '-' padding characters if character
    # length for a fret has increased in any string
#    pad_cols = {col:fret_pos[col] for col in fret_pos.keys() if fret_pos[col] > 0}
    for col in fret_pos.keys():
        for i in range(len(tab)):
            match = pattern.match(tab[i], col)
            if match:
                pad_len = fret_pos[col] - (match.end() - match.start())
                tab[i] = tab[i][:match.start()] + \
                        tab[i][match.start():match.end()] + '-' * pad_len +\
                         tab[i][match.end():]
            else:
                pad_len = fret_pos[col] - 1 # there is already one '-'
                tab[i] = tab[i][:col] + '-' * pad_len + \
                         tab[i][col:]
    
    print()
    
    return tab

def transpose(amount, tab):
    
    # get start and end of all frets
    fret_pos = {}
    for string in tab:
        for match in re.finditer('[0-9]+', string):
            if match.start() in fret_pos.keys():
                if fret_pos[match.start()] < match.end():
                    fret_pos[match.start()] = match.end()
            else:
                fret_pos[match.start()] = match.end()
                
    # process each column that contains frets
    for fret_start in sorted(fret_pos):
        fret_end = fret_pos[fret_start]
        # get all sub strings from one column
        col = [string[fret_start:fret_end] for string in tab]
        # apply amount to all frets
        col_width = 0
        for i, fret in enumerate(col):
            new_fret = re.search('[0-9]+', fret)
            if new_fret:
                new_fret = int(new_fret.group(0)) + amount
                if new_fret > 22 or new_fret < 0:
                    return 'Out of frets!'
                if len(str(new_fret)) > col_width:
                    col_width = len(str(new_fret))
                col[i] = str(new_fret)
        # apply padding to other rows where needed
        for i, row in enumerate(col):
            if len(row) < col_width:
                col[i] = col[i] + '-' * (col_width - len(row))
            if len(row) > col_width:
                col[i] = col[i][:col_width - len(row)]
        # add modified column back to tablature
        tab_new = []
        for i, row in enumerate(col):
            tab_new.append(tab[i][:fret_start] + row + tab[i][fret_end:])

    print('end of transpose')
    return tab_new

def transpose_v1(amount, tab):
    pattern = re.compile('[0-9]+')
    for i in range(len(tab)):
        pos = 0
        while True:
            match = pattern.search(tab[i], pos)
            if match:
                # transpose fret
                new_fret = int(match.group(0)) + amount
                # check if out of frets
                if new_fret > 22 or new_fret < 0:
                    return 'Out of frets!'
                tab[i] = tab[i][:match.start()] + \
                                str(new_fret) + \
                                tab[i][match.end():]
                pos = match.start() + len(str(new_fret))
                # shift frets in other lines if necessary
                len_diff = len(str(new_fret)) - len(match.group(0))
                lines = list(range(len(tab)))
                lines.remove(i)
                if len_diff > 0:
                    for l in lines:
                        tab[l] = tab[l][:match.end()] + \
                                 '-' * len_diff + \
                                 tab[l][match.end():]
                if len_diff < 0:
                    for l in lines:
                        tab[l] = tab[l][:match.start()-len_diff] + \
                                 tab[l][match.end():]
            else:
                break
    return tab

t = transpose(2, [
'e|--------5-7-----7-|-8-----8-2-----2-|-0---------0-----|-----------------|',
'B|-10---5-----5-----|---5-------3-----|---1---1-----1---|-0-1-1-----------|',
'G|----5---------5---|-----5-------2---|-----2---------2-|-0-2-2-----------|',
'D|-12-------6-------|-5-------4-------|-3---------------|-----------------|',
'A|------------------|-----------------|-----------------|-2-0-0---0--/8-7-|',
'E|------------------|-----------------|-----------------|-----------------|'])        

print(t)

"""

t = transpose(-1, [
'e|-----------------|---------------|----------------|------------------|',
'B|-----------------|---------------|----------------|------------------|',
'G|--0---3---5----0-|---3---6-5-----|-0---3---5----3-|---0----(0)-------|',
'D|--0---3---5----0-|---3---6-5-----|-0---3---5----3-|---0----(0)-------|',
'A|-----------------|---------------|----------------|------------------|',
'E|-----------------|---------------|----------------|------------------|'])

t = transpose(+2, [
'e|----------5/6-6-6-5/6-6-6-6-6-6------------------------------------|',
'B|-------6--5/6-6-6-5/6-6-6-6-6-6-9-8-6-6----------------------------|',
'G|---6h7--------------------------------6h7--------------------------|',
'D|-8----------------------------------------8-6--8-8-8-8-8-8-8-8-----|',
'A|-----------------------------------------------8-8-8-8-8-8-8-8-----|',
'E|-------------------------------------------------------------------|'])

print(t)
"""

"""

'e|-----------7/8-8-8-7/8-8-8-8-8-8-----------------------------------------------|',
'B|--------8--7/8-8-8-7/8-8-8-8-8-8-11-10-8-8-------------------------------------|',
'G|----8h9----------------------------------8h9-----------------------------------|',
'D|-10------------------------------------------10-8--10-10-10-10-10-10-10-10-----|',
'A|---------------------------------------------------10-10-10-10-10-10-10-10-----|',
'E|-------------------------------------------------------------------------------|'

"""
