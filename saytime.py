#!/usr/bin/env python3
#!
# saytime.py
#
# saytime was written in Scheme scripting language and supplied with Festival 
# Speech Synthesis System
# 
# Re-written in python3 and enhanced to provide day, month, year, day-of-week.
# Uses gspeak module for google translate to provide the text-to-speech.
#
# No output written to the console as it would then be spoken by the screen
# reader / espeak.
# 
# Ian Stewart - Mar 2019
# TODO: 
# Include a test for network if not available then output as text to console
#
import sys
import time
from datetime import datetime
try:
    from pylib.gspeak import gspeak
    from pylib.check_internet import is_internet
except:
    pass

# If any arg passed then provide the date and day-of-the-week with the time.
if len(sys.argv) > 1:
    verbose_time = True
else:
    verbose_time = False

# Get the local times' hours and minutes 
hour = time.localtime()[3]
minute = time.localtime()[4]

# Message lists
five_minute_list = ["the hour of", "five past", "ten past", "quarter past", 
            "twenty past", "twenty-five past", "half past", "twenty-five to", 
            "twenty to", "quarter to", "ten to", "five to", "the hour of"]

how_near_list = ["soon to be", "almost", "exactly", "just after", 
            "a little after"]

hour_list = ["twelve", "one", "two", "three", "four", "five", "six", "seven", 
            "eight", "nine", "ten", "eleven", "twelve", "one", "two", "three", 
            "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", 
            "twelve"]

time_of_day = ["at night", "in the morning", "in the afternoon", 
            "in the evening"]

def round_to_5_minute(x, base=5):
    # Round the minutes to 5 minute intervals. E.g. 3 to 7 will rounded to 5.
    return int(base * round(float(x)/base))

def get_five_minute(minute):
    # Create the how-near to the 5 minute message and the 5 min message.
    pointer_5_minute_list = round_to_5_minute(minute)//5
    offset = minute - round_to_5_minute(minute) + 2
    return how_near_list[offset], five_minute_list[pointer_5_minute_list]

def get_hour(hour, minute):
    # Create the message for the hour
    if minute < 33:
        hour_pointer = hour
    else:
        hour_pointer = hour + 1
    return hour_list[hour_pointer]

def get_time_of_day(hour):
    # Create message for the period of time throughout the day.
    if hour in [0,1,2,3,4,5,22,23,24]: time_or_day_pointer = 0 # night
    if hour >5 and hour <= 11: time_or_day_pointer = 1  # morning
    if hour >11 and hour <= 17: time_or_day_pointer = 2  # afternoon
    if hour >17 and hour <= 21: time_or_day_pointer = 3  # evening
    return time_of_day[time_or_day_pointer] 

def get_day_month_year():
    # Build the day month year related message
    # "%d" return "03" while "%-d" return "3". On linux - removes zero padding.    
    day_of_week = datetime.now().strftime("%A")
    month = datetime.now().strftime("%B")
    day_number = datetime.now().strftime("%-d")
    year = datetime.now().strftime("%Y")

    if day_number in ["1", "21", "31"]: day = day_number + "st"
    elif day_number in ["2", "22"]: day = day_number + "nd"
    elif day_number in ["3", "23"]: day = day_number + "rd"
    else: day = day_number + "th"

    # Choice of string to say the day and date.
    # It is Thursday on February the 14th of 2019 and ...
    #return ("It is " + day_of_week + " for " + month + " the " + day + " of " + 
    #        str(year) + " and ") 

    # February the 14th of 2019 is Thursday and ...
    return (month + " the " + day + " of " + str(year) + " is " + day_of_week 
            + " and ") 

def saytime(hour=hour, minute=minute):
    # Get messages data from other routines and build main message.
    day_month_year_message = get_day_month_year()   
    near_message, five_minute_message = get_five_minute(minute)
    hour_message = get_hour(hour, minute)
    time_of_day_message = get_time_of_day(hour)

    # Output the date and the time message. Use internet/google if available
    # Fall back to message to console if no internet.
    if verbose_time:
        if is_internet():
            message = (day_month_year_message + " the time is " + 
                    near_message + " " + five_minute_message + " " + 
                    hour_message + " " + time_of_day_message + ".")
            gspeak(message)
        else:

            # Output the date and time message to the console        
            print(day_month_year_message + "the time is " + 
                    near_message + " " + five_minute_message + " " + 
                    hour_message + " " + time_of_day_message + ".")

    else:
        if is_internet():
        # Send to gspeak
            message = ("The time is " + near_message + " " + 
                    five_minute_message + " " + hour_message + " " + 
                    time_of_day_message + ".")
            gspeak(message)

        else:
            # Output the time (only) message to the console
            print("The time is " + near_message + " " + 
                    five_minute_message + " " + hour_message + " " + 
                    time_of_day_message + ".")       

def test_program():
    # Output for every minute in the day. 
    # TODO: Turn gspeak off send to console
    for hour in range(24):
        for minute in range(60):
            main_program(hour, minute)

if __name__ == "__main__":

    from gspeak import gspeak
    from check_internet import is_internet
    # Call main program.
    saytime(hour, minute)

    # Remove comment below to test one day of time output for every minute.
    #test_program()
    sys.exit()

