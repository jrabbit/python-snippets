#!/usr/bin/env python

import sys
import os
import re
import platform
from subprocess import *
from decimal import *
import math
import feedparser
import anydbm
from BeautifulSoup import BeautifulSoup

if platform.system() == 'Darwin':
    from appscript import app, mactypes
if platform.system() == 'Windows':
    from ctypes import windll
    from PIL import Image

def get_wallpapers(entry=0):
    feed = "http://thefoxisblack.com/category/the-desktop-wallpaper-project/feed/"
    d = feedparser.parse(feed)
    soup = BeautifulSoup(d.entries[entry].content[0].value)
    urls = {}
    for x in soup.findAll('a'):
        if  x['href'].split('-')[-1][-3:] == "jpg":
            urls[x['href'].split('-')[-1][:-4]] = x['href']
    return urls

def directory(name="foxwallpaper"):
    """Construct a directory from os name"""
    home = os.path.expanduser('~')
    if platform.system() == 'Linux':
        app_dir = os.path.join(home, '.' + name)
    elif platform.system() == 'Darwin':
        app_dir = os.path.join(home, 'Library', 'Application Support',
         name)
    elif platform.system() == 'Windows':
        app_dir = os.path.join(os.environ['appdata'], name)
    else:
        app_dir = os.path.join(home, '.' + name)
    if not os.path.isdir(app_dir):
        os.mkdir(app_dir)
    return app_dir


def get_db():
    db = anydbm.open(os.path.join(directory(), 'settings'), 'c')
    return db

def is_first_run():
    if 'size' not in get_db():
        return True
    else:
        return False

def download(url):
    try:
        Popen(['wget', '-c', url], cwd=directory()).communicate()
    except OSError:
        Popen(['curl', '-C', '-', '-O', '-L', url], cwd=directory()).communicate()
    return os.path.join(directory(), url.split('/')[-1])

def get_resolution():
    try:
        #Prefered xrandr method. Broken on stock Apple X11.
        out = Popen(['xrandr'], stdout=PIPE, stderr=PIPE).communicate()[0]
        real = out.split('\n')[0].split(',')[-1].split()
        return real[1] + 'x' + real[3]
    # /usr/sbin/system_profiler SPDisplaysDataType | grep Resolution
    except IndexError:
        profiler = Popen(['system_profiler', 'SPDisplaysDataType'],
        stdout=PIPE, stderr=PIPE).communicate()[0]
        expr = re.compile('Resolution')
        resolution = filter(expr.search, profiler.splitlines())[0]
        return round_resolution(resolution.split()[1])

def round_resolution(xval):
    """Take resolution and round it (Upward, the image setter can scale it) to the closest availible image size. Justification for x value: widescreens."""
    #(Decimal(decimal)/nearest).quantize(1)*nearest
    res_x = xval
    avail = {1440:900, 1920:1200, 1280:800, 1680:1050, 2560:1440}
    z = {}
    for given_x in avail.keys():
        z[math.fabs(1 - (Decimal(res_x)/Decimal(given_x)))] = given_x
    good_x = z[min(z.keys())]
    return str(good_x) + 'x' + str(avail[good_x])
#Windows Stuff
def convert_img(img):
    "Refrenced http://gabbpuy.blogspot.com/2007/02/set-windows-wallpaper-from-python.html"
    savename = os.path.join( directory(), img[:-4] + '.bmp')
    image = Image.open(img)
    image.save(savename, "BMP")
    return savename
def set_desktop_win(path):
    "Must be BMP or jpg in >XP"
    SPI_SETDESKWALLPAPER = 20
    windll.user32.SystemParametersInfoA(SPI_SETDESKWALLPAPER, 0, path , 0)
    
#end windows stuff
def set_desktop_mac(path):
    # /usr/bin/defaults write /Library/Preferences/com.apple.loginwindow DesktopPicture "/path/to/the picture.jpg"
    app('Finder').desktop_picture.set(mactypes.File(path))

def set_desktop_feh(path):
    #feh --bg-fill file
    # Also --bg-scale, --bg-seamless, --bg-tile exist
    Popen(['feh', '--bg-fill', path]).communicate()

if __name__ == '__main__':
    db = get_db()
    if is_first_run():
        db['size'] = get_resolution()
    if platform.system() == 'Darwin':
        set_desktop_mac(download(get_wallpapers()[db['size']]))
    if platform.system() == 'Linux':
        set_desktop_feh(download(get_wallpapers()[db['size']]))
    if platform.system() == 'Windows':
        set_desktop_win(convert_img(download(get_wallpapers()[db['size']])))