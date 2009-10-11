#!/usr/bin/env python
# -*- coding: utf-8 -*-

from urllib import urlopen
from xml.etree import cElementTree as etree
import os


URL="http://radiofrance-podcast.net/podcast09/rss_13364.xml"
NICKNAME="Papous"

MOUNTHS=[
"Jan",
"Feb",
"Mar",
"Apr",
"May",
"Jun",
"Jui",
"Aug",
"Sep",
"Oct",
"Nov",
"Dec"]

OUTPUT = "~/Podcasts"

OUTPUT = os.path.expanduser(OUTPUT)

class Podcast():
    """
    Class to represent a podcast.

    It has a nick name, a date, and a url to download content.

    """
    def __init__(self, nick_name):
        self.nick_name = nick_name
        self.date      = "now"
        self.url       = None



class PodcastDownloader:
    """
    Initialized with a nickname and a url.

    Retrieve the rss file from the URL, downlaod it,
    look for guid and date attributes, then save file in
    OUTPUT/nickname/date.mp3

    """
    def __init__(self, url, nick_name):
        self.url       = url
        self.nick_name = nick_name
        self.podcast   = Podcast(nick_name)


    def download(self):
        """
        Main method.

        """
        self.retrieve_info()
        self.retrieve_content()


    def retrieve_info(self):
        """
        Retrieve the XML Rss file, and updates the podcast object

        """
        xml_file = urlopen(self.url)
        xml_tree = etree.parse(xml_file)
        xml_channel  = xml_tree.find("channel")
        xml_item     = xml_channel.find("item")
        xml_guid     = xml_item.find("guid").text
        xml_pub_date = xml_item.find("pubDate").text

        day    = int(xml_pub_date.split()[1])
        mounth = MOUNTHS.index(xml_pub_date.split()[2]) + 1
        year   = int(xml_pub_date.split()[3])

        date = "{0:04}-{1:02}-{2:02}".format(year, mounth, day)

        self.podcast.url   = xml_guid
        self.podcast.date  = date


    def retrieve_content(self):
        """
        Now that we got the information (the URL and the date),
        get the file and save it.

        """
        output_path = os.path.join(OUTPUT, self.podcast.nick_name)

        # Get filename extension from URL:
        file_extension = self.podcast.url.split(".")[-1]
        file_name = self.podcast.date + "." + file_extension
        file_path = os.path.join(output_path, file_name)

        print "Downloading ", self.podcast.url
        print "Saving to", file_path
        if not os.path.exists(output_path):
            os.mkdir(output_path)

        content = urlopen(self.podcast.url).read()
        output = open(file_path, "wb")
        output.write(content)
        output.close()



def _get_config():
    """
    Read .config/pypodget/serverlist.

    Returns a list of tuples (<urls>, <nicknames>)

    """
    res = []
    config_path = os.path.expanduser("~/.config/pypodget/serverlist")
    config = open(config_path, "r")
    lines = config.readlines()
    config.close()
    for line in lines:
        if line.startswith("#"):
            continue
        if len(line.split()) != 2:
            continue
        [url, nickname] = line.split()
        res.append((url, nickname))
    return res



def main():
    """
    Manages options when called from command-line
    """
    serverlist = _get_config()
    for (url, nick_name) in serverlist:
        podcast_downloader = PodcastDownloader(url, nick_name)
        podcast_downloader.download()


if __name__ == "__main__" :
    main()

