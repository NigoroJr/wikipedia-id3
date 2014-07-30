# wikipedia-id3(仮)

## これは何？
このスクリプトは[Wikipedia](http://ja.wikipedia.org)の記事からアルバムやシングルの収録曲を抽出し、ID3タグに書き込みます。

このスクリプトは記事内の`<ol>`タグを探すため、テーブルとして記述されたリスト([例](http://ja.wikipedia.org/wiki/Birth_%28%E5%96%9C%E5%A4%9A%E6%9D%91%E8%8B%B1%E6%A2%A8%E3%81%AE%E6%9B%B2%29))には使えません。

Pythonの勉強用に書いてみた程度のスクリプトなので、たぶん色々と間違っている部分があると思いますが、追い追い修正するかもしないかも。

## 使い方
`python3`を使います。

使用例:

    python3 main.py 'URL of album/single' /foo/bar/*.mp3

    python3 main.py --ol-count 2 --artist='somebody' 'URL of album/single' /foo/bar/*.flac

`--ol-count`は、[こんな感じ](http://ja.wikipedia.org/wiki/Extra_terrestrial_Biological_Entities)に、要約？のところなどに`<ol>`タグが使用されてるときに使います。`--ol-count 2`にすると、2つ目の`<ol>`を収録曲のリストとして見ます。

`--artist`を指定すると、アルバムのアーティストを各曲に書き込みます。

対応拡張子は、[TagLib](http://taglib.github.io/)が対応しているものです。[`pytaglib`](https://github.com/supermihi/pytaglib),
[`urllib3`](https://github.com/shazow/urllib3)を使用します。

## Author
Naoki Mizuno (NigoroJr)
