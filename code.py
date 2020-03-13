import time
import board
import random
from adafruit_pyportal import PyPortal
from secrets import secrets
# from alpha_vantage.timeseries import TimeSeries

# Set up where we'll be fetching data from
# DATA_SOURCE = "https://www.adafruit.com/api/quotes.php"
ALPHA_KEY = secrets['alphavantage_key']
symbol = "msft"
DATA_SOURCE = "https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol="+symbol+"&apikey="+ALPHA_KEY

SYMBOL = ['Global Quote', '01. symbol']
OPEN = ['Global Quote', '02. open']
HIGH = ['Global Quote', '03. high']
LOW = ['Global Quote', '04. low']
PRICE = ['Global Quote', '05. price']
VOLUME = ['Global Quote', '06. volume']
DATE = ['Global Quote', '07. latest trading day']
PREV_CLOSE = ['Global Quote', '08. previous close']
CHANGE = ['Global Quote', '09. change']
CHANGE_PCT = ['Global Quote', '10. change percent']

def format_result(dict):
    price = float(dict['Global Quote']['05. price'])
    change = float(dict['Global Quote']['09. change'])
    pct = float(dict['Global Quote']['10. change percent'].strip("%"))
    dict['Global Quote']['05. price'] = "${:,.2f}".format(price)
    dict['Global Quote']['09. change'] = "{:,.2f}".format(change)
    dict['Global Quote']['10. change percent'] = "{:,.2f}%".format(pct)

# the current working directory (where this file is)
cwd = ("/"+__file__).rsplit('/', 1)[0]
pyportal = PyPortal(url=DATA_SOURCE,
                    json_path=(PRICE, CHANGE, CHANGE_PCT, SYMBOL),
                    status_neopixel=board.NEOPIXEL,
                    default_bg=cwd+"/main_background_day.bmp",
                    text_font=cwd+"/fonts/Helvetica-Bold-36.bdf",
                    text_position=((90, 100), (90, 140), (190, 140), (90, 60)),
                    text_color=(0xFFFFFF, 0xFFFFFF, 0xFFFFFF, 0x8080FF),
                    text_wrap=(35, 0, 0, 0),
                    text_maxlen=(180, 30, 30, 30),
                    json_transform=(format_result),
                    )

# speed up projects with lots of text by preloading the font!
pyportal.preload_font()
pyportal.set_backlight(.4)

while True:
    try:
        symbol = random.choice(["amd", "msft", "oi", "gps", "alk", "adbe"])
        url = "https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol="+symbol+"&apikey="+ALPHA_KEY
        print("URL is", url)
        value = pyportal.fetch(refresh_url=url)
        print("Response is", value)
    except RuntimeError as e:
        print("Some error occured, retrying! -", e)
    time.sleep(30)