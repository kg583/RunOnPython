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

### Joining the Cause

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

### We Need To Go Deeper

Armed with crude but arbitrary string execution, we can bootstrap our way to more powerful constructs. Each of these steps is executed for-realsies in `v2/src/util`, wherein you can import any you like to build your barely-readable code. And while I may have a penchant for the simplistic model of decorator chaining == string concatenation, any substantial code simply deserves better.

First, we'll pick up some methods to turn hex strings into not-hex strings:
```python
@attrgetter
@GetItem43
@dir
@lambda _: bytes
class _FromHex:
    pass

@_FromHex
@lambda _: bytes
class FromHex:
    pass

@attrgetter
@GetItem39
@dir
@lambda _: bytes
class _Decode:
    pass

@_Decode
@lambda _: bytes
class Decode:
    pass
```

Next, we'll make a helper function to evaluate a hex string derived from an integer literal (in hex, so it at least _might_ fit on the screen). This helper, naturally, calls what will become itself on itself:
```python
@iter
@hex
@lambda _: 0x6c616d626461205f3a6576616c2862797465732e66726f6d6865782866227b5f3a787d22292e6465636f6465282929
class _EvalHex:
    pass

@eval
@Decode
@FromHex
@Join
@list
@lambda _: _EvalHex
@next
@lambda _: _EvalHex
@next
@lambda _: _EvalHex
class EvalHex:
    pass
```

The assembly is subtle: we use `next` twice to skip the leading `0x` from `hex()`, then consume the rest of the iterator into a `list`, as `str(iter(foo))` is the string representation of `iter(foo)` (which isn't very useful).

Now we can `EvalHex` whatever we'd like to execute worse and worse code. While we'd like to avoid using it too much, lest our programs become truly unreadable, but it does make our next trick much easier: matrix multiplication.

### Seriously, Why Is This Here?

In the distant past of 2014, [it was decided](https://peps.python.org/pep-0465/) that Python should have a matrix multiplication operator. In a stroke a punning, its symbol is `@`, which proves unreasonably convenient for the task at hand. By defining classes which implement `__matmul__`, we can perform _binary_ operations without any extra punctuation _or_ resorting to hex strings!

The general approach will be to use `@lambda _:` decorators, as they can have arbitrary expressions as bodies. We'll start each expression with the class whose operator we'd like to use, followed by a list of `@` operations. The class will collect the results of the operations, reducing left-associatively so that the `__matmul__` calls always succeed. For example, the `Args` class collects each subsequent element into a list:
```python
@lambda _: Args @ 1 @ 2 @ 3
class Example:
    pass
```

If we call `Example` on an argument, it will splat those elements into a function call of that argument:
```python
@Example
@lambda _: print
class Function:
    pass
```

The `util` package contains many more fantastic Matthew Mullers; their exact usage and syntax is left as an exercise to the programmer. You can also find other shortcuts like `GetName`, which takes the headache out of reverse-slicing your way to the name of a class. All of this amounts to a surprising breadth of possible paradigms for writing Run-on Python, so please do run and explore with wild abandon.

## How Can I Write Run-on Python?

In contrast to `v4`, a transpiler for `v2` code is actually decently doable. Only some very basic components are required in any given program, with the rest easy to generate on-the-fly by simply reading any given program as a string.  Some care would need to be taken for imports, proper namespacing, and generally `exec` tomfoolery, but that can be pushed to the user.

If such a transpiler ever comes to exist, it will appear here. Otherwise, enjoy writing Run-on Python by-hand and utilizing your precious moments on this Earth to create something truly ridiculous.