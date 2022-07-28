# Run-on Python

## Minimizing Punctuation in Python
There are lots of punctuation marks that can appear in Python code. Strictly speaking, *any* punctuation mark can appear inside a string literal, but that's not really part of Python's *syntax*, as such marks won't actually mean anything to the interpreter[^1].

[^1]: I'm well aware of f-strings and its predecessors, but those are once again *syntactic* elements of the language.

We also don't want our code to be all inside a string literal itself and use `exec`; the reason for this restraint is two-fold:
1. [It's already been done.](https://codegolf.stackexchange.com/questions/110648/fewest-distinct-characters-for-turing-completeness)
3. We want our code to be writable in your favorite IDE; wrapping it all in a string ditches any attempts at highlighting or lexical analysis.

Thus, this project considers all *single* punctuation marks that are syntactically valid *outside* of string literals and *without* the need for `exec` or any of its cousins. As of release 3.10[^2][^3], they are

`! " # % & ' () * + , - . / : ; < = > @ [] \ ^ {} | ~`

Compositions of two or three of the above symbols, like `+=` or `...`, are just that, compositions, and are not taken to be distinct marks. However, we will have to ensure that all valid compositions are also unnecessary.

[^2]: If [PEP-645](https://peps.python.org/pep-0645/) is accepted, which it rightly should, then `?` would enter the mix.
[^3]: `_` is not a punctuation mark, but rather an identifier (and thus more or less a letter).

So the question is: how many of the above 28 punctuation marks are *necessary* to write any and all Python code?

As far as I can reason, the answer is just ***four***: `()`, `:`, and `*`.

## The Main Tricks
We'll first establish the most important tricks in removing punctuation from your code. These will actually do most of the heavy lifting for us when it comes to removing marks, particularly any and all operators.

### Everything is Magic
Every operator in Python is converted into a certain *magic method call* when interpreted.
* `x % y` becomes `x.__mod__(y)`
* `x += y` becomes `x.__iadd__(y)`

and so on[^4]. You can find a list of all of them and their correspondences [here](https://docs.python.org/3/reference/datamodel.html).

[^4]: Sometimes these default to the *right* operand, becoming `y.__rmod__(x)`, but this is hardly relevant to our purposes.

But it should be evident that this fact lets us ditch every operator right from the get-go, since they get effectively removed anyway.

### Everything is `getattr`
In removing every operator, we've made it almost abundantly necessary to have a `.` at our disposal, as this is how we interface with the magic methods (and indeed, any class methods at all). However, Guido must've had our particular endeavor in mind all those years ago, as we are graced with the `getattr` and `setattr` methods. These methods are the true backbones of Python, as we have the following equivalences:
* `x.y` becomes `getattr(x, "y")`
* `x.y = z` becomes `setattr(x, "y", z)`

So not only is `.` out of the picture, `=` appears to be as well; we just need a way to set a simple local variable, one that isn't an attribute. Luckily, local variables are actually stored in a giant dictionary, `locals()`[^5], that we can modify using `__setitem__`. That is, we have
* `x = y` becomes `locals().__setitem__("x", y)` becomes `getattr(locals(), "__setitem__")("x", y)`

[^5]: Or sometimes `globals()`.

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

The coup-de-grace is then Python's wonderful fellow `*`, the unpacking operator. Luckily, almost every operator is binary, so we don't need to do many more shenanigans to get all the boilerplate arguments we need into a tuple.
```python
getattr(x, "y") == getattr(*tuple("y" if i else x for i in range(2)))
```
and thus
```python
(x, y, z) === getattr(*tuple("__add__" if i else tuple(y if i else x for i in range(2)) for i in range(2)))(tuple(z for _ in range(1)))
```

### You Knew `chr` Was Coming
Alright, we've (almost completely) taken care of every mark on our list except `"`. Luckily, we can turn to the `chr` function to save the day: this little bugger takes in an ASCII code as an integer and returns the corresponding character. Thus, we can build up any string we like using only `()`, as `chr` is a single-argument function[^6].

[^6]: One word about currying and I'm privating this repo.

```python
getattr(x, "y") == getattr(*tuple(chr(121) if i else x for i in range(2)))
```

As with tuples, any length of string is possible in principle, but becomes horribly messy once it needs to be written out. The use of `chr` also allows us to get disallowed punctuation inside strings, even if we don't necessarily care that they are there to begin with.

## How To Make Like a Poet and Rid Yourself of Punctuation
We will now systematically go through each of our 24 excess marks to reason why they are not necessary. Buckle up, cause this could take a while.

### `!`
* `!=` is equivalent to `__neq__`.

### `"`
* **String literals** can be built using `chr`.
* **Docstrings** are never necessary to run code, and are entirely ignored by the interpreter.
* **f-strings** can always be implemented directly.

### `#`
* **Comments** are never necessary to run code, and are entirely ignored by the interpreter.
  
### `%`
* `%` is equivalent to `__mod__`.
* `%=` is equivalent to `__imod__`.
* **Format strings** that use `%` can be identically achieved using f-strings.

### `&`
* `&` is equivalent to `__and__`.
* `&=` is equivalent to `__rand__`.

### `'`
* `'` is equivalent to `"`, which we know is moot.

### `+`
* `+` is equivalent to `__add__` as a binary operator and `__pos__` as a unary operator.
* `+=` is equivalent to `__iadd__`.

### `,`
* Multiple **function arguments** can be replaced by a single, iterable argument.
* Raw **iterables** can be constructed using the ternary tuple trick.
* Multiple **globals** or **nonlocals** on a single line can simply be split into multiple lines.
* Multiple **imports** on a single line can simply be split into multiple multiple lines. [PEP 8](https://peps.python.org/pep-0008/) even says you *should*.
* **Unpacking** can always be done across multiple lines or statements.
* **Multidimensional slices** are passed as tuples of `slice` objects into `__getitem__`, which can be resolved using known tricks.
* `with` statements with multiple **targets** are [semantically equivalent](https://docs.python.org/3/reference/compound_stmts.html#the-with-statement) to nestings of singular targets.

### `-`
* `-` is equivalent to `__sub__` as a binary operator and `__neg__` as a unary operator.
* `-=` is equivalent to `__isub__`.
* **Return type hints** are never necessary for function definitions.

### `.`
* **Attributes** can be accessed via `getattr` and `setattr`.
* **Decimals** can be written by `__div__`-ing integers by powers of 10, which will have the same viable precision as standard specification of floats.
* **Relative imports** can be translated into calls to `__import__`.
* **Ellipses** are equivalent to the identifier `Ellipsis`.

### `/`
* `/` is equivalent to `__div__` (or `__truediv__` if you're [messing about in 2.7](https://docs.python.org/2.7/reference/datamodel.html#object.__truediv__)).
* `/=` is equivalent to `__idiv__` (or `__itruediv__`).
* `//` is equivalent to `__floordiv__`.
* `//=` is equivalent to `__ifloordiv__`.
* **Positional-only parameters** are never necessary for function definitions.

### `;`
* **Newlines** are always sufficient to end a line, rendering `;` entirely unnecessary and really just a holdover for the C plebs.

### `<`
* `<` is equivalent to `__lt__`.
* `<=` is equivalent to `__le__`.
* `<<` is equivalent to `__lshift__`.
* `<<=` is equivalent to `__ilshift__`.

### `=`
* `==` is equivalent to `__eq__`.
* **Assignments** can be replaced by direct calls to `__setitem__` in `locals()` or `globals()`.
* **Class definitions** are equivalent to `type`.
* **Default function arguments** can be replaced with explicit passes of `None` followed by replacements in the function body.

### `>`
* `>` is equivalent to `__gt__`.
* `>=` is equivalent to `__ge__`.
* `>>` is equivalent to `__rshift__`.
* `>>=` is equivalent to `__irshift__`.

### `@`
* `@` is equivalent to `__matmul__`.
* **Decorators** are equivalent to calls to explicit outer functions.

### `[]`
* **List literals** can be built from tuples.
* **Subscripting** and **slicing** are equivalent to `__getitem__` and `__setitem__`.
* **Type hints** are never necessary for function definitions or assignment statements.

### `\`
* **Escape sequences** can be replaced by explicit `chr` calls.

### `^`
* `^` is equivalent to `__xor__`.
* `^=` is equivalent to `__ixor__`.

### `{}`
* **Dictionary literals** can be built from tuples of tuples.
* **Set literals** can be built from tuples.

### `|`
* `|` is equivalent to `__or__`.
* `|=` is equivalent to `__ior__`.

### `~`
* `~` is equivalent to `__inv__`.

## Can We Do Any Better?
With only four punctuation marks remaining, it seems unlikely we can get rid of any more. Indeed, I posit that this is true:
* `()` are the only way to do function calls. Seems like a no-brainer that those have to stay.
* `:` is required for just about every control flow construct. Also pretty necessary.
  * *If* you're okay with using a Turing-complete subset of Python, then I think you can dodge `:` by living entirely inside tuple comprehensions. However, this subset doesn't give you functions or classes, and feels definitely out of the spirit of this whole shebang.
* `*` is very powerful, enabling us to drop `,` among other things. Unpacking is just too good to pass up.
  * Of course, keeping `,` over `*` is *much* cleaner, but dodging `,` is just too much fun.

Thus, I do claim that four is the best we can do. Anyone clever enough to prove otherwise is more than welcome to do so.

## How Can I Write Run-on Python?
I'm glad you asked. At the moment there are plans for a transpiler which can walk a given Python AST and burn away those blasphemous punctuation marks, but no implementation is yet available. Some parts are pretty easy, such as recognizing instances where we can use one of our primary tricks. Other snippets are much trickier if the user isn't kind, requiring more complex restructuring of the AST before compiling back down to valid code.

It's almost certainly doable in its entirety though, and if enough people pester me about it it'll get written. But for now, you can use this spec to write such code yourself, and make the world a slightly more confusing place.

## Some Final Notes
This challenge came to me in an afternoon, partly inspired by [pyfuck](https://github.com/wanqizhu/pyfuck). There's no good reason to ever write code this way, but it's kinda funny. If you have anything to add to the discussion, feel free to do it here.
