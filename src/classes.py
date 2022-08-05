from util import *


class C:
    def __init__(*args):
        setattr(*build(tuple)(tup(next(iter(args)))(chr(120)))(tuple(next(advance(1)(iter(args))) for _ in O))())

    def __mul__(*args):
        return getattr(*tup(int)(A))(*tup(getattr(*tup(next(iter(args)))(chr(120))))(getattr(*tup(next(advance(1)(iter(args))))(chr(120)))))


if __name__ in tup(M)():
    set_value(chr(99))(C(42))
    print(getattr(*tup(get_value(chr(99)))(chr(120))))

    set_value(chr(100))(C(69))
    print(get_value(chr(99)) * get_value(chr(100)))
