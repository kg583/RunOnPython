from builder import Casefold
from builder import Concat
from builder import EmptyString
from builder import Join

from keywords import From
from keywords import Import

from punctuation import Asterisk
from punctuation import Space

from slices import Slice4
from slices import Slice6


@Concat
@Casefold
@Join
@Slice4
@list
@reversed
@Slice6
@list
@reversed
@str
class Math:
    pass


@exec
@From
@Space
@Math
@Space
@Import
@Asterisk
@lambda _: EmptyString
class FromMathImportAll:
    pass
