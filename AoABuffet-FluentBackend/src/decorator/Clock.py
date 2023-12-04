'''
 # @ project: AoABuffet-FluentBackend
 # @ language: Python
 # @ license: MIT
 # @ encoding: UTF-8
 # @ author: Hongqiang Lv | Chenyu Bao | Jian Lin
 # @ date: 2023-07-19 21:04:22
 # @ description: Clock decorator
 '''

import time

def clock(func: "function") -> "function":
    def func_wrapper(*args, **kwargs) -> any:
        start_time: float = time.time()
        result: any = func(*args, **kwargs)
        end_time: float = time.time()
        time_cost: float = end_time - start_time
        print(f"Function {func.__name__} costs {time_cost} seconds.")
        print("----------------------------------------------------------------------------------")
        return result
        pass
    return func_wrapper
    pass

print("decorator: Clock.py is imported.")