#!/usr/bin/env python3
#!
# check_internet.py
# Returns: True or False
# Call with: from pylib.check_internet import is_internet
# Use in bash or python script: internet_available = is_internet()
#
# Check if the internet is available by connecting to Google DNS at 8.8.8.8
#
# Example of use:
# Could be used before using google translate web-site and fall back to 
# espeak if no network avaialble.
#
# Ian Stewart - Mar 2019
#
import socket

def is_internet(host="8.8.8.8", port=53, timeout=3):
    """
    Host: 8.8.8.8 (google-public-dns-a.google.com)
    OpenPort: 53/tcp
    Service: domain (DNS/TCP)
    """
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except Exception as ex:
        #print(ex.message)
        return False

if __name__ == "__main__":

    # Check if internet available and log the time taken
    from timeit import default_timer as timer
    start = timer()
    internet_available = is_internet()
    end = timer()

    print("Time taken to check google DNS site was {:.3f} seconds"
        .format(end - start))

    print("The internet is available: {}".format(internet_available))

"""
root@kepler:~# test-check-internet
0.0867110799999864
The internet is available: True
root@kepler:~# test-check-internet
0.08389811899996857
The internet is available: True
root@kepler:~# test-check-internet
0.14388215899998613
The internet is available: True
root@kepler:~# test-check-internet
0.14845634199991764
The internet is available: True

===

Example of time-out from print(ex.message)

root@kepler:~# is-internet
Traceback (most recent call last):
  File "/root/bin/pylib/check_internet.py", line 26, in is_internet
    socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
socket.timeout: timed out

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/root/bin/is-internet", line 8, in <module>
    internet_available = is_internet()
  File "/root/bin/pylib/check_internet.py", line 29, in is_internet
    print(ex.message)
AttributeError: 'timeout' object has no attribute 'message'
root@kepler:~# 

===


https://stackoverflow.com/questions/3764291/checking-network-connection

If we can connect to some Internet server, then we indeed have connectivity. 
However, for the fastest and most reliable approach, all solutions should 
comply with the following requirements, at the very least:

o Avoid DNS resolution (we will need an IP that is well-known and guaranteed 
  to be available for most of the time)
o Avoid application layer based connections (connecting to a HTTP/FTP/IMAP 
  service)
o Avoid calls to external utilities from Python or other language of choice 
  (we need to come up with a language-agnostic solution that doesn't rely on 
  third-party solutions)

To comply with these, one approach could be to, check if one of the Google's 
public DNS servers is reachable. The IPv4 addresses for these servers are 
8.8.8.8 and 8.8.4.4. We can try connecting to any of them.


Before we try with Python, let's test connectivity using Netcat:
nc - TCP/IP swiss army knife

root@kepler:~# nc 8.8.8.8 53 -zv
google-public-dns-a.google.com [8.8.8.8] 53 (domain) open

Netcat confirms that we can reach 8.8.8.8 over TCP/53. Now we can set up a 
socket connection to 8.8.8.8:53/TCP in Python to check connection:

"""
