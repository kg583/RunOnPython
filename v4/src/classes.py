from util import *


class C:
    def __init__(*args):
        setattr(*build_tuple(f(args))(chr(120))(s(args))())

    def __mul__(*args):
        return getattr(*tup(int)(A))(*tup(getattr(*tup(f(args))(chr(120))))(getattr(*tup(s(args))(chr(120)))))

    def this_is_a_property(self):
        return getattr(*tup(int)(A))(*tup(getattr(*tup(self)(chr(120))))(27))


setattr(*build_tuple(C)(f(reversed(dir(C))))(property(getattr(*tup(C)(f(reversed(dir(C)))))))())


if __name__ in tup(M)():
    set_value(chr(99))(C(42))
    print(getattr(*tup(get_value(chr(99)))(chr(120))))

    set_value(chr(100))(C(69))
    print(get_value(chr(99)) * get_value(chr(100)))

    print(getattr(*tup(get_value(chr(99)))(f(reversed(dir(C))))))
