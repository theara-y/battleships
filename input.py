import string

def parseInput(s):
    s = s.strip()
    size = len(s)
    if size < 1 or size > 3:
        return False
    
    s = s.upper()
    letter = ''
    number = ''
    for c in s:
        if c in 'ABCDEFGHIJ':
            letter += c
        elif c in string.digits:
            number += c
    if len(letter) != 1:
        return False
    if len(number) < 1 or len(number) > 2:
        return False
    if number not in ['1','2','3','4','5','6','7','8','9','10']:
        return False
    
    y = int(number) - 1
    x = ord(letter) - ord('A')
    return (y, x)