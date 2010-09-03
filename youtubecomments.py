import gdata.youtube
import gdata.youtube.service
from BeautifulSoup import BeautifulSoup

yt_service = gdata.youtube.service.YouTubeService()
# The YouTube API does not currently support HTTPS/SSL access.
yt_service.ssl = False
yt_service.developer_key = "AI39si6sDAt4km6PVp3cw5U4MIoUAVKi-R0hVSALYdjz7EIH_Leik-7s_fxeHQZKpx6fXilSx5PvYqhk16Gg1APQFJDRncXh6g"
yt_service.client_id = "yt comments"
def get_comments():
    feed = yt_service.GetRecentlyFeaturedVideoFeed()
    #comment_feed = yt_service.GetYouTubeVideoCommentFeed(video_id=youtube_id)
    for entry in feed.entry:
        url = BeautifulSoup(str(entry.comments)).find('ns0:feedlink')['href']
        comment_feed = yt_service.GetYouTubeVideoCommentFeed(url)
        for comment_entry in comment_feed.entry:
          return str(BeautifulSoup(comment_entry.ToString()).find('ns0:content').contents)
          #find ns0:content and get content, make it nonutf.

if __name__ == '__main__':
    print get_comments()
    