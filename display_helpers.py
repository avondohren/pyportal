import displayio
from adafruit_display_text.label import Label
from adafruit_pyportal import PyPortal
from fonts_and_styles import *

def set_image(group, filename):
    print("Set image to ", filename)
    if group:
        group.pop()

    if not filename:
        return  # we're done, no icon desired
    try:
        if image_file:
            image_file.close
    except NameError:
        pass
    image_file = open(filename, "rb")
    image = displayio.OnDiskBitmap(image_file)
    try:
        image_sprite = displayio.TileGrid(image, pixel_shader=displayio.ColorConverter())
    except TypeError:
        image_sprite = displayio.TileGrid(image, pixel_shader=displayio.ColorConverter(), position=(0,0))
    group.append(image_sprite)

def hideLayer(splash, target):
    try:
        splash.remove(target)
    except ValueError:
        pass

def showLayer(splash, target):
    try:
        splash.append(target)
    except ValueError:
        pass

# Word Wrap Helper
text_hight = Label(font, text="M", color=WHITE, max_glyphs=10)

def text_box(target, top, max_chars, string):
    text = pyportal.wrap_nicely(string, max_chars)
    new_text = ""
    test = ""
    for w in text:
        new_text += '\n'+w
        test += 'M\n'
    text_hight.text = test
    glyph_box = text_hight.bounding_box
    print(glyph_box[3])
    target.text = "" # Odd things happen without this
    target.y = round(glyph_box[3]/2)+top
    target.text = new_text