# ---------- Helper Methods ------------- #
def month_string(mon):
    if (mon == 1):
        month = "Jan"
    elif (mon == 2):
        month = "Feb"
    elif (mon == 3):
        month = "Mar"
    elif (mon == 4):
        month = "Apr"
    elif (mon == 5):
        month = "May"
    elif (mon == 6):
        month = "Jun"
    elif (mon == 7):
        month = "Jul"
    elif (mon == 8):
        month = "Aug"
    elif (mon == 9):
        month = "Sep"
    elif (mon == 10):
        month = "Oct"
    elif (mon == 11):
        month = "Nov"
    elif (mon == 12):
        month = "Dec"
    return month

def weekday_string(wday):
    if (wday == 0):
        day = "Monday"
    elif (wday == 1):
        day = "Tuesday"
    elif (wday == 2):
        day = "Wednesday"
    elif (wday == 3):
        day = "Thursday"
    elif (wday == 4):
        day = "Friday"
    elif (wday == 5):
        day = "Saturday"
    elif (wday == 6):
        day = "Sunday"
    return '{:^9}'.format(day)
