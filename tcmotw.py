from BeautifulSoup import BeautifulSoup
import re
import urllib2
import urllib

def grab(user, passwd):
    o = urllib2.build_opener( urllib2.HTTPCookieProcessor() )
    urllib2.install_opener( o )
    values = {'username' : user, 'password' : passwd}
    url = 'https://tehconnection.eu/login.php'
    data = urllib.urlencode(values)
    o.open(url, data)
    f = o.open('https://tehconnection.eu/index.php')
    the_page = f.read()
    f.close()
    return the_page


def motw(user, passwd):
    html = grab(user, passwd)
    soup = BeautifulSoup(html)
    #find <div class="alertbar notify_box">
    #<a href="torrents.php?id=525">Lord of War</a> is the movie of the week! </div>
    motw = soup.findAll('div', 'alertbar notify_box')[0].['a'].contents
    return motw

if __name__ == "__main__":
    import sys
    user = sys.argv[1]
    passwd = sys.argv[2]
    print motw(user, paswd)
