from operator import attrgetter
from operator import itemgetter


@itemgetter
@lambda _: 35
class _35:
    pass


@attrgetter
@_35
@dir
@lambda _: str
class _Casefold:
    pass


@_Casefold
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


@itemgetter
@slice
@lambda _: 0
class Clear:
    pass


@Clear
@str
class EmptyString:
    pass


@itemgetter
@lambda _: 57
class _57:
    pass


@attrgetter
@_57
@dir
@lambda _: str
class _Join:
    pass


@_Join
@lambda _: EmptyString
class Join:
    pass


@itemgetter
@lambda _: 43
class _43:
    pass


@attrgetter
@_43
@dir
@lambda _: bytes
class _FromHex:
    pass


@_FromHex
@lambda _: bytes
class FromHex:
    pass


@itemgetter
@lambda _: 39
class _39:
    pass


@attrgetter
@_39
@dir
@lambda _: bytes
class _Decode:
    pass


@_Decode
@lambda _: bytes
class Decode:
    pass


@iter
@hex
@lambda _: 0x6c616d626461205f3a6576616c2862797465732e66726f6d6865782866227b5f3a787d22292e6465636f6465282929
class _EvalHex:
    pass


@eval
@Decode
@FromHex
@Join
@list
@lambda _: _EvalHex
@next
@lambda _: _EvalHex
@next
@lambda _: _EvalHex
class EvalHex:
    pass


@EvalHex
@lambda _: 0x747970652822222c28292c7b225f5f696e69745f5f223a6c616d62646120732c5f3a7365746174747228732c225f222c5f292c225f5f6d61746d756c5f5f223a6c616d62646120732c5f3a732e5f285f292c225f5f726d61746d756c5f5f223a6c616d62646120732c5f3a74797065287329285f297d29
class _Call:
    pass


@_Call
class Call:
    pass


@EvalHex
@lambda _: 0x747970652822222c28292c7b225f5f696e69745f5f223a6c616d62646120732c5f3a7365746174747228732c225f222c5f292c225f5f6d61746d756c5f5f223a6c616d62646120732c5f3a4e6f74496d706c656d656e746564206966206973696e7374616e6365285f2c5f43616c6c29656c7365207479706528732928732e5f2b5b5f5d297d29
class _Builder:
    pass


@EvalHex
@lambda _: 0x747970652822222c285f4275696c6465722c292c7b225f5f63616c6c5f5f223a6c616d62646120732c5f3a5b5f3a3d66285f29666f72206620696e20732e5f5d5b2d315d7d29
class _Compose(_Builder):
    pass


@_Compose
@Clear
@list
@str
class Compose:
    pass


@EvalHex
@lambda _: 0x747970652822222c285f4275696c6465722c292c7b225f5f63616c6c5f5f223a6c616d62646120732c5f3a5f282a732e5f297d29
class _Args(_Builder):
    pass


@_Args
@Clear
@list
@str
class Args:
    pass


@itemgetter
@lambda _: 28
class _28:
    pass


@attrgetter
@_28
@dir
@lambda _: type
class GetName:
    pass


@EvalHex
@lambda _: 0x696e742e5f5f6e65675f5f
class Negate:
    pass


@Negate
@lambda _: 1
class _1:
    pass


@itemgetter
@lambda _: Args @ None @ None @ _1 @ Call @ slice
class Reverse:
    pass


@EvalHex
@lambda _: 0x6c616d6264612a5f3a6c697374285f29
class ListOf:
    pass
