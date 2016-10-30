#     This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.



# Use the python-twitter library to authenticate with the Twitter API,
# fetch a user, and then print a selection of data. After that, fetch
# a user timeline and print some statuses.

import twitter

api = twitter.Api(consumer_key='your-consumer-key',
                  consumer_secret='your-consumer-secret',
                  access_token_key='your-access-token-key',
                  access_token_secret='your-access-token-secret')

# set a handle
handle = 'anthonydb'

# Get some info on a user
user = api.GetUser(screen_name=handle)

print user.GetName()
print user.GetDescription()
print user.GetFollowersCount()
print user.GetStatusesCount()
print user.GetUrl()

# get a user timeline
statuses = api.GetUserTimeline(screen_name='pokjournal', count=1)
print [s.text for s in statuses]

