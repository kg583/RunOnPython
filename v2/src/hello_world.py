from util import attrgetter
from util import itemgetter

from util import str︳__add__
from util import str︳join


@itemgetter
@slice
@lambda _: 5
class Slice5:
    pass


@itemgetter
@slice
@lambda _: 7
class Slice7:
    pass


@str︳__add__
@str︳join
@Slice5
@list
@reversed
@Slice7
@list
@reversed
@str
class Hello:
    pass


@str︳__add__
@Hello
@chr
@lambda _: 32
class Space:
    pass


@str︳__add__
@Space
@str︳join
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
@World
@chr
@lambda _: 33
class ExclamationPoint:
    pass
