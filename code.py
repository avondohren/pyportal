# Libraries
import gc
print("Very start -- "+str(gc.mem_free()))
import time
import board
import displayio
import json
import random
import rtc
import re
from analogio import AnalogIn
import adafruit_requests as requests
from adafruit_bitmap_font import bitmap_font
from adafruit_display_text.label import Label
from adafruit_button import Button
from adafruit_pyportal import PyPortal
import adafruit_touchscreen
print("before file imports -- "+str(gc.mem_free()))
# File Imports
from secrets import secrets
from fonts_and_styles import *
from display_helpers import *
from date_helpers import *
print("After Imports -- "+str(gc.mem_free()))

# ------------- Inputs and Outputs Setup ------------- #
# init. the light sensor
light_sensor = AnalogIn(board.LIGHT)

# -------------- Screen Setup -------------- #
display = board.DISPLAY
pyportal = PyPortal(status_neopixel=board.NEOPIXEL)
pyportal.set_backlight(0.3)
pyportal.set_background('pyportal_startup.bmp')

# ----------- Touchscreen setup ----------- #
# Rotate 0:
ts = adafruit_touchscreen.Touchscreen(board.TOUCH_XL, board.TOUCH_XR,
    board.TOUCH_YD, board.TOUCH_YU, calibration=((5200, 59000), (5800, 57000)),
    size=(display.width, display.height))

# ------------- Display Groups ------------- #
splash = displayio.Group(max_size=15)  # The Main Display Group
bg_group = displayio.Group(max_size=5) # The Background Group
splash.append(bg_group)
space_view = displayio.Group(max_size=15)
weather_view = displayio.Group(max_size=15)
stock_view = displayio.Group(max_size=15)
sensor_view = displayio.Group(max_size=15)

pyportal.set_background(None)
set_image(bg_group,"/main_background_day.bmp")

# Text Label Objects
time_data = Label(font, text="Time", color=WHITE, max_glyphs=100, x=10, y=85)
date_data = Label(font, text="Date", color=WHITE, max_glyphs=100, x=10, y=185)
day_data = Label(font, text="Workday", color=0x000000, max_glyphs=100, x=2, y=137) #BLACK
bg_group.append(date_data)
bg_group.append(time_data)
bg_group.append(day_data)

space_data = Label(font, text="Loading...", color=GREEN, max_glyphs=100, x=LABEL_X+5, y=90)
space_view.append(space_data)

weather_data = Label(font, text="Loading...", color=GREEN, max_glyphs=100, x=LABEL_X+5, y=90)
weather_view.append(weather_data)

stocks_label = Label(font_36, color=0x8080FF, max_glyphs=200, x=LABEL_X, y=LABEL_Y) # LIGHT_BLUE
stocks_data = Label(font, text="Loading...", color=GREEN, max_glyphs=100, x=LABEL_X+15, y=100)
stock_view.append(stocks_label)
stock_view.append(stocks_data)

sensors_label = Label(font, text="Sensors", color=GREEN, max_glyphs=200, x=LABEL_X, y=LABEL_Y)
sensor_data = Label(font, text="Data", color=GREEN, max_glyphs=100, x=LABEL_X+15, y=100)
sensor_view.append(sensors_label)
sensor_view.append(sensor_data)

# ---------- Buttons ------------- #
# Main User Interface Buttons
space_button = Button(x=int(0 * NAV_WIDTH), y=NAV_Y, height=50, width=NAV_WIDTH - 5,
                     label="", label_font=font, label_color=None, fill_color=None, outline_color=None)
weather_button = Button(x=int(1 * NAV_WIDTH - 5), y=NAV_Y, height=NAV_HEIGHT, width=NAV_WIDTH + 2,
                     label="Weather", label_font=font,
                     label_color=WHITE, fill_color=DARK_BLUE, outline_color=0x000000, # BLACK
                     selected_fill=MED_BLUE, selected_outline=DARK_BLUE, selected_label=WHITE)
