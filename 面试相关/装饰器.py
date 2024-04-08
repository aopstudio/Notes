from typing import Callable

def decorator(fn: Callable):
    def wrapper(*args,**kwargs):
        fn_name = fn.__name__
        print(f'{fn_name} start')
        result = fn(*args,**kwargs)
        print(f'{fn_name} end')
        return result
    return wrapper
@decorator
def simple_plus(a,b):
    return a+b

f1 = decorator(simple_plus)
result = f1('1','2')
print(result)

for i in range(5):
    pass