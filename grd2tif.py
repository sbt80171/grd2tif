"""
xyzファイルをGeoTiffに変換

headerなしファイル対象
"""
import glob
import os.path

import geopandas as gpd
import pandas as pd
import rasterio
import rasterio.transform
import rasterio.features

# nodata
FILL = -9999


def get_shape(xmin, xmax, ymin, ymax, res):
    """
    入力：データ範囲と解像度
    出力：行列サイズ(ny, nx)
    """
    ny = int(((ymax-ymin)+res) / res)
    nx = int(((xmax-xmin)+res) / res)
    shape = (ny, nx)
    return shape


def get_trans(xmin, ymax, res):
    """
    入力：北西端のセルの中心座標と解像度
    出力：アフィン変換行列
    """
    west = xmin - res/2
    north = ymax + res/2
    trans = rasterio.transform.from_origin(
        west, north, res, res
    )
    return trans


def main(fill=FILL):
    print('グリッド型の xyz ファイルを GeoTiff に変換')
    print('')
    print('変換元データを保存したフォルダを指定')
    fold = input('>> ')
    print('拡張子を指定')
    ext = input('>> ')
    print('区切り文字を指定')
    sep = input('>> ')
    print('xyz の列番号をカンマ区切りで指定')
    xyz_str = input('>> ')
    idx_xyz = [int(c)-1 for c in xyz_str.strip().split(',')]
    print('グリッド間隔を m で指定')
    res = float(input('>> '))
    print('EPSG コードを指定')
    print('座標系を指定しない場合は Enter')
    crs_str = input('>> ')
    if crs_str:
        crs_identifier = f'EPSG:{crs_str}'
    else:
        crs_identifier = None

    fps_in = glob.glob(os.path.join(fold, '*.' + ext))
    for fp_in in fps_in:
        fn = os.path.splitext(os.path.basename(fp_in))[0]
        fp_out = os.path.join(fold, fn + '.tif')
        # 読込
        df = pd.read_csv(
            fp_in,
            sep=sep,
            names=['x', 'y', 'z'],
            usecols=idx_xyz
            )
        df['geometry'] = gpd.points_from_xy(df['x'], df['y'])
        gdf = gpd.GeoDataFrame(df)
        # 対象範囲をセルの中心座標で取得
        desc = gdf.describe()
        xmax = desc.loc['max', 'x']
        xmin = desc.loc['min', 'x']
        ymax = desc.loc['max', 'y']
        ymin = desc.loc['min', 'y']
        # 行列サイズ
        shape = get_shape(xmin, xmax, ymin, ymax, res)
        # アフィン変換行列
        trans = get_trans(xmin, ymax, res)
        # np.ndarrayに標高を格納
        arr = rasterio.features.rasterize(
            [(g, z) for g, z in zip(gdf['geometry'], gdf['z'])],
            out_shape=shape,
            fill=fill,
            transform=trans,  # type: ignore
            dtype='float32'
        )
        # 書込
        with rasterio.open(
            fp_out, 'w',
            driver='GTiff',
            height=arr.shape[0],
            width=arr.shape[1],
            count=1,
            dtype='float32',
            crs=crs_identifier,
            transform=trans,
            nodata=fill
        ) as f:
            f.write(arr, 1)

        print(fn)


if __name__ == '__main__':
    main()
