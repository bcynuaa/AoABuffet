'''
 # @ Author: bcynuaa
 # @ Create Time: 2023-07-07 13:27:27
 # @ Description: python decorator
 '''

import time

split_line = "------------------------------------------------------------------------------------"

def clock(func):
    def timer(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print(f"{func.__name__} cost {time.time() - start} seconds.")
        print(split_line)
        return result
        pass
    return timer
    pass

print("utils: Decorator is imported.")