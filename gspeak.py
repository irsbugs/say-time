#!/usr/bin/env python3
#!
# gspeak.py
# Requires: mpv. $ apt install mpv
#
# Accept a string of text as an argument, send it to google translate,
# the returned .mp3 data is fed to mpv to produce the audio. 
#
# Call via bash or install as a python module.
#
# Ian Stewart - March 2019
#
import sys
import subprocess
import urllib.parse
import urllib.request

def gspeak(message='Hello World', language='en'):
    """
    Use google translate to do text to speech translation.
    Use mpv to play the mp3 data.
    message = text to be converted to speech
    language = en is English, fr is French, de is German, etc.
    """
    # Build the url string.
    url = 'https://translate.google.com/translate_tts'
    user_agent = 'Mozilla'
    values = {'tl' : language,
              'client' : 'tw-ob',
              'ie' : 'UTF-8',
              'q' : message }

    data = urllib.parse.urlencode(values)
    headers = { 'User-Agent' : user_agent }

    req = urllib.request.Request(url + "?" + data, None, headers)

    # mpv seems to work better than mplayer. Doesn't have connect messages 
    player = subprocess.Popen \
      (
        args = ("mpv", "-cache", "1024", "-really-quiet", "/dev/stdin"),
        stdin = subprocess.PIPE
       )
    # Send the request to google, and send mp3 data to mp3 player.
    try:
        with urllib.request.urlopen(req) as response:
            mp3_data = response.read()
            player.stdin.write(mp3_data)

    except urllib.error.URLError as e:
        #print(e)
        #print(e.reason)
        #print(e.read())
        print("gspeak error: urllib.error.URLError - check network connection")

    except socket.gaierror as e:
        #print(e)
        #print(e.reason)
        #print(e.read())
        print("gspeak error: socket.gaierror - check network connection")

    except:
        print("gspeak error: Unknown - check network connection.")

    player.stdin.close()
    player.wait() # fixme: should check return status


if __name__=="__main__":

    gspeak("gspeak is a python3 program that uses google translate.")
    gspeak("bonjour", "fr")
    gspeak("guten Morgen", "de")

'''
Google Translate as of March 2019
56 Languages it can speak
Code    Language    Audio
-------------------------
af		Afrikaans   *
sq		Albanian    *
am		Amharic
ar		Arabic      *
hy		Armenian    *
az		Azerbaijani
eu		Basque
be		Belarusian
bn		Bengali     *
bs		Bosnian     *
bg		Bulgarian
ca		Catalan     *
ceb		Cebuano
ny		Chichewa
zh-CN   Chinese Simplified  *
zh-TW   Chinese Traditional *
co		Corsican
hr		Croatian    *
cs		Czech       *
da		Danish      *
nl		Dutch       *
en		English     *
eo		Esperanto   *
et		Estonian    *
tl		Filipino    *
fi		Finnish     *
fr		French      *
fy		Frisian
gl		Galician
ka		Georgian
de		German      *
el		Greek       *
gu		Gujarati
ht		Haitian Creole
ha		Hausa
haw		Hawaiian
iw		Hebrew
hi		Hindi       *
hmn		Hmong
hu		Hungarian   *
is		Icelandic   *
ig		Igbo
id		Indonesian  *
ga		Irish
it		Italian     *
ja		Japanese    *
jw		Javanese    *
kn		Kannada
kk		Kazakh
km		Khmer       *
ko		Korean      *
ku		Kurdish (Kurmanji)
ky		Kyrgyz
lo		Lao
la		Latin       *
lv		Latvian     *
lt		Lithuanian
lb		Luxembourgish
mk		Macedonian  *
mg		Malagasy
ms		Malay
ml		Malayalam   *
mt		Maltese
mi		Maori
mr		Marathi     *
mn		Mongolian
my		Myanmar (Burmese) *
ne		Nepali      *
no		Norwegian   *
ps		Pashto
fa		Persian
pl		Polish      *
pt		Portuguese  *
pa		Punjabi
ro		Romanian    *
ru		Russian     *
sm		Samoan
gd		Scots Gaelic
sr		Serbian     *
st		Sesotho
sn		Shona
sd		Sindhi
si		Sinhala     *
sk		Slovak      *
sl		Slovenian
so		Somali
es		Spanish     *
su		Sundanese   *
sw		Swahili     *
sv		Swedish     *
tg		Tajik
ta		Tamil       *
te		Telugu      *
th		Thai        *
tr		Turkish     *
uk		Ukrainian   *
ur		Urdu
uz		Uzbek
vi		Vietnamese  *
cy		Welsh       *
xh		Xhosa
yi		Yiddish
yo		Yoruba
zu		Zulu
'''
  
    
