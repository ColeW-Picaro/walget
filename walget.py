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

# Taken almost directly from the pywal wiki
def walImage ():
    """Main function."""
    CACHE_DIR = os.path.join(os.environ["HOME"], ".cache/wal")
    # Validate image and pick a random image if a
    # directory is given below.
    image = pywal.image.get("image.jpg")

    # Return a dict with the palette.
    # Set quiet to 'True' to disable notifications.
    colors = pywal.colors.get(image)
    print (colors)

    # Apply the palette to all open terminals.
    # Second argument is a boolean for VTE terminals.
    # Set it to true if the terminal you're using is
    # VTE based. (xfce4-terminal, termite, gnome-terminal.)


    pywal.export.every(colors)
    
    # Export individual template files.
    pywal.export.color(colors, "xresources", 
                       os.path.join(CACHE_DIR, "colors.xresources"))
    pywal.export.color(colors, "shell", 
                       os.path.join(CACHE_DIR, "colors.bash"))

    pywal.sequences.send(colors, CACHE_DIR)

    # Reload xrdb, i3 and polybar.
    pywal.reload.env()

    # Reload individual programs.
    pywal.reload.i3()
    pywal.reload.polybar()
    pywal.reload.xrdb()

    # Set the wallpaper.
    pywal.wallpaper.change(image)
    return

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
    # Run it through pywal
    walImage ()
    f.close ()


main ()
