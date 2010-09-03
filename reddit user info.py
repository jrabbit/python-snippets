from urllib2 import urlopen
import simplejson as json
import sys

user = sys.argv[1]
url = 'http://www.reddit.com/user/%s/about.json' % user
raw = urlopen(url).read()
data = json.loads(raw)['data']
#print data
karma = data['link_karma']
comment = data['comment_karma']
print "%s has %s link karma and %s comment karma: http://www.reddit.com/user/%s" % (user, karma, comment, user)