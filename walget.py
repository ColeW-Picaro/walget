# Pulls down wallhaven home page and extracts image codes of top papes
import sys
import os
import exrex
import re
import random
import urllib.request
import pywal

# Return url with images
def geturl ():
    #d = exrex.getone ('([a-z]|[0-9]){2}')
    #affix = exrex.getone ('([a-z]|[0-9]){6}')
    #url = "https://w.wallhaven.cc/full/" + d + "/wallhaven-" + affix + ".jpg"
    url = 'https://wallhaven.cc/'
    return url

# Append 6 character code on wallhaven url
def getCodeUrl (code):
    return 'https://wallhaven.cc/w/' + code

# pulls html from url
def getFile (url):
    req = urllib.request.Request (url, headers={'User-Agent': 'Mozilla/5.0'})
    html = urllib.request.urlopen (req).read ().decode ('utf-8')
    return html

# finds all "lg-thumb" spans in html and extracts the 6 character code
# sample link
# https://th.wallhaven.cc/small/6k/6kyk9w.jpg
# turns into:
# https://w.wallhaven.cc/full/39/wallhaven-39gogv.jpg


def getImageLinks (html):
    thumbs = re.findall ('img src="[^"<>]*"', html)
    thumblist = []
    for thumb in thumbs:        
        if "user" in thumb:
            continue
        # A lot of unfortuante regex subs to turn a thumbnail link to full size image link
        # It sucks, but it works 
        try:
            thumb = re.sub ('img src=', '', thumb)
            thumb = re.sub ('/th.', '/w.', thumb)
            thumb = re.sub ('/small/', '/full/', thumb)
            thumb = re.sub ('/lg/', "/full/", thumb)
            code = re.search ('\w{6}.jpg', thumb).group ()
            thumb = re.sub ('\w{6}.jpg', "wallhaven-" + code, thumb)
            thumb = re.sub ('"', '', thumb)
            thumblist.append (thumb)
        except Exception as e:
            print (e)
    return thumblist

# Downloads the image from url
def downloadImage (url):
    req = urllib.request.Request(url, headers={'User-Agent' : "Magic Browser"}) 
    image = urllib.request.urlopen (req).read ()
    #urllib.request.Request (url, headers={'User-Agent': 'Mozilla/5.0'})
    return image

def main ():
    # Get homepage html
    html = getFile (geturl ())
    # Find top image codes
    links = getImageLinks (html)
    # Extract Code URL at random
    # Download the image
    image = downloadImage (random.choice (links))
    f = open ("image.jpg", "wb")
    f.write (image)
    f.close ()
    return

main ()
