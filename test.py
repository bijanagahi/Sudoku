def say_hi()->int:
    print("hi!")
    return 5

x:list[callable] = [say_hi] # type: ignore

y:int = x[0]()
print(y)
print(x[0].__name__)