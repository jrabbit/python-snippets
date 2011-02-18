#!/usr/bin/env python

import sys
import os
import re
import platform
from subprocess import *
import feedparser
import anydbm
from BeautifulSoup import BeautifulSoup

from appscript import app, mactypes

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
        Popen(['curl', '-C', '-', '-O', '-L', url], cwd=dl_dir).communicate()
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
        return resolution.split()[1] + 'x' + resolution.split()[3]

def set_desktop_mac(path):
    # /usr/bin/defaults write /Library/Preferences/com.apple.loginwindow DesktopPicture "/path/to/the picture.jpg"
    app('Finder').desktop_picture.set(mactypes.File(path))

if __name__ == '__main__':
    db = get_db()
    if is_first_run():
        db['size'] = get_resolution()
    set_desktop_mac(download(get_wallpapers()[db['size']]))