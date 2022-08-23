# Run-on Python v2

## Decorator? I Hardly Know Her!
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

### One Is The Lonelist Number
Despite their utility, decorators have one absolutely devastating flaw: they only take one argument, no more, no less. This eliminates *most* built-ins from our workspace, including non-unary operators. How can we continue?

Well, you first may cry, "But I've seen decorators take arguments!" Indeed you probably have, but not in the way that you think, and this will kill our efforts to use them for two reasons. Decorators do support the syntax `@[name]([args])`, but pay attention to how this is actually defined. Consider a decorator which repeats a function some number of times before returning:
```python
@repeat(times=3)
def divide_by_8(x):
    return x // 2
    
assert divide_by_8(72) == 9
```
But how do we *define* `repeat`? Recall that decorators (usually) take a function as an argument and return another function:
```python
def repeat(times):
    def inner(func):
        def repeater(x):
            for _ in range(times):
                x = func(x)
                
            return x
            
        return repeater
        
    return inner
```
Just look at that nesting! Very very few built-ins do anything close to this, so we'd have to define such a decorator ourselves. But remember, we're trying to get rid of `()`! We can't possibly define our own decorators[^1], let alone call a decorator with arguments in the first place.

[^1]: To anybody who just thought about `lambda`s, pat yourself on the back, but also see if you can define a decorator that actually does something useful.

### An Executive Order
With a heavy heart, I posit that we need `exec` to continue; it's the only way to call *n*-ary functions, despite our having to build them into a string to do so. But we should not get so hung up on this lamentable inclusion, for by its hand our journey to punctuation nirvana can continue. And besides, we don't have to worry too much about it until the end; we just need to focus on building arbitrary strings, which is still plenty of fun.

## Hack and Slash

Unsurprisingly, the easiest way to build arbitrary strings is to use `@str`. Specifically, we'll make use of the fact that every object in Python has a string representation obtainable from `str`[^2]. Our strategy will then be to acquire various string methods to slice up and connect these strings, then `exec` the whole thing. Let's get crackin'.

[^2]: *Technically*, this is handled by `repr`, which is in fact what *should* be used in the case of objects that override `__str__` for reasonable purposes. Our classes, however, don't, so we'll stick with the shorter call.

### Staying Classy
For objects that don't have a canonical string representation (e.g. functions), Python makes do with something like this:
```python
assert str(my_func) == "<function '__main__.my_func'>"
```
where `__main__` is simply whatever module contains the function (in this case, the top-level one). This is all well and good, but some of you have probably been screaming your heads off for the past few paragraphs: function definitions require parentheses! Fear not, for decorators can decorate another, friendlier set of objects: classes. Classes come with the bonus of not requiring any parentheses to define, as an empty class is simply
```python
class Foo:
    pass
```
It's string representation is similar:
```python
assert str(Foo) == "<class '__main__.Foo'>"
```

The bottom line is that we've got our class name in the string representation, but it's surrounded by a bunch of other fluff that we'll need to excise. We'll also need to deal with punctuation marks, as those by definition cannot appear in identifiers. The latter, however, is not too hard using `chr` and some clever little `lambda` constructs that became available in 3.9:
```python
@chr
@lambda _: 32
class ThisIsASpace:
    pass
    
assert ThisIsASpace == " "
```
### Operator? I Hardly...
Like a surgeon diving delicately into the intricate innards of their patient, we will endeavor to `slice` out the good parts of our strings from the bad. Indeed, we can accomplish this since `slice` has multiple arities, and in particular
```python
x[:i] == x.__getitem__(slice(None, i, None) == x.__getitem__(slice(i))
```

Thus, we can obtain slices from the left, but what about the `__getitem__` call? Well, this is where the unassuming `operator` module enters the scene, armed with two functions that saved this project before it even began: `attrgetter` and `itemgetter`. These beauties were devised for their utility in calls to `map` and its other functional cousins, and are equivalent to
```python
assert attrgetter("x")(y) == y.x
assert itemgetter(x)(y) == y[x]
```
Just look at that currying! I claimed before that *most* built-ins do not admit this kind of design, but these are among the exceptions.