stocks_button = Button(x=int(2 * NAV_WIDTH - 3), y=NAV_Y, height=NAV_HEIGHT, width=NAV_WIDTH + 1,
                     label="Stocks", label_font=font,
                     label_color=WHITE, fill_color=DARK_BLUE, outline_color=0x000000, # BLACK
                     selected_fill=MED_BLUE, selected_outline=DARK_BLUE, selected_label=WHITE)
sensors_button = Button(x=int(3 * NAV_WIDTH - 2), y=NAV_Y, height=NAV_HEIGHT, width=NAV_WIDTH +2,
                     label="Sensors", label_font=font,
                     label_color=WHITE, fill_color=DARK_BLUE, outline_color=0x000000, #BLACK
                     selected_fill=MED_BLUE, selected_outline=DARK_BLUE, selected_label=WHITE)
# This group will make it easy for us to read a button press later.
buttons = [space_button, weather_button, stocks_button, sensors_button]
for b in buttons:
    splash.append(b.group)

# ---------- Load Real Time Clock ------------- #
while (rtc.RTC().datetime.tm_year == 2000):
    try:
        pyportal.get_local_time(secrets['timezone'])
    except RuntimeError as exception:
            print("An error occured", exception)

# ---------- Switch View Helper ------------- #
def switch_view(what_view):
    # Hide all views and disable all buttons
    hideLayer(splash, space_view)
    hideLayer(splash, weather_view)
    hideLayer(splash, stock_view)
    hideLayer(splash, sensor_view)
    space_button.selected = False
    weather_button.selected = False
    stocks_button.selected = False
    sensors_button.selected = False
    global view_live

    if what_view == 2:
        weather_button.selected = True
        showLayer(splash, weather_view)
        view_live = 2
        print("Weather View On")
    elif what_view == 3:
        stocks_button.selected = True
        showLayer(splash, stock_view)
        view_live = 3
        print("Stock View On")
    elif what_view == 4:
        sensors_button.selected = True
        showLayer(splash, sensor_view)
        view_live = 4
        print("Sensor View On")
    else:
        space_button.selected = True
        showLayer(splash, space_view)
        view_live = 1
        print("Space View On")

# ---------- Setup Default View ------------- #
switch_view(2) #show space_view
display.show(splash)
check_weather = 0
check_stocks = 0
check_space = 0
print("Before loop - "+str(gc.mem_free()))

