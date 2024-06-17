def to_cs(ts):
    us = ts.split(":")
    sec = us[-1].split(".")

    us[-1] = sec[0]    
    cs = 0
    for u in us:
       cs = 60 * cs
       cs = cs + int(u)
    cs = cs * 100
    if len(sec) > 1:
        cs = cs + int(sec[1])

    return cs

def from_cs(cs):
    cs = round(cs)
    sec = cs % 6000
    min = cs // 6000

    hr = min // 60
    min = min % 60

    return f"{hr:02}:{min:02}:{sec//100:02}.{sec%100:02}"

def average(t1, t2):
    return from_cs((to_cs(t1) + to_cs(t2)) / 2)