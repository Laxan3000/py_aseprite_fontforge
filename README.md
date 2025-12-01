## Fork of [py_aseprite](https://github.com/Eiyeron/py_aseprite), original README there

Simple fork with a script added to easily convert a sprite made in [Aseprite](http://aseprite.org/) to a font icon in [FontForge](https://fontforge.org/).

The script does not change the metadata of the font, but it is recommended to set the `em` size to the same size of the sprite canvas (with ascending set to 0).

To run, tweak the constants inside `makechar.py` and run on your terminal:

```sh
fontforge -script makechar.py
```

From FlatPak:

```sh
flatpak run org.fontforge.FontForge -script makefont.py
```