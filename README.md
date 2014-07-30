# wikipedia-id3 (Subject to change)

## What
This is a program that extracts the titles of tracks from
[Wikipedia](http://en.wikipedia.org) and writes to the ID3 tag of music files.

This program looks for `<ol>` tags so it probably won't work for most of the
English albums on Wikipedia.

*I wrote this script in order to get familiar with the Python language so I'm
pretty sure I'm doing some idiotic stuff even in this short script.*

## How
This script uses `python3`.

Examples:

    python3 main.py 'URL of album/single' /foo/bar/*.mp3

    python3 main.py --ol-count 2 --artist='somebody' 'URL of album/single' /foo/bar/*.flac

Although in most cases the track listing is in the first `<ol>` tag,
sometimes this is not the case. `--ol-count` lets you specify which
`<ol>` tag to look at.

`--artist` also sets the artist name of the album/single.

## Author
Naoki Mizuno (NigoroJr)
