'''
#Function = object
def my_functon():
    print('Hello')
x = my_functon
print(x()) # Hello'''

"""
def foo():
    a = 5
    def two():
        a = 10
        return a

    return two(), a

bla = foo()
bla
"""


'''
def foo():
    a = 5
    def two():
        a = 10
        print(a)
    print("foo")
    return two

bla = foo()
bla() # bla() because nested
'''

'''x = 25
def foo(x):
    def bar():
        print(x)
    return bar

x = foo(x)
x()
'''

"""

IMPORTANT:

##################### 1
def my_special_function():
  print('You are running my_special_function()')
  
def get_new_func(func):
  def call_func():
    func()
  return call_func

new_func = get_new_func(my_special_function)

# Redefine my_special_function() to just print "hello"
def my_special_function():
  print("hello")

new_func() # You are running my_special_function()'

##################### 2
def my_special_function():
  print('You are running my_special_function()')
  
def get_new_func(func):
  def call_func():
    func()
  return call_func

new_func = get_new_func(my_special_function)

# Delete my_special_function()
del(my_special_function)

new_func() # You are running my_special_function()

################## 3 
def my_special_function():
  print('You are running my_special_function()')
  
def get_new_func(func):
  def call_func():
    func()
  return call_func

# Overwrite `my_special_function` with the new function
my_special_function = get_new_func(my_special_function)

my_special_function() # You are running my_special_function()
"""



def test():
  test.rustam += 10
  print("Hello", test.rustam)

test.rustam = 0

test()