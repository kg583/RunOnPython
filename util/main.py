class F:
  def __add__():
    pass
  
  def __getitem__():
    pass
  
  def __setitem__():
    pass
  
  
def tup(first):
  def inner(second):
    return tuple(second if i else first for i in range(2))
  return inner

def advance(num):
  def inner(iterator):
    for _ in range(num):
      next(iterator)
    return iterator
  return inner

def get_value(name):
  return getattr(*tup(globals())(next(advance(10)(iter(dir(F))))))(name)

def set_value(name):
  def inner(value):
    return getattr(*tup(globals())(next(advance(24)(iter(dir(F))))))(*tup(name)(value))
  return inner

set_value(chr(65))(next(iter(dir(F)))))
set_value(chr(71))(next(advance(10)(iter(dir(F)))))
set_value(chr(83))(next(advance(24)(iter(dir(F)))))

set_value(chr(79))(range(1))
set_value(chr(84))(range(2))

def build(t):
  def first(left):
    def second(right):
      return getattr(*tup(t)(A))(*tup(left)(right))
    return second
  return first
