# grd2tif

グリッド型の xyz ファイルを GeoTiff に変換します。

# 入力データについて

航空レーザ測量（LP測量）等の成果品であるグリッドデータを使用します。

拡張子、区切り文字、並び順、グリッド間隔、座標系は、コンソールから入力します。

# 出力データについて

入力ファイル別にGeoTiffファイルが出力されます。

欠損セルは NoData になります。

# 入力例

```
変換元データを保存したフォルダを指定
>> c:\test
拡張子を指定
>> txt
区切り文字を指定
>> ,
xyz の列番号をカンマ区切りで指定
>> 1,2,3
グリッド間隔を m で指定
>> 5
EPSG コードを指定
座標系を指定しない場合は Enter
>> 1111
```

# ライブラリ

python  3.9.5  
geopandas  0.10.2  
pandas  1.3.1  
rasterio  1.2.10  

# License

Copyright (c) 2022 sbt80171

Released under the [MIT license](https://opensource.org/licenses/mit-license.php).
