#!/usr/bin/env python3
#
# google_tts_gstreamer.py
#
# This uses the GStreamer (Gst) module playbin
#
# This uses a loop and needs call_back() function(s) for EOS, etc.
#
# Demonstration of using google translate text to speech feature.
# Will also play a local mp3 file. E.g. yakety_yak.mp3
#
# Ian Stewart - 2020-03-25
# Importing...
import gi
gi.require_version('Gst', '1.0')
gi.require_version('GLib', '2.0')
from gi.repository import Gst, GLib
import sys


# Brief uri as default when calling main().
URI =  'https://translate.google.com/translate_tts?'
URI += 'ie=UTF-8&client=tw-ob&tl={}&q={}'
#URI_COMPOSED = URI.format("en-au", "Hello. I speak with an Australian accent.")
#URI_COMPOSED = URI.format("en-UK", "This should be with a British accent.")
URI_COMPOSED = URI.format("en-US", "This should be with an American accent.")

def main(uri=URI_COMPOSED):
    """
    Requires the uri to be passed.   
    Initialize: Gst, Instantiate playbin, and get rid of video. loop and bus.
    Set the uri property. 
    Start playing the text to google and receiving the mp3 audio stream.
    Run loop and accept bus_call() interupts, checking for EOS.
    End by changing state to null.
    """
    # Init  - call initialize function.
    player, loop = initialize()

    # Set the uri to be sent to google
    player.set_property('uri', uri)

    # Send text to google, and start streaming the mp3 audio with playbin
    player.set_state(Gst.State.PLAYING)

    # Loop while waiting for audio to finish. 
    loop.run()

    # On exiting loop() set playbin state to Null.
    player.set_state(Gst.State.NULL)


def initialize():
    """
    Initialize, Gst, player, loop and bus.
    Create a fakesink to bury any video.
    Bus is set up to perfom a call back to def bus_call(bus, message, loop)
    every time a playbin message is generated.
    """
    # Init
    #GObject.threads_init()
    Gst.init(None)

    # Instantiate    
    #player = Gst.ElementFactory.make("playbin", 'player')

    player = Gst.ElementFactory.make("playbin") #, 'player')

    if not player:
        sys.stderr.write("'playbin' gstreamer plugin missing\n")
        sys.exit(1)

    # Stop video. Only sending audio to playbin
    fakesink = Gst.ElementFactory.make("fakesink", "fakesink")
    player.set_property("video-sink", fakesink)

    # Instantiate the event loop.
    #loop = GObject.MainLoop() <-- deprecated, use GLib
    loop = GLib.MainLoop()

    # Instantiate and initialize the bus call-back 
    bus = player.get_bus()
    bus.add_signal_watch()
    bus.connect ("message", bus_call, loop)

    return player, loop


def bus_call(bus, message, loop):
    """
    Call back for messages generated when playbin is playing.
    The End-of-Stream, EOS, message indicates the audio is complete and the
    waiting loop is quit.
    Note: could havre multiple call_back()'s. One for EOS, one for ERROR, etc.
    """
    t = message.type
    #print(t)

    if t == Gst.MessageType.EOS:
        # End-of-Stream therefore quit loop which executes playbin state Null
        #sys.stdout.write("End-of-stream\n")
        #print(t) # <flags GST_MESSAGE_EOS of type Gst.MessageType>
        loop.quit()

    elif t == Gst.MessageType.ERROR:
        err, debug = message.parse_error()
        # TODO: If error then re-try last message
        sys.stderr.write("Error: %s: %s\n" % (err, debug))
        loop.quit()

    return True


if __name__=="__main__":

    #main()
    
    main(URI.format("en-au", "G'day. I speak with an Australian accent."))
    main(URI.format("en-UK", "Good morning. I speak with a British accent."))
    main(URI.format("en-US", "Howdie. I speak with an American accent."))   

    sys.exit()
    
    # The full uri as created by gTTS
    uri_google = 'https://translate.google.com/translate_tts?ie=UTF-8&q=Hello+this+is+being+spoken+by+an+Aussie+and+listened+to+by+a+Kiwi&tl=en-au&ttsspeed=1&total=1&idx=0&client=tw-ob&textlen=66&tk=887071.737023'
    main(uri_google)
    
    sys.exit()    

    #mp3_file = "file:///home/ian/google_talk/yakety_yak.mp3"
    #main(mp3_file)

    # Alternative if an mp3 file is in the current working directory
    mp3_file = "yakety_yak.mp3"
    uri_mp3 = Gst.filename_to_uri(mp3_file)
    #print(uri_mp3) # file:///home/ian/google_talk/yakety_yak.mp3
    main(uri_mp3)

"""
Documentation:

Python GStreamer Tutorial:
https://brettviren.github.io/pygst-tutorial-org/pygst-tutorial.html

GStreamer tutorial's in C langauge:
https://gstreamer.freedesktop.org/documentation/tutorials/index.html?gi-language=c

https://gstreamer.freedesktop.org/documentation/playback/playbin.html?gi-language=c

Examples of using Gst.parse_launch()

https://www.programcreek.com/python/example/88576/gi.repository.Gst.parse_launch
See example for: Project: PartyZone   Author: glennpierce   File: play-slave.py 


PyGIDeprecationWarning: GObject.MainLoop is deprecated; use GLib.MainLoop instead
  loop = GObject.MainLoop()
  
"""

