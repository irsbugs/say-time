#!/usr/bin/env python3
#!
# saytime_espeak.py
#
# saytime was written in Scheme scripting language and supplied with Festival 
# Speech Synthesis System
# 
# Re-written in python3 and enhanced to provide day, month, year, day-of-week.
#
# If it writes to console and has espeak on, then double voices.
# If espeak available use an no console output otherwise colsole output 
# Edit program to change espeak voice characteristics.
#
# Ian Stewart - Mar 2019
#
# 
import time
from datetime import datetime
import sys

espeak_available = False
verbose_time = False

# Change the sound of the espeak voice parameters
#         Rate Volume Pitch Range Punctuation Capitals Wordgap
# default[175, 100,   50,   50,   0,          0,       0]
new_parameter = [220, 100, 80, 80, 0, 0, 0]

# Change the type of English voice
voice = ['en', 'other/en-sc', 'other/en-n', 'other/en-rp', 'other/en-wm', 
         'en-us', 'other/en-wi']
voice_value = 5

# If any arg passed then provide the date and day-of-the-week with the time.
if len(sys.argv) > 1:
    verbose_time = True

try: 
    from espeak import espeak
    espeak_available = True
except:
    espeak_available = False   

# If a screen reader, like Orca, provides text to speech then turn off espeak.
#espeak_available = False

hour = time.localtime()[3]
minute = time.localtime()[4]

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
    # "%d" return 03 while "%-d" return 3. On linux - removes zero padding.    
    day_of_week = datetime.now().strftime("%A")
    month = datetime.now().strftime("%B")
    day_number = datetime.now().strftime("%-d")
    year = datetime.now().strftime("%Y")

    if day_number in ["1", "21", "31"]: day = day_number + "st"
    elif day_number in ["2", "22"]: day = day_number + "nd"
    elif day_number in ["3", "23"]: day = day_number + "rd"
    else: day = day_number + "th"

    # It is Thursday on February the 14th of 2019 and ...
    #return ("It is " + day_of_week + " for " + month + " the " + day + " of " + 
    #        str(year) + " and ") 

    # February the 14th of 2019 is Thursday and ...
    return (month + " the " + day + " of " + str(year) + " is " + day_of_week 
            + " and ") 

def time_espeak(hour=hour, minute=minute):
    # Get messages data from other routines and build main message.
    if espeak_available:
        # Set voice to parameters in list at beginning of program
        change_espeak_voice()

    day_month_year_message = get_day_month_year()   
    near_message, five_minute_message = get_five_minute(minute)
    hour_message = get_hour(hour, minute)
    time_of_day_message = get_time_of_day(hour)

    # Output the date and the time message
    if verbose_time:
        # If python3 espeak is available then speak the message
        if espeak_available:
            espeak.synth(day_month_year_message + " the time is " + 
                near_message + " " + five_minute_message + " " + 
                hour_message + " " + time_of_day_message + ".")
            # Wait for espeak to speak the message
            while espeak.is_playing():
                time.sleep(0.2)
        else:
            print(day_month_year_message + "the time is " + 
                near_message + " " + five_minute_message + " " + 
                hour_message + " " + time_of_day_message + ".")

    else:
        # If python3 espeak is available then speak the message
        if espeak_available:
            espeak.synth("The time is " + near_message + " " + 
                        five_minute_message + " " + hour_message + " " + 
                        time_of_day_message + ".")
            # Wait for espeak to speak the message
            while espeak.is_playing():
                time.sleep(0.2)

        # Output the time (only) message to the console
        else:
            print("The time is " + near_message + " " + 
                        five_minute_message + " " + hour_message + " " + 
                        time_of_day_message + ".")

def change_espeak_voice():
    # Change the sound of the voice
    default_parameter_name = [
    "Rate", "Volume", "Pitch", "Range", "Punctuation", "Capitals", "Wordgap"]
    default_parameter = []

    for i in range(1,8):
       default_parameter.append(espeak.get_parameter(i, 1))

    for i in range(len(default_parameter)):
        pass
        #print(default_parameter_name[i], default_parameter[i])

    for i in range(len(default_parameter_name)):
        espeak.set_parameter(i + 1, new_parameter[i])    

    for i in range(1,8):
        pass
        #print(espeak.get_parameter(i, 1))
        
    espeak.set_voice(voice[voice_value])

    #espeak.synth("hello World")        
    #while espeak.is_playing():
    #    time.sleep(0.2)        

def test_program():
    # Output for every minute in the day. Turn espeak off
    global espeak_available
    espeak_available = False
    for hour in range(24):
        for minute in range(60):
            main_program(hour, minute)

if __name__ == "__main__":
    # Call main program.
    time_espeak(hour, minute)

    # Remove comment below to test one day of time output for every minute.
    #test_program()
    sys.exit()

"""
This can be called as a module with 

from pylib.saytime_espeak import 
#print(dir(pylib.saytime))

#['__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__spec__', 'change_espeak_voice', 'datetime', 'espeak', 'espeak_available', 'five_minute_list', 'get_day_month_year', 'get_five_minute', 'get_hour', 'get_time_of_day', 'hour', 'hour_list', 'how_near_list', 'main_program', 'minute', 'new_parameter', 'round_to_5_minute', 'sys', 'test_program', 'time', 'time_of_day', 'verbose_time', 'voice', 'voice_value']
import time
hour = time.localtime()[3]
minute = time.localtime()[4]

pylib.saytime.main_program(hour, minute) 

saytime only the time
and
saytime -x  Verbose has day and month

"""
