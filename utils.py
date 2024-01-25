#!/usr/bin/env python3

def dict_filter(f, d)-> dict: return { k : v for k, v in d.items() if f(k, v)}

def dict_contains(d1, d2):
    count = len(d2)
    for k, v in d1.items():
        if count <= 0: return True
        if (k, v) in d2.items():
            count -= 1
    return False

def intersperse(l: list, value):
    result = []
    if len(l) == 0: return []
    for i in range(0, len(l)):
        result.append(l[i])
        if i != len(l) - 1:
            # we are not on last element
            result.append(value)
    return result
