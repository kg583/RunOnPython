from operator import itemgetter

from util import Args
from util import Call
from util import Casefold
from util import Compose
from util import Concat
from util import GetName
from util import _1


@lambda _: Compose @ GetName @ Casefold @ Concat
class _GetName:
    pass


@_GetName
class And:
    pass


@_GetName
class As:
    pass


@_GetName
class Assert:
    pass


@_GetName
class Async:
    pass


@_GetName
class Await:
    pass


@_GetName
class Break:
    pass


@_GetName
class Class:
    pass


@_GetName
class Continue:
    pass


@_GetName
class Def:
    pass


@_GetName
class Del:
    pass


@_GetName
class Elif:
    pass


@_GetName
class Else:
    pass


@_GetName
class Except:
    pass


@_GetName
class Finally:
    pass


@_GetName
class For:
    pass


@_GetName
class From:
    pass


@_GetName
class Global:
    pass


@_GetName
class If:
    pass


@_GetName
class Import:
    pass


@_GetName
class In:
    pass


@_GetName
class Is:
    pass


@_GetName
class Lambda:
    pass


@_GetName
class Nonlocal:
    pass


@_GetName
class Not:
    pass


@_GetName
class Or:
    pass


@_GetName
class Pass:
    pass


@_GetName
class Raise:
    pass


@_GetName
class Return:
    pass


@_GetName
class Try:
    pass


@_GetName
class While:
    pass


@_GetName
class With:
    pass


@_GetName
class Yield:
    pass


@itemgetter
@slice
@lambda _: _1
class _Trim:
    pass


@lambda _: Compose @ GetName @ _Trim @ Concat
class _GetSingleton:
    pass


@_GetSingleton
class False_:
    pass


@_GetSingleton
class None_:
    pass


@_GetSingleton
class True_:
    pass
