from util import Concat
from util import EmptyString
from util import GetName

from punctuation import Space
from punctuation import ExclamationMark


@Concat
@GetName
class Hello:
    pass


@Concat
@GetName
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
