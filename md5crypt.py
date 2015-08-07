from hashlib import md5

pw = "toomanysecrets"
salt = "2Z4e3j5f"
rounds = 1000

magic = "$1$"
pwlen = len(pw)
itoa64 = "./0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

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

# iterate 1000 times to slow down brute force cracking
for i in xrange(rounds):
    tmp = md5(pw if i & 1 else dc)
    if i % 3: tmp.update(salt)
    if i % 7: tmp.update(pw)
    tmp.update(dc if i & 1 else pw)
    dc = tmp.digest()

# mix the final output
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
