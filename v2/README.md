# Run-on Python v2

## Decorator? I hardly know 'er!
If you read the main `README.md` and are at least decently familiar with Python, you should be able to guess exactly how we're gonna accomplish our goals. If not, though, a quick refresher.

### Oh Honey Honey
A *decorator* is usually described as a device that modifies some existing function. The syntax is `@[name]`, which appears just above a function definition. For example, in the following class, we use `@property` to turn a standard getter method into one that doesn't need to be called:
```python
class Foo:
    def my_value(self):
        return 7
	
    @property
    def my_property(self):
        return 7
		
print(Foo().my_value())
print(Foo().my_property)
```

However,the key fact about decorators is that they are just sugar; namely, decorator syntax is precisely equivalent to the following:
```python
my_property = property(my_property)
```
(Kudos if you knew that `property` was a built-in function)

Furthermore, the decorator is allowed to be *anything* callable; it doesn't need to return a first-class function. For example,
```python
@str
def my_func():
    print("Off I go!")
	
assert isinstance(my_func, str)
```

Perhaps this is enough to predict where we are headed. If not, then a final reminder: decorators can be chained.
```python
@list
@str
def my_func():
    print("Off I go!")

assert isinstance(my_func, list)
```
This will permit us to do some very abhorrent things to our functions; in particular, we can compose functions without making explicit calls, granting us nearly the full power of functional programming.
