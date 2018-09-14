def namelist(names):
    ret_str = ''
    s = [e['name'] for e in names]
    if len(s) > 1:
        ret_str = ', '.join(s[:-1]) + ' & ' + s[-1]
    if len(s) == 1:
        ret_str = s[0]
    return ret_str

print(namelist([{'name': 'Bart'}, {'name': 'Lisa'}, {'name': 'Maggie'}]))
print(namelist([{'name': 'Bart'},{'name': 'Lisa'}]))
print(namelist([{'name': 'Bart'}]))
print(namelist([]))