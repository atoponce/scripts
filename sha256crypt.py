from hashlib import sha256

# $ mkpasswd --method='sha-256' --salt='sQkvOlC7y2nGmCCr' --rounds=5000 --stdin 'toomanysecrets'
# $5$rounds=5000$sQkvOlC7y2nGmCCr$VCGMywA7NHWyXjDAqWe5GsVxIcBJrfZiYuqYVAunXZ6

pw = "toomanysecrets"
salt = "sQkvOlC7y2nGmCCr"
rounds = 5000

magic = "$5$"
pwlen = len(pw)
itoa64 = "./0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
quot, rem = divmod(rounds, 42)

# Ensure min and max limits for rounds
if rounds < 1000: rounds = 1000
if rounds > 999999999: rounds = 999999999

# Start digest "a"
da = sha256(pw + salt)

# Create digest "b"
db = sha256(pw + salt + pw).digest()

# Update digest "a" by repeating digest "b", providing "pwlen" bytes:
i = pwlen
while i > 0:
    da.update(db if i > 32 else db[:i])
    i -= 32

# Upate digest "a" by adding either a NULL or the first char from "pw"
i = pwlen
while i:
    da.update(db if i & 1 else pw)
    i >>= 1

da = da.digest()

# Create digest "p"
dp = sha256()

# For every character in "pw", add "pw" to digest "p"
for char in pw:
    dp.update(pw)
dp = dp.digest()

# Produce byte sequence "p" of the same length as "pw"
i = pwlen
tmp = ""
while i > 0:
    tmp += dp if i > 32 else dp[:i]
    i -= 32
dp = tmp

# Create digest "s"
ds = sha256(salt * (16 + ord(da[0]))).digest()[:len(salt)]
dc = da

p = dp
pp = dp+dp
ps = dp+ds
psp = dp+ds+dp
sp = ds+dp
spp = ds+dp+dp

permutations = [
    (p , psp), (spp, pp), (spp, psp), (pp, ps ), (spp, pp), (spp, psp),
    (pp, psp), (sp , pp), (spp, psp), (pp, psp), (spp, p ), (spp, psp),
    (pp, psp), (spp, pp), (sp , psp), (pp, psp), (spp, pp), (spp, ps ),
    (pp, psp), (spp, pp), (spp, psp)
]
# Optimize!
while quot:
    for i, j in permutations:
        dc = sha256(j + sha256(dc + i).digest()).digest()
    quot -= 1

if rem:
    half_rem = rem >> 1
    for i, j in permutations[:half_rem]:
        dc = sha256(j + sha256(dc + i).digest()).digest()
    if rem & 1:
        dc = sha256(dc + permutations[half_rem][0]).digest()

# convert 3 8-bit words to 4 6-bit words
final = ""
for x,y,z in ((0,10,20),(21,1,11),(12,22,2),(3,13,23),(24,4,14),
              (15,25,5),(6,16,26),(27,7,17),(18,28,8),(9,19,29)):
    v = ord(dc[x]) << 16 | ord(dc[y]) << 8 | ord(dc[z])
    for i in range(4):
        final += itoa64[v & 0x3f]
        v >>= 6
v = ord(dc[31]) << 8 | ord(dc[30])
for i in range(3):
    final += itoa64[v & 0x3f]
    v >>= 6

# output the result
print "{0}rounds={1}${2}${3}".format(magic, rounds, salt, final)
