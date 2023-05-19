import time

def getpbar(w, num, on):
    a = num/on*(w-2)
    if a-int(a) > 0.75:
        h = 3
    elif a-int(a) > 0.50:
        h = 2
    elif a-int(a) > 0.25:
        h = 1
    else:
        h = 0
    bar = ""
    for i in range(w - 2):
        if i < int(a):
            bar += '█'
        elif i == int(a) and h > 0:
            if h == 1:
                bar += '░'
            elif h == 2:
                bar += '▒'
            else:
                bar += '▓'
        else:
            bar += '.'
    return f"[{bar}]"

def getpbar2(w, num, on):
    a = int(num/on*w)
    bar = ""
    for i in range(w):
        if i < int(a):
            bar += '━'
        else:
            bar += '┅'
    return f" {bar}"

"""for i in range(100):
    print("\r"+getpbar(10, i, 100), end = '')
    time.sleep(0.1)"""
