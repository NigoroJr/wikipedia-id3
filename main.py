#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os.path
import re
import sys
from html.parser import HTMLParser
import urllib.parse

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

def set_track_titles(titles, files, artist, album, year):
    n = min(len(titles), len(files))    # Whichever's shorter
    for i in range(n):
        f = taglib.File(files[i])

        # Remove comments
        if 'COMMENT' in f.tags:
            del(f.tags['COMMENT'])

        if artist:
            f.tags['ARTIST'] = artist
        if album:
            f.tags['ALBUM'] = album
        if year:
            f.tags['DATE'] = year

        f.tags['TITLE'] = titles[i]
        digits = len(str(len(titles)))
        f.tags['TRACKNUMBER'] = ['%0*d/%d' % (digits, i, len(titles))]

        retval = f.save()
        if len(retval) != 0:
            print('Something went wrong while saving {0}'.format(files[i]))
        else:
            print('Saved tags to {0}'.format(files[i]))

def rename_files(titles, files):
    n = min(len(titles), len(files))    # Whichever's shorter
    for i in range(n):
        title = titles[i]
        old_file_path = files[i]
        extension = re.sub('.*\.', '', old_file_path)

        dir_name = os.path.dirname(old_file_path)
        old_file_name = os.path.basename(old_file_path)
        new_file_name = "{0:02d}. {1}.{2}".format(i + 1, title, extension)

        # Replace only the file path
        new_file_path = os.path.join(dir_name, new_file_name)

        os.rename(old_file_path, new_file_path)
        print("Renamed: {0}\n\t=> {1}".format(old_file_name, new_file_name))

def print_titles(titles, artist=None, album=None, year=None):
    print('Changes to be written')
    if artist:
        print('{0:<6s}: {1}'.format('Artist', artist))
    if album:
        print('{0:<6s}: {1}'.format('Album', album))
    if year:
        print('{0:<6s}: {1}'.format('Year', year))

    print('{0:<6s}: {1}'.format('Track', 'Title'))
    print('--------------------------------------')
    fmt = '    {track_num:02d}. {title}'
    for i in range(len(titles)):
        print(fmt.format(track_num=i + 1, title=titles[i]))


argparser = argparse.ArgumentParser()
# Options
argparser.add_argument('--ol-count',  '-o', type=int, default=1, metavar='N',
        help='use Nth <ol> tag as the list of track titles')
argparser.add_argument('--artist', '-ar',
        help='album artist')
argparser.add_argument('--album', '-al',
        help='album name')
argparser.add_argument('--album-from-url', '-au', action='store_true',
        help='album name from url')
argparser.add_argument('--year', '-y',
        help='year the album was released')
argparser.add_argument('--rename', '-r', action='store_true',
        help='rename files to track titles in the format of "01. Foobar.mp3"')
argparser.add_argument('--test', '-t', action='store_true',
        help='only display the titles')

# Required
argparser.add_argument('url')

# Required unless test
argparser.add_argument('files', nargs=argparse.REMAINDER,
        help='files to write the tags to')

args = argparser.parse_args()

if not args.test and len(args.files) == 0:
    argparser.error('must specify files unless test')

album_name = None
if args.album:
    album_name = args.album
elif args.album_from_url:
    o = urllib.parse.urlparse(args.url)
    url_path = urllib.parse.unquote(o.path, 'utf-8')
    # Remove '/wiki/'
    album_name = re.sub('\/wiki\/', '', url_path)

titles = get_titles(args.url, args.ol_count)

# Only titles and exit
if args.test:
    print_titles(titles, args.artist, album_name, args.year)
    exit()

set_track_titles(titles, args.files, args.artist, album_name, args.year)

if args.rename:
    rename_files(titles, args.files)
