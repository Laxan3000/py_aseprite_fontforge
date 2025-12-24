from aseprite import AsepriteFile

SQUARE_SIZE = 16
ASE_NAME = "project.ase"
SFD_NAME = 'font.sfd'
FONT_SAVE_NAME = f"font."

def validate(chars) -> int:
    try: return int(chars)
    except: return -1


print("-- program ready to start --")

with open("icons.ase", "rb") as f:
    ase = AsepriteFile(f.read())

font = fontforge.open(SFD_NAME) # type: ignore
font.selection.select(glyph := (input('Select the character: ')[0]))
font.clear()
c= font.createChar(-1, glyph)
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

for i, byte in enumerate((chunk := celchunks[index]).data['data']):
    print('##' if byte else '  ', end='')
    if (i + 1) % SQUARE_SIZE == 0: print()
    if not byte: continue
    x, y = i % SQUARE_SIZE + chunk.x_pos, SQUARE_SIZE - i // SQUARE_SIZE - chunk.y_pos - font.descent
    pen.moveTo((x, y))
    pen.lineTo((x+1, y))
    pen.lineTo((x+1, y-1))
    pen.lineTo((x, y-1))
    pen.closePath()

print("-- adjusting character --")

c.removeOverlap()
c.simplify()
c.correctDirection()
c.autoHint()

print("-- all done! saving changes --")

pen = None
font.save(SFD_NAME)

if input("would you also like to create the fonts? y/[n]:") == 'y':
    font.generate(f"{SAVE_FOLDER}woff2")
    font.generate(f"{SAVE_FOLDER}woff")
    font.generate(f"{SAVE_FOLDER}ttf")
    font.generate(f"{SAVE_FOLDER}otf")
    
    print("-- fonts generated! --")

font.close()
