# This in theory works, but there are an unfortunate amount of regexs that match wallhaven's
# urls and not enough wallpapers to make it work.  It just generates url's that are
# technically valid, there just aren't wallpapers there :(
import sys
import os
import wget
import exrex
import random

def geturl ():
    #d = exrex.getone ('([a-z]|[0-9]){2}')
    affix = exrex.getone ('([a-z]|[0-9]){6}')
    #url = "https://w.wallhaven.cc/full/" + d + "/wallhaven-" + affix + ".jpg"
    url = "https://wallhaven.cc/w/" + affix
    return url

def wgetfile (url):
    try:
        return wget.download (url)
    except Exception:
        return 0
    
def main ():
    file = 0
    while file == 0:
        file = wgetfile (geturl ())
    print (url)

main ()
