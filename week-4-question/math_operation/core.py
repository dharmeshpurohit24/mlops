class DivisionError(Exception):
    pass

def addition(a,b):
    return a+b

def subraction(a,b):
    return a-b

def multiplication(a,b):
    return a*b

def division(a,b):
    if b == 0:
        raise DivisionError("Cannot divide by zero")
    return a/b
