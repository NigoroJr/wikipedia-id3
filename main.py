#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import re
import sys
from html.parser import HTMLParser

import urllib3
import taglib

class MyHTMLParser(HTMLParser):
    ignore_tags = {'ul', 'dl', 'dd'}

    def __init__(self, target_ol_count = 1):
        self.target_ol_count = target_ol_count
        self.ol_count = 1

        self.in_ol = False
        self.in_li = False
        self.skip_depth = 0
        self.titles = []
        self.title_str = ''
        super(MyHTMLParser, self).__init__()

    def handle_starttag(self, tag, attrs):
        # Wait till given count
        if self.ol_count != self.target_ol_count:
            return

        if tag == 'ol':
            self.in_ol = True
        elif tag == 'li' and self.in_ol and self.skip_depth == 0:
            self.in_li = True
        elif tag in self.ignore_tags:
            self.skip_depth += 1

    def handle_endtag(self, tag):
        if tag == 'ol':
            self.in_ol = False
            self.ol_count += 1

        # Wait till given count
        elif self.ol_count != self.target_ol_count:
            return

        elif tag == 'li' and self.in_li and self.skip_depth == 0:
            self.in_li = False

            self.add_title(self.title_str)   # Add title to list
            self.title_str = ''              # Reset title

        elif tag in self.ignore_tags:
            self.skip_depth -= 1

    def handle_data(self, data):
        # Skipping irrelevant tags?
        if self.skip_depth > 0:
            return

        # Nth <ol> tag that we're looking for?
        if self.ol_count != self.target_ol_count:
            return

        # Empty?
        data = data.rstrip()
        if not data:
            return

        # Concatenate string of partial title (e.g. when there is a href)
        if self.in_li:
            self.title_str += data

    def add_title(self, title):
        # Empty?
        if not title:
            return

        # Remove [TIME] e.g. 'Title [3:35]' => 'Title'
        title = re.sub('\s*\[.*?\]\s*$', '', title)

        self.titles.append(title)


def get_titles(url, ol_count = 1):
    http = urllib3.PoolManager()
    response = http.request('GET', url)

    parser = MyHTMLParser(ol_count)
    parser.feed(response.data.decode('utf-8'))

    return parser.titles

def set_track_titles(titles, files, artist):
    n = min(len(titles), len(files))    # Whichever's shorter
    for i in range(n):
        f = taglib.File(files[i])

        if artist:
            f.tags['ARTIST'] = artist

        f.tags['TITLE'] = titles[i]
        digits = len(str(len(titles)))
        f.tags['TRACKNUMBER'] = ['%0*d/%d' % (digits, i, len(titles))]

        retval = f.save()
        if len(retval) != 0:
            print('Something went wrong while saving {0}'.format(files[i]))
        else:
            print('Saved tags to {0}'.format(files[i]))


argparser = argparse.ArgumentParser()
argparser.add_argument('--ol-count',  type=int, default=1, metavar='N',
        help='use Nth <ol> tag as the list of track titles')
argparser.add_argument('--artist', help='album artist')
argparser.add_argument('url')
argparser.add_argument('files', nargs='+', help='files to write the tags to')

args = argparser.parse_args()
url = args.url
ol_count = args.ol_count
files = args.files
artist = args.artist

# print(get_titles(url, ol_count))
titles = get_titles(url, ol_count)
set_track_titles(titles, files, artist)
