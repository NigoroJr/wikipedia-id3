# wikipedia-id3(仮)

## これは何？
このスクリプトは[Wikipedia](http://ja.wikipedia.org)の記事からアルバムやシングルの収録曲を抽出し、ID3タグに書き込みます。

このスクリプトは記事内の`<ol>`タグを探すため、テーブルとして記述されたリスト([例](http://ja.wikipedia.org/wiki/Birth_%28%E5%96%9C%E5%A4%9A%E6%9D%91%E8%8B%B1%E6%A2%A8%E3%81%AE%E6%9B%B2%29))には使えません。

Pythonの勉強用に書いてみた程度のスクリプトなので、たぶん色々と間違っている部分があると思いますが、追い追い修正するかもしないかも。

## 使い方
`python3`を使います。

使用例:

    python3 main.py 'URL of album/single' /foo/bar/*.mp3

    python3 main.py --ol-count=2 --artist='somebody' 'URL of album/single' /foo/bar/*.flac

    python3 main.py --artist='foobar' --album-from-url --rename 'URL of album' *.mp3

    # When --album and --album-from-url are both given, --album is used
    python3 main.py --artist='somebody' --year=2012 \
        --album='awesome album' --album-from-url \
        'URL of album/single' /foo/bar/*.flac

デフォルトでは曲のタイトルのみが変更されます。オプションを指定することでアルバム名、アーティスト名、リリース年が変更できます。

`--ol-count`は、[こんな感じ](http://ja.wikipedia.org/wiki/Extra_terrestrial_Biological_Entities)に、要約？のところなどに`<ol>`タグが使用されてるときに使います。`--ol-count 2`にすると、2つ目の`<ol>`を収録曲のリストとして見ます。

URLがアルバム名の場合(ほとんどの場合そうでしょう)、`--album-from-url`でそのアルバム名を指定できます。

`--rename`オプションを使用することで、タイトルを使用してファイル名を変更できます。ファイル名が、

    foo.mp3 bar.mp3 baz.mp3

で、タイトルが

    Track_one Track2 TrackThree

だった場合、`--rename`によって

    01. Track_one.mp3 02.Track2.mp3 03.TrackThree.mp3

にそれぞれ名前が変更されます。

対応拡張子は、[TagLib](http://taglib.github.io/)が対応しているものです。サードパーティーライブラリは、
[`pytaglib`](https://github.com/supermihi/pytaglib),
[`urllib3`](https://github.com/shazow/urllib3)を使用します。

## Author
Naoki Mizuno (NigoroJr)
