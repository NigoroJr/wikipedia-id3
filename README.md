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

    python3 main.py --ol-count=2 --artist='somebody' 'URL of album/single' /foo/bar/*.flac

    python3 main.py --artist='foobar' --album-from-url --rename 'URL of album' *.mp3

    # --album と --album-from-url の両方がオンの場合、 --album が使われます。
    python3 main.py --artist='somebody' --year=2012 \
        --album='awesome album' --album-from-url \
        'URL of album/single' /foo/bar/*.flac

Only the track titles are changed by default. You can change the artist, album
name, and release year by enabling the options.

Although in most cases the track listing is in the first `<ol>` tag,
sometimes this is not the case. `--ol-count` lets you specify which
`<ol>` tag to look at.

`--album-from-url` lets you set the album name from the URL if the URL
accurately reflects the album name, which is the case most of the time.

`--rename` will rename the files with the appropriate titles as their file
name. 2-digit number is added to each file. For example, if the files were:

    foo.mp3 bar.mp3 baz.mp3

and the titles were:

    Track_one Track2 TrackThree

then the renamed files will be:

    01. Track_one.mp3 02.Track2.mp3 03.TrackThree.mp3

You can tag extensions that are supported by [TagLib](http://taglib.github.io/).

## Author
Naoki Mizuno (NigoroJr)
