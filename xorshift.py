class xorshift(object):
    def __init__(self, *args):
        self._seed(*args)

    def _int32(self, n):
        return int(0xFFFFFFFF & n)

    def _int64(self, n):
        return int(0xFFFFFFFFFFFFFFFF & n)

    def _seed(self, *args):
        import time
        if len(args) > 4:
            raise ValueError('Maximum of 4 seeds allowed.')
        self._x = self._int64(args[0] if len(args) > 0 else int(time.time() * 1000000))
        self._y = self._int64(args[1] if len(args) > 1 else int(time.time() * 1000000))
        self._z = self._int64(args[2] if len(args) > 2 else int(time.time() * 1000000))
        self._w = self._int64(args[3] if len(args) > 3 else int(time.time() * 1000000))

    def xorshift32(self):
        x = self._x
        x ^= (x << 13)
        x ^= (x >> 17)
        x ^= (x << 5)
        self._x = self._int64(x)
        return self._int32(x)

    def xorshift128(self):
        t = self._w
        t ^= (t << 11)
        t ^= (t >> 8)
        self._w = self._z
        self._z = self._y
        self._y = self._x
        t ^= self._x
        t ^= (self._x >> 19)
        self._x = self._int64(t)
        return self._int32(t)

    def xorshift64star(self):
        x = self._x
        x ^= (x >> 12)
        x ^= (x << 25)
        x ^= (x >> 27)
        self._x = self._int64(x)
        return self._int64(x * 0x2545F4914F6CDD1D)

    def xorshift128plus(self):
        x = self._x
        y = self._y
        self._x = self._int64(y)
        x ^= (x << 23)
        self._y = self._int64(x ^ y ^ (x >> 17) ^ (y >> 26))
        return self._int64(self._y + y)
