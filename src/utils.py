def break_lines(string, nMax):
    pieces = []
    while string:
        pieces.append(string[:nMax-1].lstrip())
        string = string[nMax-1:]
    return '\n'.join(pieces)
