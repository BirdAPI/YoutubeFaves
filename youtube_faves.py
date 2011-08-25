import sys
import os
import gdata.youtube
import gdata.youtube.service

#******************GLOBALS**************************
yt_service = gdata.youtube.service.YouTubeService()
yt_service.ssl = False
yt_service.developer_key = "AI39si7jh-vsFCUaY3E8gJmA60BWNX7fafF_StEX1wkr1VwZ1xoN2KQ4io-wL7B_eC5hc1xaVa3iza41q1AXtal_FelY8XrvGw"
#***************************************************

def get_id_from_url(url):
	url = url.replace("&feature=youtube_gdata_player", "")
	id = url[url.rfind("=") + 1:]
	return id

def get_recent_ids(user):
	ids = []
	feed = yt_service.GetUserFavoritesFeed(username=user) 
	for entry in feed.entry: 
		id = get_id_from_url(entry.media.player.url)
		ids.append(id)
	return ids

def get_favorites_ids(user):
	ids = []
	feed = yt_service.GetUserFavoritesFeed(username=user) 
	while feed is not None: 
	  for entry in feed.entry: 
		id = get_id_from_url(entry.media.player.url)
		ids.append(id)
	  if feed.GetNextLink() is not None: 
		feed = yt_service.GetYouTubeVideoFeed(feed.GetNextLink().href) 
	  else: 
		feed = None 
	return ids
	
def get_only_new_ids(user, dl_path, delete_part_files):
	ids = get_favorites_ids(user)
	for file in os.listdir(dl_path):
		if delete_part_files and file.endswith(".part"):
			os.remove(file)
		else:
			for id in ids:
				if id in file:
					ids.remove(id)
					break
	return ids

def print_ids(ids):
	for id in ids:
		print "http://www.youtube.com/watch?v=%s" % id
	
def print_all_ids(user):
	ids = get_favorites_ids(user)
	print_ids(ids)

def print_new_ids(user, dl_path, delete_part_files):
	ids = get_only_new_ids(user, dl_path, delete_part_files)
	print_ids(ids)
	
def main(argv=None):
    if argv is None:
        argv = sys.argv
	if len(argv) == 2:
		print_all_ids(argv[1])
	elif len(argv) == 3:
		print_new_ids(argv[1], argv[2], True)
	else:
		print "Usage: %s username [download_path]" % argv[0].replace("\\", "/")[argv[0].rfind("/") + 1:]

if __name__ == "__main__":
    sys.exit(main())
