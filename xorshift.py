class xorshift(object):
    def __init__(self, *args):
        self.seed(*args)

    def _int32(self, n):
        return int(0xFFFFFFFF & n)

    def _int64(self, n):
        return int(0xFFFFFFFFFFFFFFFF & n)

    def seed(self, *args):
        import time
        if len(args) > 4:
            raise ValueError('Maximum of 4 seeds allowed.')
        self.x = self._int64(args[0] if len(args) > 0 else int(time.time() * 1000000))
        self.y = self._int64(args[1] if len(args) > 1 else int(time.time() * 1000000))
        self.z = self._int64(args[2] if len(args) > 2 else int(time.time() * 1000000))
        self.w = self._int64(args[3] if len(args) > 3 else int(time.time() * 1000000))

    def xorshift32(self):
        t = self.x
        t ^= t << 13
        t ^= t >> 17
        t ^= t << 5
        self.x = self._int64(t)
        return self._int32(t)

    def xorshift128(self):
        t = self.w
        t ^= t << 11
        t ^= t >> 8
        self.w = self.z
        self.z = self.y
        self.y = self.x
        t ^= self.x
        t ^= self.x >> 19
        self.x = self._int64(t)
        return self._int32(t)

    def xorshift64star(self):
        t = self.x
        t ^= t >> 12
        t ^= t << 25
        t ^= t >> 27
        self.x = self._int64(t)
        return self._int64(t * 0x2545F4914F6CDD1D)

    def xorshift128plus(self):
        t = self.x
        u = self.y
        self.x = self._int64(u)
        t ^= t << 23
        self.y = self._int64(t ^ u ^ (t >> 17) ^ (u >> 26))
        return self._int64(self.y + u)
