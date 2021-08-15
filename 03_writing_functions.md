
## Writing functions in Python
**Best practices**
```py
# Docstring - Google style
def function(arg_1, arg_2=42, some_function):
    """Descriptioin of what this function does.

    Args:
        arg_1 (str): Description of arg_1.
            (The string to search).
        arg_2 (int, optional): Write optional when
            argument has default value.
        some_function (callable): The function we want a tooltip for.

    Returns:
        bool: Optional description of the return value.
        Extra lines not indedted.
    
    Raises: 
        ValueError: Include any type of error that the function raises.

    Notes:
        See https://......com for more usage.
        import inspect
        doc = inspect.getdoc(function)
    """
```
```py
# DRY - Do one thing!
# Use functions to avoid repetition.
# Problem: it does multiple things. First, it loads the data. Then it plots the data. You must write seperate functions for them.

# Pass by argument
def foo(var=None): # do not write: var=[]
    if var is None:    
        var = []  
    var.append(1)
    return var
foo()
```

**Context managers** --> initialize, enter, exit --> CONNECT/DISCONNECT, OPEN/CLOSE
```py
"""with"""
# how to write? class-based or function-based.
# Python generator --> yield
@contextlib.contextmanager
def my_context():
    print('hello')
    yield 42 
    print('finished')

with my_context() as foo: # we use 'as' cuz my_context kind of returns yield 42
    print(f'foo is {foo}') # foo is 42

"""nested context manager"""
with stock('NVDA') as nvda:
  # Open "NVDA.txt" for writing as f_out
  with open('NVDA.txt', 'w') as f_out:
    for _ in range(10):
      value = nvda.price()
      print('Logging ${:.2f} for NVDA'.format(value))
      f_out.write('{:.2f}\n'.format(value))
    # Opening stock ticker for NVDA
    # Logging $139.50 for NVDA
    # Logging $139.54 for NVDA
    # Logging $139.61 for NVDA
    # Closing stock ticker

"""try/except/finally to be ensure to finish (close file or disconnect printer) even error"""
def get_printer(ip):
    p = connect_to_printer(ip)

    try:
        yield
    finally:
        p.disconnect()
        print('disconnected from printer')
```

**Functions & Closure**
```py
"""Function = object"""
# 1. Function is object, just reference them to variable
def my_functon():
    print('Hello')
x = my_functon # DO NOT INCLUDE ()
x() # Hello

# 2. List of functions
list_of_funcs = [my_function, open, print] # can also transform to dict
list_of_funcs[2]("Wow working")

# 3. Function as argument
def has_docstring(func):
    """Check to see if function has doc.
    """
    return func.__doc__ is not None
def yes():
    """Returns value 42.
    """
    return 42
has_docstring(yes)

# 4. Function as return values
def get_function():
    def print_me(s):
        print(s)
    return print_me

new_func = get_function()
new_func('This is a sentence')
```
```py
"""Closure"""
def return_a_func(arg1, arg2):
  def new_func():
    print('arg1 was {}'.format(arg1))
    print('arg2 was {}'.format(arg2))
  return new_func
    
my_func = return_a_func(2, 17)

print(my_func.__closure__ is not None)
print(len(my_func.__closure__) == 2)

# Get the values of the variables in the closure
closure_values = [
  my_func.__closure__[i].cell_contents for i in range(2)
]
print(closure_values == [2, 17])
```
**Decorators**
- <img src="img/python_decorator.png" width=300>
- Decorator = wrapper -> modify input, modify output, modify function
- **We should have the same parameters inside wrapper like our function!**
- https://realpython.com/primer-on-python-decorators/
```py
# Template to reuse
import functools

def decorator(func):
    @functools.wraps(func)
    def wrapper_decorator(*args, **kwargs):
        # Do something before
        value = func(*args, **kwargs)
        # Do something after
        return value
    return wrapper_decorator
```
```py
"""Decorator"""
def double_args(func):
    def wrapper(a, b):
        return func(a * 2, b * 2)
    return wrapper

@double_args # same as new_multiply = double_args(multiply)
def multiply(a, b):
    return a * b

multiply(2, 3)
```
```py
"""Anvanced decorator"""
from functools import wraps

def timer(func):
  """A decorator that prints how long a function took to run."""
  @wraps(func)
  def wrapper(*args, **kwargs):
    # When wrapper() is called, get the current time.    
    t_start = time.time()
    # Call the decorated function and store the result.    
    result = func(*args, **kwargs)
    # Get the total time it took to run, and print it.    
    t_total = time.time() - t_start    
    print('{} took {}s'.format(func.__name__, t_total))
    return result
 return wrapper
```
- `duplicate.__wrapped__(3, 5)` - call the original function instead of the decorated one
```py
"""Decorators with arguments"""
# we have to turn it into a function that returns a decorator, rather than a function that is a decorator

# instead of writing decorator function for only 4, we can do for values n
def repeat(num_times):
    def decorator_repeat(func):
        @functools.wraps(func)
        def wrapper_repeat(*args, **kwargs):
            for _ in range(num_times):
                value = func(*args, **kwargs)
            return value
        return wrapper_repeat
    return decorator_repeat

@repeat(num_times=4)
def greet(name):
    print(f"Hello {name}")

greet("World")

"""Project: HTML Generator"""
# instead of doing seperately for bold, italic, we can do like below
def html(open_tag, close_tag):
  def decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
      msg = func(*args, **kwargs)
      return '{}{}{}'.format(open_tag, msg, close_tag)
    # Return the decorated function
    return wrapper
  # Return the decorator
  return decorator

@html("<b>", "</b>")
def hello(name):
  return 'Hello {}!'.format(name)
  
print(hello('Alice'))
```

