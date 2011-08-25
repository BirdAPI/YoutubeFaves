echo %date%
python "youtube-dl/youtube-dl" -w -i -o "%1/%%(stitle)s-%%(id)s.%%(ext)s" -a favs.txt
