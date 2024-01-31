import json
import os
import sys

def resource_path(relative_path):
	if hasattr(sys, '_MEIPASS'):
		return os.path.join(sys._MEIPASS, relative_path)
	return os.path.join(os.path.abspath("."), relative_path)

with open(resource_path('style.json')) as styles:
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
