import json
with open('style.json') as styles:
    style = json.load(styles)


def customScale():
    sizing = style["defaults"]
    scale = style["scale"]

    sizing["width"] *= scale
    sizing["height"] *= scale
    sizing["particleWidth"] *= scale

    return sizing


def customResolution(sizing):
    resolution = style["resolution"]

    sizing["Dt"] *= resolution

    return sizing


def customFont():
    font = style["textfont"]
    return font


def customFontsize():
    size = style["textsize"]
    return size