# ------------- Code Loop ------------- #
while True:
    touch = ts.touch_point
    my_time = time.time()
    ctime = time.localtime(my_time)

    hour = ctime.tm_hour
    period = "AM"
    if hour > 12:
        hour = hour - 12
        period = "PM"
    if hour == 0:  # Turn 0 hour into 12 for display
        hour = 12

    time_data.text = '{:^8}\n{:^8}'.format('{:d}:{:02d}'.format(hour, ctime.tm_min), period)
    day_data.text = weekday_string(ctime.tm_wday)
    mo_day = '{} {}'.format(month_string(ctime.tm_mon), ctime.tm_mday)
    date_data.text = '{:^8}\n{:^8}'.format(mo_day, ctime.tm_year)
    del hour
    del period
    del ctime
    gc.collect()
    # print("after date update: "+str(gc.mem_free()))

    # ------------- Handle Button Press Detection  ------------- #
    if touch:  # Only do this if the screen is touched
        # loop with buttons using enumerate() to number each button group as i
        for i, b in enumerate(buttons):
            if b.contains(touch):  # Test each button to see if it was pressed
                print('button%d pressed' % i)
                if view_live != i+1:
                    switch_view(i+1)
                    while ts.touch_point:
                        pass
    gc.collect()

    # Space View
    if (view_live == 1 and (my_time > check_space)):
        gc.collect
        check_space = my_time + 3600 #  1 hour
        people = []
        launches = []
        gc.collect
        try:
            json_data = json.loads(pyportal.fetch(refresh_url="http://api.open-notify.org/astros.json"))
            for path in (['number'], ['people']):
                people.append(PyPortal._json_traverse(json_data, path))
            del json_data
            gc.collect()
            space_data.text = "There are "+str(people[0])+" in space."
            for person in people[1]:
                space_data.text = space_data.text + "\n  "+person["name"]+"("+person["craft"]+")"
            del people
            gc.collect()

            json_data = json.loads(pyportal.fetch(refresh_url="https://fdo.rocketlaunch.live/json/launches/next/2"))
            for path in (['result']):
                launches.append(PyPortal._json_traverse(json_data, path))
            del json_data
            gc.collect()
            space_data.text = space_data.text+"\n"
            for launch in launches[0]:
                space_data.text = space_data.text+"\n"+launch["launch_description"]
            del launches
            gc.collect()
        except RuntimeError as exception:
            print("An error occured", exception)
            if 'json_data' in locals():
                del json_data
            if 'people' in locals():
                del people
            if 'launches' in locals():
                del launches
            del exception
            gc.collect()
            check_space = my_time + 5
            continue


    # Update weather if view_live is 2
    if (view_live == 2 and (my_time > check_weather)):
        gc.collect()
        check_weather = my_time + 300 #  5 min
        url = "https://api.weather.gov/stations/KOMA/observations/latest"
        json_path = (['properties', 'temperature', 'value'],
                     ['properties', 'windSpeed', 'value'],
                     ['properties', 'textDescription'])
        weather_values = []
        gc.collect()
        try:
            gc.collect()
            json_data = json.loads(pyportal.fetch(refresh_url=url))
            for path in json_path:
                weather_values.append(PyPortal._json_traverse(json_data, path))
            del json_data
            del json_path
            gc.collect()

            # Update display
            weather_values[0] = ((weather_values[0] or 0.0) * 1.8) + 32
            weather_values[1] = (weather_values[1] or 0.0)
            weather_values[2] = '\n'.join(PyPortal.wrap_nicely(weather_values[2], 12))
            weather_data.text = 'Temperature: {}°F\nWind Speed: {:.1f} mph\nConditions: {}'.format(weather_values[0],
                                weather_values[1], weather_values[2])
            del weather_values
            gc.collect()
        except RuntimeError as exception:
            print("An error occured", exception)
            if 'json_data' in locals():
                del json_data
            if 'json_path' in locals():
                del json_path
            if 'weather_values' in locals():
                del weather_values
            if 'url' in locals():
                del url
            del exception
            gc.collect()
            check_weather = my_time + 10
            continue

    # Update stock info if view_live is 3
    if (view_live == 3 and (my_time > check_stocks)):
        check_stocks = my_time + 30 #  update stocks every 30s
        symbol = random.choice(["amd", "msft", "oi", "gps", "alk", "adbe", "cvs"])
        print("New symbol is: ", symbol)
        url = "https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol="+symbol+"&apikey="+secrets['alphavantage_key']
        json_path = (['Global Quote', '01. symbol'],
                     ['Global Quote', '05. price'],
                     ['Global Quote', '09. change'],
                     ['Global Quote', '10. change percent'])
        stock_values = []
        gc.collect()
        try:
            json_data = json.loads(pyportal.fetch(refresh_url=url))
            del url
            gc.collect()
            for path in json_path:
                stock_values.append(PyPortal._json_traverse(json_data, path))
            del json_data
            del json_path
            gc.collect()

            # Update display
            stocks_label.text = stock_values[0]
            stocks_data.text = 'Price: {}\nChange: {} ({})'.format("${:,.2f}".format(float(stock_values[1])), "{:,.2f}".format(float(stock_values[2])), "{:,.2f}%".format(float(stock_values[3].strip("%"))))
            if float(stock_values[2]) < 0:
                stocks_data.color = RED
            else:
                stocks_data.color = GREEN
        except RuntimeError as exception:
            print("An error occured", exception)
            if 'json_data' in locals():
                del json_data
            if 'json_data' in locals():
                del json_path
            if 'stock_values' in locals():
                del stock_values
            if 'symbol' in locals():
                del symbol
            del exception
            gc.collect()
            check_stocks = my_time + 10
            continue

    # Sensor View
    if (view_live == 4):
        sensor_data.text = 'Touch: {}\nLight: {}'.format(touch, light_sensor.value)