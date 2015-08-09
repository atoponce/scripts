from hashlib import md5
from random import SystemRandom

pw = "toomanysecrets"

r = SystemRandom()
pwlen = len(pw)
itoa64 = "./0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
salt = "".join(r.choice(itoa64) for i in xrange(8))
quot, rem = divmod(1000, 42) # md5crypt does not support a variable # of rounds

p = pw
pp = pw+pw
ps = pw+salt
psp = pw+salt+pw
sp = salt+pw
spp = salt+pw+pw

permutations = [
    (p , psp), (spp, pp), (spp, psp), (pp, ps ), (spp, pp), (spp, psp),
    (pp, psp), (sp , pp), (spp, psp), (pp, psp), (spp, p ), (spp, psp),
    (pp, psp), (spp, pp), (sp , psp), (pp, psp), (spp, pp), (spp, ps ),
    (pp, psp), (spp, pp), (spp, psp)
]

# Start digest "a"
da = md5(pw + "$1$" + salt)

# Create digest "b"
db = md5(psp).digest()

# Update digest "a" by repeating digest "b", providing "pwlen" bytes:
i = pwlen
while i > 0:
    da.update(db if i > 16 else db[:i])
    i -= 16

# Upate digest "a" by adding either a NULL or the first char from "pw"
i = pwlen
while i:
    da.update(b"\x00" if i & 1 else pw[0])
    i >>= 1
da = da.digest()

# Optimize!
while quot:
    for i, j in permutations:
        da = md5(j + md5(da + i).digest()).digest()
    quot -= 1

for i, j in permutations[:rem/2]:
    da = md5(j + md5(da + i).digest()).digest()

# convert 3 8-bit words to 4 6-bit words while mixing
final = ''
for x, y, z in ((0, 6, 12), (1, 7, 13), (2, 8, 14), (3, 9, 15), (4, 10, 5)):
    v = ord(da[x]) << 16 | ord(da[y]) << 8 | ord(da[z])
    for i in range(4):
        final += itoa64[v & 63]
        v >>= 6
v = ord(da[11])
for i in range(2):
    final += itoa64[v & 63]
    v >>= 6

# output the result
print "$1${0}${1}".format(salt, final)
