class F:
    def __add__(self):
        pass

    def __getitem__(self):
        pass

    def __setitem__(self):
        pass


def tup(first):
    def inner(*second):
        if not second:
            return tuple(first for _ in range(1))

        return tuple(next(iter(second)) if i else first for i in range(2))

    return inner


def advance(num):
    def inner(iterator):
        for _ in range(num):
            next(iterator)
        return iterator

    return inner


def get_value(name):
    return getattr(*tup(globals())(next(advance(10)(iter(dir(F))))))(name)


def set_value(name):
    def inner(value):
        return getattr(*tup(globals())(next(advance(24)(iter(dir(F))))))(*tup(name)(value))

    return inner


set_value(chr(65))(next(iter(dir(F))))
set_value(chr(71))(next(advance(10)(iter(dir(F)))))
set_value(chr(83))(next(advance(24)(iter(dir(F)))))

set_value(chr(79))(range(1))
set_value(chr(84))(range(2))


def build_map(t):
    def mapper(func):
        def init(initial):
            def end(final):
                def inner(*element):
                    if not element:
                        return getattr(*tup(t)(A))(*tup(initial)(final))

                    return init(getattr(*tup(t)(A))(*tup(initial)(func(next(iter(element))))))(final)

                return inner

            return end

        return init

    return mapper


def identity(x):
    return x


def build(t):
    return build_map(t)(identity)


build_string = build_map(str)(chr)(str())(str())

set_value(chr(68))(build_string(95)(95)())
build_magic = build_map(str)(chr)(D)(D)

set_value(chr(69))(build_magic(101)(113)())
set_value(chr(77))(build_magic(109)(97)(105)(110)())
