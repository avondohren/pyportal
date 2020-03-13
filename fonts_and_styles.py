import board
from adafruit_bitmap_font import bitmap_font

display = board.DISPLAY

# --------- Load Fonts --------- #
font_36 = bitmap_font.load_font("/fonts/Helvetica-Bold-36.bdf")
font_36.load_glyphs(b'abcdefghjiklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890- ():')
font_16 = bitmap_font.load_font("/fonts/Helvetica-Bold-16.bdf")
font_16.load_glyphs(b'abcdefghjiklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890- ():')
font = font_16

# ---------- Text Boxes ------------- #
# Default Label styling:
LABEL_X = 90
LABEL_Y = 50

# Colors
WHITE = 0xffffff
RED = 0xff0000
GREEN = 0x03AD31
MED_BLUE = 0x31699c
DARK_BLUE = 0x10416b

# Default button styling:
BUTTON_HEIGHT = 30
BUTTON_WIDTH = int(display.width/4)

# We want three buttons across the top of the screen
NAV_HEIGHT = 30
NAV_WIDTH = int(display.width/4)
NAV_Y = 2