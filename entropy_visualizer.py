import Image
from bitstring import BitArray

size = 16 # square
extracted = ''
pic = Image.new('RGB', (size, size)) # default background is black

def von_neumann_extractor(bit_str):
    index = 0
    tmp = ''
    while index < len(bit_str):
        if index+1 < len(bit_str):
            bit_1 = bit_str[index]
            bit_2 = bit_str[index+1]
            if bit_1 <> bit_2:
                tmp += bit_1
        index += 2
    return tmp

while len(extracted) <= 256:
    with open('/dev/urandom', 'rb') as f:
        data = f.read(1)

    raw_bytes = BitArray(bytes=data)
    raw_bits = raw_bytes.bin
    extracted += von_neumann_extractor(raw_bits)

bits = extracted[:256]

for x in xrange(size):
    for y in xrange(size):
            bit = int(bits[((x+1)+(y*8))])
            if bit % 2 == 0:
                pic.putpixel((x, y), (255,255,255)) # white pixel against black

pic.save('random.png')
