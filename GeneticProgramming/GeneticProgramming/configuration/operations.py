import math
import sys


def safe_add(x, y):
    try:
        return min(max(x + y, -sys.float_info.max), sys.float_info.max)
    except OverflowError:
        return sys.float_info.max if x > 0 else -sys.float_info.max


def safe_sub(x, y):
    try:
        return min(max(x - y, -sys.float_info.max), sys.float_info.max)
    except OverflowError:
        return sys.float_info.max if x > 0 else -sys.float_info.max


def safe_mul(x, y):
    try:
        return min(max(x * y, -sys.float_info.max), sys.float_info.max)
    except OverflowError:
        return sys.float_info.max if x > 0 else -sys.float_info.max


def safe_div(x, y):
    if y == 0:
        return 0
    try:
        return min(max(x / y, -sys.float_info.max), sys.float_info.max)
    except OverflowError:
        return sys.float_info.max if x > 0 else -sys.float_info.max


def safe_exp(x):
    try:
        return min(math.exp(min(x, 709)), sys.float_info.max)
    except OverflowError:
        return sys.float_info.max


def safe_sqr(x):
    try:
        if abs(x) > math.sqrt(sys.float_info.max):
            return sys.float_info.max
        return x ** 2
    except OverflowError:
        return sys.float_info.max


ops = {
    '+': {'func': safe_add, 'arity': 2, 'weight': 1},
    '-': {'func': safe_sub, 'arity': 2, 'weight': 1},
    '*': {'func': safe_mul, 'arity': 2, 'weight': 1},
    '/': {'func': safe_div, 'arity': 2, 'weight': 1},
    'exp': {'func': safe_exp, 'arity': 1, 'weight': 0.5}
}