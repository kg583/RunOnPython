from keywords import From
from keywords import Import

from punctuation import Asterisk
from punctuation import Space

from util import Casefold
from util import Concat
from util import EmptyString
from util import GetName


@Concat
@Casefold
@GetName
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
