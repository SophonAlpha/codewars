def accum(s):
    # repeat characters
    ret = [char*(i+1) for i, char in enumerate(s)]
    # capitalise first character
    ret = [string[0].upper() + string[1:].lower() for string in ret]
    # join with '-'
    ret = '-'.join(ret)
    return ret

print(accum("ZpglnRxqenU"))    # 
print(accum("RqaEzty")) # "R-Qq-Aaa-Eeee-Zzzzz-Tttttt-Yyyyyyy"
print(accum("cwAt"))    # "C-Ww-Aaa-Tttt"
