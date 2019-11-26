# Pulls down wallhaven home page and extracts image codes of top papes
import sys
import os
import re
import random
import urllib.request

# Global function: Used by all classes
# pulls html from url
def getHtml (url):
    try:
        req = urllib.request.Request (url, headers={'User-Agent': 'Mozilla/5.0'})
        html = urllib.request.urlopen (req).read ().decode ('utf-8')
        return html
    except urllib.error.URLError as e:
        print (e)
        exit ()


# Global function: Used by all classes
# Downloads the image from url
def getImage (url):
    try:
        req = urllib.request.Request(url, headers={'User-Agent' : "Magic Browser"}) 
        image = urllib.request.urlopen (req).read ()
        #urllib.request.Request (url, headers={'User-Agent': 'Mozilla/5.0'})
        return image
    except urllib.error.URLError as e:
        print (e)
        return 0

# wallhaven.cc specific behaviors
class wallhaven ():
    # ctor to initalize wallhaven homepage as url
    def __init__ (self):
        self.url = 'https://wallhaven.cc'
        self.html = getHtml (self.url)
        self.thumblist = []
    # Returns url
    def geturl (self):
        return url
    # Returns thumbnail list
    def getThumblist (self):
        return self.thumblist
    def getHtml (self):
        return self.html
    # Sets html of this object
    def setHtml (self, html):
        self.html = html
        return    
    # finds all img srcs in html and turns it into a full size link
    # sample link
    # https://th.wallhaven.cc/small/6k/6kyk9w.jpg
    # turns into:
    # https://w.wallhaven.cc/full/39/wallhaven-39gogv.jpg
    def genThumblist (self):
        thumbs = re.findall ('img src="[^"<>]*"', self.html)
        for thumb in thumbs:        
            if "user" in thumb:
                continue
            elif "logo" in thumb:
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
                self.thumblist.append (thumb)
            except Exception as e:
                print (thumb)                
        return
        
def main ():
    w = wallhaven ()
    w.genThumblist ()
    tl = w.getThumblist ()
    # Open file and save it
    image = 0
    while image == 0:
        image = getImage (random.choice (tl))
    f = open ("image.jpg", "wb")
    f.write (image)
    f.close ()
    return

main ()
