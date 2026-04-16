from aseprite import AsepriteFile

ASE_NAME = "icons.ase"
SFD_NAME = "font.sfd"
SAVE_FOLDER = ""

def validate(chars) -> int:
    try: return int(chars)
    except: return -1


print("-- program ready to start --")

with open(ASE_NAME, "rb") as f:
    ase = AsepriteFile(f.read())
    WIDTH, HEIGHT = ase.header.width, ase.header.height

font = fontforge.open(SFD_NAME) # type: ignore
font.selection.select(glyph := (input('Select the character: ')[0]))
font.clear()
c = font.createChar(-1, glyph)
pen = c.glyphPen()

print("-- contents of gliph erased --")

celchunks = [_ for _ in ase.frames[0].chunks if isinstance(_, CelChunk)]
print(
    "Select the index of the layer to import:",
    *[
        f'{i} - {layer.name}'
        for i, layer in enumerate(ase.layers[_.layer_index] for _ in celchunks)
    ],
    sep='\n'
)
while not 0 <= (index := validate(input("- : "))) < len(ase.layers): pass

print("-- value accepted, evaluating changes -- ")

for i, byte in enumerate((data := (chunk := celchunks[index]).data)['data']):
    print('##' if byte else '  ', end='')
    if (i + 1) % data['width'] == 0: print()
    if not byte: continue
    x, y = i % data['width'] + chunk.x_pos, HEIGHT - i // data['height'] - chunk.y_pos - font.descent
    pen.moveTo((x, y))
    pen.lineTo((x+1, y))
    pen.lineTo((x+1, y-1))
    pen.lineTo((x, y-1))
    pen.closePath()

print("-- adjusting character --")

c.removeOverlap()
c.simplify()
c.correctDirection()
# c.autoHint()

print("-- all done! saving changes --")

pen = None
font.save(SFD_NAME)

if input("would you also like to create the fonts? y/[n]: ") == 'y':
    font.generate(f"{SAVE_FOLDER}woff2")
    font.generate(f"{SAVE_FOLDER}woff")
    font.generate(f"{SAVE_FOLDER}ttf")
    font.generate(f"{SAVE_FOLDER}otf")
    
    print("-- fonts generated! --")

font.close()
