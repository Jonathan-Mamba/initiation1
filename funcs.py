import math

def add(a, b):
    return a + b 

def sub(a, b):
    return a - b

def mult(a, b):
    return a * b

def pow(a,b):
    return a ** b

def div(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return math.inf

def fdiv(a, b):
    try:
        return a // b
    except ZeroDivisionError:
        return math.inf

def mod(a, b):
    try:
        return a % b
    except ZeroDivisionError:
        return math.inf