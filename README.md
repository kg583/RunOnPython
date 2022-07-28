# Run-on Python

## Minimizing Punctuation in Python
There are lots of punctuation marks that can appear in Python code. Strictly speaking, *any* punctuation mark can appear inside a string literal, but that's not really part of Python's *syntax*, as such marks won't actually mean anything to the interpreter[^1].

We also don't want our code to be all inside a string literal itself and use `exec`; the reason for this restraint is two-fold:
1. [It's already been done.](https://codegolf.stackexchange.com/questions/110648/fewest-distinct-characters-for-turing-completeness)
3. We want our code to be writable in your favorite IDE; wrapping it all in a string ditches any attempts at highlighting or lexical analysis.

Thus, this project considers all *single* punctuation marks that are syntactically valid *outside* of string literals and *without* the need for `exec` or any of its cousins. As of release 3.10[^2], they are

`! " # % & ' () * + , - . / : ; < = > @ [] \ ^ {} | ~`

Compositions of two or three of the above symbols, like `+=` or `...`, are just that, compositions, and are not taken to be distinct marks.

So the question is: how many of the above 28 punctuation marks are *necessary* to write any and all Python code?

As far as I can reason, the answer is just ***four***: `()`, `:`, and `*`.

[^1]: I'm well aware of f-strings and its predecessors, but those are once again *syntactic* elements of the language.
[^2]: If [PEP-645](https://peps.python.org/pep-0645/) is accepted, which it rightly should, then `?` would enter the mix.

## The Main Tricks
We'll first establish the most important tricks in removing punctuation from your code. These will actually do most of the heavy lifting for us when it comes to removing marks, particularly any and all operators.

### Everything is Magic
Every operator in Python is converted into a certain *magic method call* when interpreted.
* `x % y` becomes `x.__mod__(y)`
* `x += y` becomes `x.__iadd__(y)`

and so on. You can find a list of all of them and their correspondences [here](https://docs.python.org/3/reference/datamodel.html).

But it should be evident that this fact lets us ditch every operator right from the get-go, since they get effectively removed anyway.

### Everything is `getattr`
In removing every operator, we've made it almost abundantly necessary to have a `.` at our disposal, as this is how we interface with the magic methods (and indeed, any class methods at all). However, Guido must've had our particular endeavor in mind all those years ago, as we are graced with the `getattr` and `setattr` methods. These methods are the true backbones of Python, as we have the following equivalences:
* `x.y` becomes `getattr(x, "y")`
* `x.y = z` becomes `setattr(x, "y", z)`

So not only is `.` out of the picture, `=` appears to be as well; we just need a way to set a simple local variable, one that isn't an attribute. Luckily, local variables are actually stored in a giant dictionary, `locals()`, that we can modify using `__setitem__`. That is, we have
* `x = y` becomes `locals().__setitem__("x", y)` becomes `getattr(locals(), "__setitem__")("x", y)`

What's most interesting about the above is that there is a sense in which `x = y` *literally means* the expanded form on the right. Overiding `__setitem__` for the built-in `dict` class would apply, as would messing about with `getattr` (both of which are highly frowned upon outside shenanigans like this).

### The Pythonic Comma
Now surely, we must be insane to think we can be rid of the `,`. Every call to `getattr` requires one, and `setattr` needs two! But fear not, for there is one more trick up our sleeve: the ternary operator.

In C and its many children, the ternary operator looks like `a ? b : c`, which means "evaluate `a`, and return `b` if it is True and `c` otherwise".

Python being the little rascal that it is managed to forego punctuation altogether for its version: `b if a else c`.

We can now employ the ternary operator to replace the comma in the following way. First, we use it to construct two-element tuples (or lists, whichever you fancy):
```python
(x, y) == tuple(y if i else x for i in range(2))
```

Note the subtlety of this trick: we have to use the truthiness of `i = 1` to distinguish `x` and `y` in the tuple construction *without relying on any other operators*, as otherwise we'd be right back to needing a comma in the function call!

Next, we construct longer tuples. We'll simply use the `__add__` method for tuples along with the tricks we already know:
```python
(x, y, z) === getattr(tuple(y if i else x for i in range(2)), "__add__")(tuple(z for _ in range(1)))
```
We can extend this indefinitely, and also make it a bit less messy by using local variables (i.e. `locals()` members) along the way.

The coup-de-grace is then Python's wonderful fellow `*`, the unpacking operator. Luckily, almost every operator is binary, so we don't need to do many more shenanigans to get all the arguments we need into a tuple.
```python
getattr(x, "y") == getattr(*tuple("y" if i else x for i in range(2)))
```
and thus
```python
(x, y, z) === getattr(*tuple("__add__" if i else tuple(y if i else x for i in range(2)) for i in range(2)))(tuple(z for _ in range(1)))
```

## How To Make Like a Poet and Rid Yourself of Punctuation
We will now systematically go through each of our 24 excess marks to reason why they are not necessary.
