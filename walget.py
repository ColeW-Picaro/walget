# Pulls down wallhaven home page and extracts image codes of top papes
import sys
import os
import exrex
import re
import random
import urllib.request
import pywal


def geturl ():
    #d = exrex.getone ('([a-z]|[0-9]){2}')
    #affix = exrex.getone ('([a-z]|[0-9]){6}')
    #url = "https://w.wallhaven.cc/full/" + d + "/wallhaven-" + affix + ".jpg"
    url = 'https://wallhaven.cc/'
    return url

def getCodeUrl (code):
    return 'https://wallhaven.cc/w/' + code

def getFile (url):
    req = urllib.request.Request (url, headers={'User-Agent': 'Mozilla/5.0'})
    html = urllib.request.urlopen (req).read ().decode ('utf-8')
    return html

# finds all "lg-thumb" spans in html and extracts the 6 character code
def getImageCodes (html):
    thumbs = re.findall ('<span class="lg-thumb"><a href="[^"><]*">', html)
    thumblist = []
    for thumb in thumbs:
        thumb = re.sub ('<span class="lg-thumb"><a href="https://wallhaven.cc/w/', '', thumb)
        thumb = re.sub ('">', '', thumb)
        thumblist.append (thumb)
    return thumblist

# Another regex sub to extract full link
def getImageLink (html):
    wallpaper = re.search ('<img id="wallpaper" src="https://w.wallhaven.cc/full/.{2}/wallhaven-.{6}.jpg"', html).group ()
    wallpaper = re.sub ('<img id="wallpaper" src="', '', wallpaper)
    wallpaper = re.sub ('"', '', wallpaper)
    return wallpaper

def downloadImage (url):
    req = urllib.request.Request(url, headers={'User-Agent' : "Magic Browser"}) 
    image = urllib.request.urlopen (req).read ()
    #urllib.request.Request (url, headers={'User-Agent': 'Mozilla/5.0'})
    return image

def main ():
    # Get homepage html
    html = getFile (geturl ())
    # Find top image codes
    codes = getImageCodes (html)
    # Extract Code URL at random
    html = getFile (getCodeUrl (random.choice (codes)))
    # Download the image
    wallpaper = getImageLink (html)
    image = downloadImage (wallpaper)
    f = open ("image.jpg", "wb")
    f.write (image)
    f.close ()
    return

main ()
