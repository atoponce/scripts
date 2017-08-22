import Image
import ImageTk
import Tkinter

from bitstring import BitArray
    
tk = Tkinter.Tk()
tk.title = "Entropy"
tk.resizable(0,0)
tk.wm_attributes("-topmost", 1)

def von_neumann_extractor(bit_str):
    extracted = ''
    bits = iter(bit_str)
    try:
        while True:
            x, y = bits.next(), bits.next()
            if x <> y:
                extracted += str(x)
    except StopIteration:
        pass

    return extracted

def draw_image():
    size = 16 # square
    extracted = ''

    img = Image.new('RGB', (size, size)) # default background is black

    while len(extracted) <= 256:
        with open('/dev/urandom', 'rb') as f:
            data = f.read(128) # read 4x data as necessary before extraction

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
    label = Tkinter.Label(tk)
    label.pack()
    # need to git image from --^ to --v somehow
    tk.after(500, draw_image)

draw_image()
tk.mainloop()
