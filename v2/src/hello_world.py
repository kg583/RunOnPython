from builder import Concat
from builder import EmptyString
from builder import Join

from punctuation import Space
from punctuation import ExclamationMark

from slices import Slice5
from slices import Slice7


@Concat
@Join
@Slice5
@list
@reversed
@Slice7
@list
@reversed
@str
class Hello:
    pass


@Concat
@Join
@Slice5
@list
@reversed
@Slice7
@list
@reversed
@str
class World:
    pass


@print
@Hello
@Space
@World
@ExclamationMark
@lambda _: EmptyString
class Main:
    pass
