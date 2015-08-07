from hashlib import md5

# $ mkpasswd --method='md5' --salt='2Z4e3j5f' --rounds=1000 --stdin 'toomanysecrets'
# $1$2Z4e3j5f$sKZptx/P5xzhQZ821BRFX1

pw = "toomanysecrets"
salt = "2Z4e3j5f"
rounds = 1000000

magic = "$1$"
pwlen = len(pw)
itoa64 = "./0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
quot, rem = divmod(rounds, 42)

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
da = md5(pw + magic + salt)

# Create digest "b"
db = md5(pw + salt + pw).digest()

# Update digest "a" by repeating digest "b", providing "pwlen" bytes:
i = pwlen
while i > 0:
    da.update(db if i > 16 else db[:i])
    i -= 16

# Upate digest "a" by adding either a NULL or the first char from "pw"
i = pwlen
while i:
    da.update(chr(0) if i & 1 else pw[0])
    i >>= 1
dc = da.digest()

# Optimize!
while quot:
    for i, j in permutations:
        dc = md5(j + md5(dc + i).digest()).digest()
    quot -= 1

for i, j in permutations[:rem/2]:
    dc = md5(j + md5(dc + i).digest()).digest()

# convert 3 8-bit words to 4 6-bit words
final = ''
for x, y, z in ((0, 6, 12), (1, 7, 13), (2, 8, 14), (3, 9, 15), (4, 10, 5)):
    v = ord(dc[x]) << 16 | ord(dc[y]) << 8 | ord(dc[z])
    for i in range(4):
        final += itoa64[v & 0x3f]
        v >>= 6
v = ord(dc[11])
for i in range(2):
    final += itoa64[v & 0x3f]
    v >>= 6

# output the result
print "{0}rounds={1}${2}${3}".format(magic, rounds, salt, final)
