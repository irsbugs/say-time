# say-time

Speak the approximate time

saytime.py

**saytime** was written in Scheme scripting language and supplied with Festival 
Speech Synthesis System

Re-written in python3 and enhanced to provide day, month, year, day-of-week.
Uses gspeak module for google translate to provide the text-to-speech.
The gspeak module uses subprocess and urllib to interact with google An alternatve is to use GStreamer. Refer to the google_tts_gstreamer.py program.

No output written to the console as it would then be spoken by the screen
reader / espeak.

Ian Stewart - Mar 2019
