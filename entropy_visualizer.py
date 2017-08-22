import Image
import ImageTk
import Tkinter

from bitstring import BitArray
    
tk = Tkinter.Tk()
tk.title = "Entropy"
tk.resizable(0,0)
tk.wm_attributes("-topmost", 1)

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

def draw_image():
    size = 16 # square
    extracted = ''

    img = Image.new('RGB', (size, size)) # default background is black

    while len(extracted) <= 256:
        with open('/dev/urandom', 'rb') as f:
            data = f.read(64)

        raw_bytes = BitArray(bytes=data)
        raw_bits = raw_bytes.bin
        extracted += von_neumann_extractor(raw_bits)

    bits = extracted[:256]

    for x in xrange(size):
        for y in xrange(size):
            bit = int(bits[((x+1)+(y*8))])
            if bit % 2 == 0:
                img.putpixel((x, y), (255,255,255)) # white pixel against black

    img = img.resize((512, 512), Image.NEAREST)
    tkimg = ImageTk.PhotoImage(img)
    # need to git image from --^ to --v somehow
    tk.after(500, draw_image)

draw_image()
tk.mainloop()
