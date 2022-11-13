from operator import attrgetter
from operator import itemgetter


from itemgetters import GetItem34
from itemgetters import GetItem56

from slices import Clear


@attrgetter
@GetItem34
@dir
@lambda _: str
class CasefoldTemplate:
    pass


@CasefoldTemplate
@lambda _: str
class Casefold:
    pass


@attrgetter
@next
@iter
@dir
@lambda _: str
class Concat:
    pass


@Clear
@str
class EmptyString:
    pass


@attrgetter
@GetItem56
@dir
@lambda _: str
class JoinTemplate:
    pass


@JoinTemplate
@lambda _: EmptyString
class Join:
    pass
