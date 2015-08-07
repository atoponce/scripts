from hashlib import sha512

# $ mkpasswd --method='sha-512' --salt='q4QD/vCH2sSrLdeb' --rounds=5000 --stdin 'toomanysecrets'
# $6$rounds=5000$q4QD/vCH2sSrLdeb$8KMwaDhI2jQD/sOGvjxgFB4XWuhTYwjXovFYDku20CFz4ZvCE7030dvTzdxo9P0ce8UjNbKBZ/MhIG8m8A2xm1

pw = "toomanysecrets"
salt = "q4QD/vCH2sSrLdeb"
rounds = 5000

magic = "$6$"
pwlen = len(pw)
itoa64 = "./0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

# Start digest "a"
da = sha512(pw + salt)

# Create digest "b"
db = sha512(pw + salt + pw).digest()

# Update digest "a" by repeating digest "b", providing "pwlen" bytes:
i = pwlen
while i > 0:
    da.update(db if i > 64 else db[:i])
    i -= 64

# Upate digest "a" by adding either a NULL or the first char from "pw"
i = pwlen
while i:
    da.update(db if i & 1 else pw)
    i >>= 1

da = da.digest()

# Create digest "p"
dp = sha512()

# For every character in "pw", add "pw" to digest "p"
for char in pw:
    dp.update(pw)
dp = dp.digest()

# Produce byte sequence "p" of the same length as "pw"
i = pwlen
tmp = ""
while i > 0:
    tmp += dp if i > 64 else dp[:i]
    i -= 64
dp = tmp

# Create digest "s"
ds = sha512(salt * (16 + ord(da[0]))).digest()[:len(salt)]

dc = da

# iterate "rounds" times to slow down brute force cracking
for i in xrange(rounds):
    tmp = sha512(dp if i & 1 else dc)
    if i % 3: tmp.update(ds)
    if i % 7: tmp.update(dp)
    tmp.update(dc if i & 1 else dp)
    dc = tmp.digest()

# mix the final output
final = ""
for x,y,z in ((0,21,42),(22,43,1),(44,2,23),(3,24,45),(25,46,4),(47,5,26),
              (6,27,48),(28,49,7),(50,8,29),(9,30,51),(31,52,10),(53,11,32),
              (12,33,54),(34,55,13),(56,14,35),(15,36,57),(37,58,16),
              (59,17,38),(18,39,60),(40,61,19),(62,20,41)):
    v = ord(dc[x]) << 16 | ord(dc[y]) << 8 | ord(dc[z])
    for i in range(4):
        final += itoa64[v & 0x3f]
        v >>= 6
v = ord(dc[63])
for i in range(2):
    final += itoa64[v & 0x3f]
    v >>= 6

# output the result
print "{0}rounds={1}${2}${3}".format(magic, rounds, salt, final)
