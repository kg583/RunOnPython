# Run-on Python v4

## The Main Tricks
We'll first establish the most important tricks in removing punctuation from your code. These will actually do most of the heavy lifting for us when it comes to removing marks, particularly any and all operators.

### Everything is Magic
Every operator in Python is converted into a certain *magic method call* when interpreted.
* `x % y` becomes `x.__mod__(y)`
* `x += y` becomes `x.__iadd__(y)`

and so on[^1]. You can find a list of all of them and their correspondences [here](https://docs.python.org/3/reference/datamodel.html).

[^1]: Sometimes these default to the *right* operand, becoming `y.__rmod__(x)`, but this is hardly relevant to our purposes.

But it should be evident that this fact lets us ditch every operator right from the get-go, since they get effectively removed anyway.

### Everything is `getattr`
In removing every operator, we've made it almost abundantly necessary to have a `.` at our disposal, as this is how we interface with the magic methods (and indeed, any class methods at all). However, Guido must've had our particular endeavor in mind all those years ago, as we are graced with the `getattr` and `setattr` methods. These methods are the true backbones of Python, as we have the following equivalences:
* `x.y` becomes `getattr(x, "y")`
* `x.y = z` becomes `setattr(x, "y", z)`

So not only is `.` out of the picture, `=` appears to be as well; we just need a way to set a simple local variable, one that isn't an attribute. Luckily, local variables are actually stored in a giant dictionary, `locals()`[^2][^3], that we can modify using `__setitem__`. That is, we have
* `x = y` becomes `locals().__setitem__("x", y)` becomes `getattr(locals(), "__setitem__")("x", y)`

[^2]: Or sometimes `globals()`, which will be important later.
[^3]: Or sometimes [not at all](https://docs.python.org/3/library/functions.html#locals).

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

Next, we construct longer tuples. We'll simply use the `__add__` method for tuples along with the tricks we already know[^4]:
```python
(x, y, z) == getattr(*(y if i else x for i in range(2)), "__add__")(tuple(z for _ in range(1)))
```
We can extend this indefinitely, and also make it a bit less messy by using local variables (i.e. `locals()` members) along the way.

[^4]: We can drop `tuple` from unpacking statements, since generators can be unpacked as well, saving us a few letters.

The coup-de-grace is then Python's wonderful fellow `*`, the unpacking operator. Luckily, almost every operator is binary, so we don't need to do many more shenanigans to get all the boilerplate arguments we need into a tuple.
```python
getattr(x, "y") == getattr(*("y" if i else x for i in range(2)))
```
and thus
```python
(x, y, z) == getattr(*("__add__" if i else tuple(y if i else x for i in range(2)) for i in range(2)))(tuple(z for _ in range(1)))
```

In the case of `getattr`, arguably the most common call of all, the built-in `operator` module can also save the day via `attrgetter`:
```python
getattr(x, "y") == operator.attrgetter("y")(x)
```
This particular convenience makes use of inner functions, which will prove to be our best friends further down the road.

### You Knew `chr` Was Coming
Alright, we've (almost completely) taken care of every mark on our list except `"`. Luckily, we can turn to the `chr` function to save the day: this little bugger takes in an ASCII code as an integer and returns the corresponding character. Thus, we can build up any string we like using only `()`, as `chr` is a single-argument function.

```python
getattr(x, "y") == getattr(*(chr(121) if i else x for i in range(2)))
```

As with tuples, any length of string is possible in principle, but we need to be crafty: recall that in order to build longer tuples, we needed the `__add__` method. But in order to access it, we used `getattr(tuple, "__add__")`, which already has a string in it!

The key is the wonderful `dir` function, which returns a list of the *names* every attribute of an object[^5]. By turning this list into an iterator, we can `next` our way to *any* element, and then use that name as the argument to `getattr`! We might need *many* `next` calls, but they are all well within the rules. To keep from relying on the method order of the built-ins[^6], we can define a custom class:

```python
class F:
  def __add__(self):
    pass
  
  def __setitem__(self):
    pass
```

[^5]: Specifically, `dir(foo)` is equivalent to `foo.__dir__`, which *very conveniently* dodges that `.`.
[^6]: This order is alphabetical, but could be adjusted slightly as new methods get added with each release.

Such a class has the added benefit of containing relatively few default methods that get in the way, which you can see by running `dir` on an empty class:

```python
class X:
  pass
  
dir(X) == ['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__']
```

So, once we can nab `__setitem__` and its friends all at once, we have it at our disposal to build arbitrary strings.

### None of This Actually Works

Now, I must be honest with you: the tricks that we've seen so far are great, but we're still quite far from getting something functional. Trying to employ most of them directly fails for two main reasons: nested unpacking and the true meaning of `locals()`.

For reasons that are [purely aesthetic](https://peps.python.org/pep-0448/#variations), Python won't let you unpack within a comprehension. Thus, we can only use our tuple trick once or twice before needing to store the value away; in particular, we can never call a multi-argument function within another multi-argument function call, which really wrecks our ability to use `getattr` well.

Our problems are furthermore compounded by the fact that `locals()` is actually unusable with our new tricks. Consider the following, seemingly identical snippets:

```python
locals().__setitem__("S", "__setitem__")
getattr(*("__setitem__" if i else locals() for i in range(2)))("S", "__setitem__")
```

The first of those lines does exactly what you'd expect: saves `'__setitem__'` to `S` so we can use it later. The second, however, doesn't, because of the following devilish detail: comprehensions define new variable scopes. Once inside a comprehension, `locals()` refers not to the enclosing scope you came from, but the scope of the comprehension itself! Thus, setting the "local" value of `S` is useless, since it does not live outside the comprehension.

Luckily, there's an easy but inelegant fix: use `globals()` instead. Namespace purists may rage, but it's the only option we've got. And now that we've got `globals()`, we can store away values in-between unpackings to keep Guido happy.

### Putting It All Together

So, let's build our way to a working Run-on Python implementation. We've got no classes, long strings, or anything else at our disposal, and we'll also refrain from importing anything at the moment.

We're first gonna want some helper functions. The most crucial is the "twopler", a function with can curry two inputs to build a tuple using the power of inner functions:

```python
def tup(first):
  def inner(second):
    return tuple(second if i else first for i in range(2))
  return inner
```

Thus, we can avoid unpacking within a comprehension, since we won't even be using a raw comprehension to build our tuples!

Next, we'll define a function that can call `next` an arbitrary number of times. Note that we need to do this *without* being able to store the iterator somewhere directly (since we don't have `__setitem__` yet), but luckily we can leverage the fact that functions bind their arguments to their parameter names:

```python
def advance(num):
  def inner(iterator):
    for _ in range(num):
      next(iterator)
    return iterator
  return inner
```

With it, we can nab our method names from the class `F` defined earlier:

```python
'__add__' == next(iter(dir(F)))
'__setitem__' == next(advance(23)(iter(dir(F))))
```

A function that simplifies `__setitem__` calls would also be nice (recall that we have to always use `globals()` for variables):

```python
def set_value(name):
  def inner(value):
    return getattr(*tup(globals())(next(advance(23)(iter(dir(F))))))(*tup(name)(value))
  return inner
```

We can use this helper to put our method names into convenient, single-letter variables, along with `range(1)` and `range(2)` for convenience:

```python
set_value(chr(65))(next(iter(dir(F))))
set_value(chr(83))(next(advance(23)(iter(dir(F)))))

set_value(chr(79))(range(1))
set_value(chr(84))(range(2))
```

Finally, we'll give ourselves the ultimate builder function. This wonderful fellow can assemble *any* iterable that implements `__add__`, most importantly strings; we can use it by first calling with a type and initial value, then each element in order, and then an empty call:
```python
def build(t):
    def init(initial):
        def inner(*element):
            if not element:
                return initial
            return init(getattr(*tup(t)(A))(*tup(initial)(next(iter(element)))))
        return inner
    return init
```

Presto! We've got ourselves an implementation of Run-on Python that isn't completely horrendous to use. You can find all of this code plus some additional helper objects in `src/util/__init__py` (and thus you can import `util` to start your next project!).

Only one last step to round off our endeavor.

## How To Make Like a Poet and Rid Yourself of Punctuation
We will now systematically go through each of our 24 excess marks to reason why they are not necessary. Buckle up, cause this could take a while.

### `!`
* `!=` is equivalent to `__neq__` or `not in` with a singleton tuple.

### `"`
* **String literals** can be built using `chr`.
* **Docstrings** are never necessary to run code, and are entirely ignored by the interpreter.
* **f-strings** can always be implemented directly; `str.format` can also take a bit of the load.

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
* Multiple **function arguments** can be replaced by a single, iterable argument, or by currying with inner functions.
* Raw **iterables** can be constructed using the ternary tuple trick.
* Multiple **globals** or **nonlocals** on a single line can simply be split into multiple lines.
* Multiple **imports** on a single line can simply be split into multiple lines. [PEP-8](https://peps.python.org/pep-0008/) even says you *should*.
* **Unpacking** can always be done across multiple lines or statements.
* **Multidimensional slices** are passed as tuples of `slice` objects into `__getitem__`, which can be resolved using known tricks.
* `with` statements with **multiple targets** are [semantically equivalent](https://docs.python.org/3/reference/compound_stmts.html#the-with-statement) to nestings of singular targets.

### `-`
* `-` is equivalent to `__sub__` as a binary operator and `__neg__` as a unary operator.
* `-=` is equivalent to `__isub__`.
* **Return type hints** are never necessary for function definitions.

### `.`
* **Attributes** can be accessed via `getattr` and `setattr`.
* **Decimals** can be written by `__div__`-ing integers by powers of 10, which will have the same viable precision as standard float literals.
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
* `==` is equivalent to `__eq__` or `in` with a singleton tuple.
* **Assignments** can be replaced by direct calls to `__setitem__` in `locals()` or `globals()`.
* **Class definitions** are equivalent to `type`.
* **Default function arguments** can be replaced with explicit passes of `None` followed by replacements in the function body.
* **Keyword arguments** can be passed using dictionaries.

### `>`
* `>` is equivalent to `__gt__`.
* `>=` is equivalent to `__ge__`.
* `>>` is equivalent to `__rshift__`.
* `>>=` is equivalent to `__irshift__`.

### `@`
* `@` is equivalent to `__matmul__`.
* **Decorators** are equivalent to calls to explicit outer functions.

### `[]`
* **List literals** can be built from tuples or generators.
* **Subscripting** and **slicing** are equivalent to `__getitem__` and `__setitem__` via `slice`.
* **Type hints** are never necessary for function definitions or assignment statements.

### `\ `
* **Escape sequences** can be replaced by explicit `chr` calls.

### `^`
* `^` is equivalent to `__xor__`.
* `^=` is equivalent to `__ixor__`.

### `{}`
* **Dictionary literals** can be built from tuples or generators of tuples.
* **Set literals** can be built from tuples or generators.

### `|`
* `|` is equivalent to `__or__`.
* `|=` is equivalent to `__ior__`.

### `~`
* `~` is equivalent to `__inv__`.

## A Few Objections

* "If everything gets stored in `globals()`, how can you do recursion?"
  * The answer is a call stack or something like it. Surely you've implemented one yourself before, right?
* "How do you dictionaries? Like, actually."
  * Here's a snippet to build the dictionary `d = {0: 1, 2: 3}`:
```python
set_value(chr(100))(dict(tup(tup(0)(1))(tup(2)(3))))
``` 
* "What if you mess with the built-ins?"
  * @iPhoenix devised such examples, but such a point is rather moot, as messing with the built-ins enough breaks Python normally!
  * Thus, this project assumes you're not doing anything heinous *before* getting rid of your punctuation marks.
* "Aren't classes kinda impossible since `self` is always the first argument of a method?"
  * Fear not, for `*args` can save us! The object will get collected just like any other argument, and from there you just need to parse.
  * Here's how to initialize an object that has a member `x` passed as the "first" argument:
```python
class C:
    def __init__(*args):
        setattr(*build(tuple)(tup(next(iter(args)))(chr(120)))(tuple(next(advance(1)(iter(args))) for _ in range(1)))())
        
set_value(chr(99))(C(5))
```
* "I can't access values by their names, what gives?"
  * Oh, yeah... see `set_value` modifies the `globals()` *for `util/__init__.py`*, meaning the interpreter won't be able to find any values set from outside the import by name.
  * Instead, you can use the included `get_value` helper, which accesses the same `globals()` scope and thus can find all your variables at no additional charge.

## Can We Do Any Better?
With only four punctuation marks remaining, it seems unlikely we can get rid of any more. Indeed, I posit that this is true, *if* `exec` is barred from play:
* `()` are the main way to do function calls, and are also the only grouping symbol left. Seems like a no-brainer that those have to stay.
  * As pointed out by @commandblockguy, decorators can also call things, as can the `del` operator, but then we run into the problem of defining those things in the first place.
  * It is also possible to dodge parentheses entirely [in some situations](https://polygl0ts.ch/writeups/2021/b01lers/pyjail_noparens/README.html), again using decorators, but we need to take on even more symbols to make it happen.
* `:` is required for just about every control flow construct. Also pretty necessary.
  * *If* you're okay with using a Turing-complete subset of Python, then I think you can dodge `:` by living entirely inside tuple comprehensions. See the mission statement section for why we're not doing this.
* `*` is very powerful, enabling us to drop `,` among other things. Unpacking is just too good to pass up.
  * Of course, keeping `,` over `*` is *much* cleaner, but dodging `,` is just too much fun.
  * Lambda calculus can also be implemented using only `()` and `:`, but again, that's not Python, just a whole lot of currying.

[^7]: A separate gist of this file (which might later become its permanent home) can be found [here](https://gist.github.com/kg583/74dcf08574bb37f13be6fd978279bd6e).

## How Can I Write Run-on Python?
I'm glad you asked. At the moment there are plans for a transpiler which can walk a given Python AST and burn away those blasphemous punctuation marks, but no implementation is yet available. Some parts are pretty easy, such as recognizing instances where we can use one of our primary tricks. Other snippets are much trickier if the user isn't kind, requiring more complex restructuring of the AST before compiling back down to valid code.

The transpiler is still almost certainly doable in its entirety though, and if enough people pester me about it it'll get written. But for now, you can use this spec to write such code yourself, and make the world a slightly more confusing place.
