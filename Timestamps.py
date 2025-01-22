def to_ms(ts):
    us = ts.split(":")
    sec = us[-1].replace(",", ".").split(".")

    us[-1] = sec[0]
    ms = 0
    for u in us:
       ms = 60 * ms
       ms = ms + int(u)
    ms = ms * 1000
    if len(sec) > 1:
        ms = ms + round(int(sec[1]) * 10**(3 - len(sec[1])))

    return ms

def from_ms(ms):
    ms = round(ms)
    sec = ms % 60000
    min = ms // 60000

    hr = min // 60
    min = min % 60

    return f"{hr:02}:{min:02}:{sec//1000:02}.{sec%1000:03}"

def average(t1, t2):
    return from_ms((to_ms(t1) + to_ms(t2)) / 2)
