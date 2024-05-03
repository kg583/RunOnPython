# Run-on Python

## Minimizing Punctuation in Python

There are lots of punctuation marks that can appear in Python code. Strictly speaking, *any* punctuation mark can appear inside a string literal, but that's not really part of Python's *syntax*, as such marks won't actually mean anything to the interpreter[^1].

[^1]: I'm well aware of f-strings and its predecessors, but those are once again *syntactic* elements of the language.

Thus, this project considers all *single* punctuation marks that are syntactically valid *outside* of string literals. As of release 3.11[^2][^3], they are

`! " # % & ' () * + , - . / : ; < = > @ [] \ ^ {} | ~`

Compositions of two or three of the above symbols, like `+=` or `...`, are just that, compositions, and are not taken to be distinct marks. However, we will have to ensure that all valid compositions are also unnecessary.

[^2]: If [PEP-645](https://peps.python.org/pep-0645/) is accepted, which it rightly should, then `?` would enter the mix.
[^3]: `_` is not a punctuation mark, but rather an identifier (and thus more or less a letter). Though `string` thinks it *is* punctuation...

So the question is: how many of the above 28 punctuation marks are *necessary* to write any and all Python code?

As far as I can reason, the answer is ***four***: `()`, `:`, and `*`, a measly ***two***: `@` and `:`, or just ***one***: `:`, depending on the liberties you take along the way. Let's go over some of those.

## Our Mission Statement

### To `exec` or Not To `exec`

Let's make it clear exactly what the goal is here. When I first started this project, I knew I had to avoid `exec` and its cousins at all costs; it was already the key to minimizing the space of *all* characters to execute arbitrary code, as shown [here](https://codegolf.stackexchange.com/questions/110648/fewest-distinct-characters-for-turing-completeness).

This is extraordinarily boring, as wrapping all your code inside a string literal (and a hard-to-read one at that!) almost defeats the point, as one could simply write code as they always do and read the file into an encoder. There's no meat to the problem, not to mention that such code is unparseable by your favorite IDE.  So, we weren't allowed to wrap everything up in a string and call it a day.

*However*, as I experimented with the use of decorators to forego explicit function calls, I realized that `exec` could actually save the day. See, the normal way to use `exec` to hack your way to universality requires *three* punctuation marks, `()` and `+`, to chain `chr` calls together, obtaining any character you need using only digits.

As I discovered, though, we can bring ourselves down to only two, `@` and `:`, to build those kinds of constructions. Now, this is where the judgment call comes in: using the three punctuation marks needed to normally use `exec` in a minimal way is, frankly, boring. Meanwhile, working down to two is, in my opinion, much trickier and fun. Thus, I decided to bring `exec` back for the show, to finally attain the true minimum of Python punctuationlessness. 

So, a rift was formed: `exec` was banned on one side, and glorified on the other. If you want to check out the original machinations, Run-on Python v4, head to `v4/`; there you will find the original text of `README.md`, which explains how to weasel your way into punctuation nirvana *without* `exec`. If you'd like to make Guido cry even more, and see how just two will do, you can check out Run-on Python v2 in `v2/`, which has an accompanying `README.md`.

Both directories also include helper code that can be imported for use in other programs (see `util/`). This helper code includes a number of useful constructs for the respective Run-on Python version, written entirely within their own constraints.

### Some Common Bonds

Despite this rift, there are still some common principles underlying all of Run-on Python's code. Most important of them is the ability to emulate *any* possible Python syntax or construction. This doesn't mean that *everything* will be possible (most things certainly won't be), but that *anything* can be approximated well enough in form and function. For example, Run-on Python v4 dives into how to ditch the `=` sign in code, replacing it with `__eq__` calls and `__setitem__` on the dictionary of variables. These substitutions match the function of `=` (and `==`) *exactly*, at the interpreter level.

But what about default function arguments? You'd say there's no way to emulate those with some funky magic method, and you'd be correct. However, we can still *approximate* the form and function of default arguments by explicitly passing `None` in our calls (which is what the interpreter is doing under the hood!). We can then write our functions like
```python
def foo(bar, baz):
    print(bar)
    print(baz if baz is not None else "Default argument!")
```

This is just one small example of what Run-on Python is trying to do: let you write whatever code you want, but your keyboard is broken in a very specific way that doesn't let you type punctuation, and thus force you to take some creative liberties in getting that code to behave the same way.

Of course, "behave the same way" is a bit subjective sometimes, as one could claim that a Turing machine can "behave" identically to any Python program. You'd be right, but you'd also be very wrong: a Turing machine has no variables, nor classes, nor functions, nor printing to `stdout`. Being able to compute anything is not quite enough.

Basically, one should be able to take any existing Python code, make some (probably several) adjustments, and obtain Run-on Python code (v2 or v4) that does the same thing in the same ways. Capiche? Cool, let's do it.

## Wait, Didn't You Mention Using Just One?

I did. Recently, some of the lovely competitors on [code.golf](https://code.golf/) were intrigued by this project's premise. Within 24 hours, golfer extraordinaire @Lydxn devised the following contraption to perform arbitrary string execution with just one punctuation mark, `:`, and a single copy of it at that:
```python
from builtins import eval as __path__
from binascii import unhexlify as __getattr__
from __main__ import efbbbf7072696e74282248656c6c6f2c20776f726c64212229 as code
class __getattr__:
  from builtins import exec as __contains__
  from random import seed as __init__
from __main__ import _ as C
code in C
```

This code is a work of art, everything I could ever hope `v1` to be and more, but I nonetheless hesitate slightly to consider it the end-all of this project's endeavors.

Firstly, you may notice that the code of interest is stored as a hex string in an identifier; we'll employ this trick in `v2` to save some time and headaches, but the idea of it being strictly _necessary_ is not quite my cup of tea.

Secondly, two external-but-builtin packages are utilized to "run" the compressed code. The way they are used, and the exploitation of the `import` system in general, is a stroke of genius, but reliance on pure Python code which does _not_ conform to our rules is troubling. We'll see that `v2` itself requires the `operator` package, though, so plenty of slack should be cut in this regard; then again, `v4` needs none of this fiddling.

But at the end of the day, I love this code. And I love `v4`, and I love `v2`, and you should too. Something about journeys and destinations, and something else about the good, the bad, and the ugly.

## Some Other Notes

This challenge came to me in an afternoon, partly inspired by [pyfuck](https://github.com/wanqizhu/pyfuck). There's no good reason to ever write code this way, but it's kinda funny. Shoutout to @commandblockguy, @iPhoenix, and @LogicalJoe for comments and discussion on this monstrosity as it developed.

I'll update the utilities whenever I feel like it, and thus they may not exactly conform to any details I happen to give in the corresponding READMEs. Let it be an exercise for the coder to deduce exactly what everything is doing.

In particular, if I haven't gotten around to it yet, stuff may be broken because classes contain more magic methods by default than they used to. Adding (or subtracting, if you're downgrading your Python version) one or two to the index being fetched in the attribute fetchers should resolve things.
