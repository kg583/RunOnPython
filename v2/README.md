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

In fact, this dastardly device can implement `=` all by itself!
```python
@lambda _: OtherThing
class MyThing:
    pass

assert MyThing == OtherThing
```

### Operator? I Hardly...
Like a surgeon diving delicately into the intricate innards of their patient, we will endeavor to `slice` out the good parts of our strings from the bad. Indeed, we can accomplish this since `slice` has multiple arities, and in particular
```python
x[:i] == x.__getitem__(slice(None, i, None)) == x.__getitem__(slice(i))
```

Thus, we can obtain slices from the left, but what about the `__getitem__` call? Well, this is where the unassuming `operator` module enters the scene, armed with two functions that saved this project before it even began: `attrgetter` and `itemgetter`. These beauties were devised for their utility in calls to `map` and its other functional cousins, and are equivalent to
```python
assert attrgetter("x")(y) == y.x
assert itemgetter(x)(y) == y[x]
```
Just look at that currying! I claimed before that *most* built-ins do not admit this kind of design, but these are among the exceptions. They thus allow us to make the following construction:
```python
@itemgetter
@lambda _: 0
class GetTheFirstItem:
    pass
    
@GetTheFirstItem
@str
class ThisIsALeftAngleBracket:
    pass
    
assert ThisIsALeftAngleBracket == "<"
```
And this is just the tip of the iceberg! With `@slice`, we can grab a whole section of the string as desired... except, we can't, at least not in the way we want. Recall that the actual string we want is at the *end* of the representation, and might be preceded by all kinds of gibberish depending on the module. But, if we can slice from the end instead, the amount we have to cut is fixed, namely `'>` at the very end.

We can do this via `reversed`, and then leverage the fact that slicing works just as well on lists:
```python
@itemgetter
@slice
@lambda _: 23
class Slice23:
    pass
    
@itemgetter
@slice
@lambda _: 25
class Slice25:
    pass

@Slice23
@list
@reversed
@Slice25
@list
@reversed
@str
class ThisIsAStringOfLength23:
    pass
```
But wait, we don't get a string out in the end! It's just a darn list of characters! And you know what that means...

## `/attribute`
This part's pretty easy to piece together. We've already got all the ingredients: `attrgetter`, `itemgetter`, and a little ol' friend called `dir`. We can mix these together into a delicious attribute-accessing parfait, complete with all of your favorite string methods and functions.

Let's get a hold of `str.__add__` first, since it's pretty easy:
```python
@attrgetter
@next
@iter
@dir
@lambda _: str
class StrDotAdd:
    pass
```
We use it by attaching it to one string (i.e. decorating the class with the first operand), then calling the attachment on the other. Recall our use of carefully-chosen `slice`s:
```python
@StrDotAdd
@Slice4
@list
@reversed
@Slice6
@list
@reversed
@str
class Left:
    pass

@Left
@Slice5
@list
@reversed
@Slice7
@list
@reversed
@str
class Right:
    pass

assert Right == "LeftRight"
```

### Joining The Cause

Our good friend `str.join` is a bit stranger; we need to first bind it to the empty string so we can join up our lists of characters with no separators. We'll get a hold of the empty string using another clever slice:
```python
@Slice0
@str
class EmptyString:
    pass
```

Now we need `join` itself, which lives at index 56 inside `dir(str)`:
```python
@itemgetter
@lambda _: 56
class GetItem56:
    pass

@attrgetter
@GetItem56
@dir
@lambda _: str
class StrDotJoin:
    pass

@StrDotJoin
@Slice0
@str
class EmptyDotJoin:
    pass
```
And voila! We can reconnect our lists of characters from earlier, and thus revel in our ability to construct arbitrary strings. Just add up the parts, using `chr` where necessary to nab punctuation, and we're done!

### Putting it all together

 While building code strings is quite the pain, a multitude of modules have been built to make the process much more streamlined, all of which can be found in `v2/src`:

* `build`: your basic string-building operations
* `itemgetters`: item nabbers from 0 to 99
* `keywords`: every non-identifier keyword
* `punctuation`: every ASCII punctuation mark
* `slices`: slicers from 0 to 99

Take a look at the sample programs to see how to best combine these tools into barely-readable code.

## How Can I Write Run-on Python?

In contrast to `v4`, a transpiler for `v2` code is actually decently doable. Only some very basic components are required in any given program, with the rest easy to generate on-the-fly by simply reading any given program as a string.  Some care would need to be taken for imports, proper namespacing, and generally `exec` tomfoolery, but that can be pushed to the user.

If such a transpiler ever comes to exist, it will appear here. Otherwise, enjoy writing Run-on Python by-hand and utilizing your precious moments on this Earth to create something truly ridiculous.