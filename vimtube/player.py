import urllib.request
import urllib.parse
import re
from html.parser import HTMLParser
from collections import namedtuple
import pafy
import vlc

Results_template = namedtuple('entry', 'title url')
yt_url = 'https://www.youtube.com'

class parse(HTMLParser):
    def __init__(self, html=None):
        HTMLParser.__init__(self)
        self.results = list()
        if html != None:
            self.feed(html)
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            check = 0
            for name, data in attrs:
                if name == 'title':
                    title = data
                    check += 1
                elif name == 'href':
                    if re.match(r'^\/watch\?v=(.{11})$', data) == None:
                        return
                    else:
                        url = data
                        check += 1
            if check == 2:
                self.results.append(Results_template(title=title, url=url))

class player:
    def __init__(self, video=None):
        self.video = video
        self.status = None
        self.catalogue = list()

    def load(self, selection=0):
        if len(self.catalogue) > 0:
            self.video = pafy.new(yt_url + self.catalogue[selection].url)

    def play(self):
        if self.status is not None:
            self.player.set_mrl(self.video.getbest().url)
            self.stop()
        self.player = vlc.MediaPlayer(self.video.getbest().url)
        self.player.play()
        self.status = 1

    def pause(self):
        try:
            self.player.pause()
        except:
            pass

    def seek(self, second):
        try:
            self.player.set_time(self.player.get_time() + second * 1000)
        except:
            pass

    def stop(self):
        if self.status is not None:
            self.player.stop()
            self.status = None

    def search(self, query):
        enc_query = urllib.parse.urlencode({'search_query': query})
        html = urllib.request.urlopen(yt_url + '/results?' + enc_query)
        parser = parse(html.read().decode())
        self.catalogue = parser.results
