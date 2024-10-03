# -*- coding: utf-8 -*-
"""
@Time ： 2024/6/13 15:15
@Auth ： Bin Zhang
@File ：Draw.py
@IDE ：PyCharm
"""
import math
import os

from osgeo import gdal,ogr
import matplotlib.pyplot as plt
import numpy as np
import json
import csv
import rasterio
import plotly.graph_objects as go
import Raster
from Judge_by_Surface_Morphology import *
from scipy import interpolate
import os

def color(r,g,b):
    return (r/255,g/255,b/255)

def Draw_scatter(subbemdding_json):

    with open(subbemdding_json, 'r', encoding='UTF-8') as f:
        result = json.load(f)
    data=[]
    dH=[]
    xy=[]
    for i in result:
        temp_xy=[i]
        for c in result[i]:
            temp_xy.append(result[i][c])
        xy.append(temp_xy)
        if -1<result[i]['subbemdding']<=1 :
            data.append(result[i]['subbemdding'])
            dH.append(result[i]['dH'])
    print(xy)
    with open(r'F:\专利申请\一种考虑地表形态特征的子流域与坡面判别方法\DATA\NWEI\沱沱河\1\基础数据\sub.csv',"a", encoding='utf-8', newline='') as f:
        writer=csv.writer(f)
        writer.writerows(xy)
    # x=[i for i in range(len(data))]
    # plt.scatter(x,data)
    # plt.show()

def draw_F1(csv_file):
    """
    绘制F1变化图
    :param csv_file:
    :return:
    """
    plt.rcParams['font.sans-serif'] = ['Times New Roman']

    embedding = []
    F1 = []
    Kappa = []
    accuracy = []
    precision = []
    recall = []
    n=0
    with open(csv_file,'r') as f:
        reader = csv.reader(f)
        for i in reader:
            if n>0:
                accuracy.append(float(i[1]))
                precision.append(float(i[3]))
                recall.append(float(i[4]))
                embedding.append(float(i[0]))
                Kappa.append(float(i[2]))
                F1.append(float(i[5]))
            n+=1

    plt.plot(embedding,F1)
    plt.plot([0.453,0.453],[0,1],linestyle='--')
    plt.plot([-0.4,0.6], [0.91,0.91], linestyle='--')
    plt.fill_between(embedding,F1,color='blue',alpha=0.1)
    # plt.fill_between(embedding, accuracy,  alpha=0.1)
    # plt.fill_between(embedding, precision,  alpha=0.1)
    # plt.fill_between(embedding, recall,  alpha=0.1)
    # plt.fill_between(embedding, Kappa,  alpha=0.1)
    # plt.text(0.15,0.2,'embedding=0.453',size=10)
    # plt.xlabel('embedding',size=12)
    # plt.ylabel('ratio',size=12)

    # 0.453
    # 0.829360659 Accuracy
    # 0.827316903 Kappa
    # 0.840362812 Precision
    # 0.983545648 Recall
    # 0.906334067 F1

    plt.show()

def draw_verification(csv_file):
    """
    绘制F1变化图
    :param csv_file:
    :return:
    """
    plt.rcParams['font.sans-serif'] = ['Times New Roman']

    embedding = []
    F1 = []
    Kappa = []
    accuracy = []
    precision = []
    recall = []
    n=0
    with open(csv_file,'r') as f:
        reader = csv.reader(f)
        for i in reader:
            if n>0:
                accuracy.append(float(i[1]))
                precision.append(float(i[3]))
                recall.append(float(i[4]))
                embedding.append(float(i[0]))
                Kappa.append(float(i[2]))
                F1.append(float(i[5]))
            n+=1


    plt.plot([0.453,0.453],[0,1.05],linestyle='--')
    # plt.plot([-0.4,0.6], [0.91,0.91], linestyle='--')


    plt.subplot(2,2,1)
    plt.plot(embedding, precision,color=color(154,201,219))
    plt.fill_between(embedding, precision,color=color(154,201,219),  alpha=0.4)
    plt.subplot(2,2, 2)
    plt.plot(embedding, recall,color=color(248,172,140))
    plt.fill_between(embedding, recall,color=color(248,172,140),  alpha=0.1)
    plt.subplot(2,2, 3)
    plt.plot(embedding, Kappa,color=color(200,36,35))
    plt.fill_between(embedding, Kappa,color=color(200,36,35),  alpha=0.1)
    plt.subplot(2,2, 4)
    plt.plot(embedding, accuracy, color=color(40, 120, 181))
    plt.fill_between(embedding, accuracy, color=color(40, 120, 181), alpha=0.1)
    # plt.text(0.15,0.2,'embedding=0.453',size=10)
    # plt.xlabel('embedding',size=12)
    # plt.ylabel('ratio',size=12)


    plt.show()

def draw_error():

    plt.errorbar()

def check_slope(slope_file):

    """
    绘制坡度直方图，看坡度分布模式
    :param slope:
    :return:
    """
    slope = Raster.get_raster(slope_file)
    proj,geo,nodata=Raster.get_proj_geo_nodata(slope_file)

    row,col = slope.shape

    slope_value = []
    for i in range(row):
        for j in range(col):
            if slope[i,j] != nodata:
                slope_value.append(slope[i,j]/math.pi*180)


    print("read successfully!")
    print("Average slope is {:.2}".format(sum(slope_value)/len(slope_value)))
    plt.hist(slope_value,bins=100)
    plt.show()


# 20240821
def draw_3D_surface(DEM_file):


    # Load DEM data
    dem_data = Raster.get_raster(DEM_file)
    dem_data = np.array(dem_data,np.float64)
    min_H = min(dem_data[dem_data>0])
    max_H = max(dem_data[dem_data > 0])
    dem_data[dem_data == max_H] = np.nan
    dem_data[dem_data<=min_H] = np.nan
    print(min(dem_data[dem_data>0]))
    # Create grid of coordinates
    x = np.arange(dem_data.shape[1])
    y = np.arange(dem_data.shape[0])
    x, y = np.meshgrid(x, y)
    z = dem_data


    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Plot the surface
    surf = ax.plot_surface(x,y,z,cmap = 'rainbow')
    # ax.contourf(x,y,z,  # 传入数据
    #             zdir='z'  # 设置为z轴为等高线的不变轴
    #             , offset=min_H  # 映射位置在z=-1处
    #             , cmap=plt.get_cmap('rainbow')  # 设置颜色为彩虹色
    #             )  # 绘制图像的映射，就是等高线图。

    # 设置边界的填充颜色和透明度
    surf.set_edgecolors('k')  # 设置边界颜色为黑色
    ax.set_facecolor('white')  # 设置图形背景颜色为白色/
    # 调整视角
    ax.view_init(elev=18, azim=140)
    ax.axis('off')



    plt.show()

def Draw_profile():
    #绘制最长流路的坡面
    # 构建研究区最长流路
    stream = Raster.get_raster(
        r'F:\专利申请\一种考虑地表形态特征的子流域与坡面判别方法\DATA\察隅验证\曲面\raster\delete\s1000link.tif')
    s_proj, s_geo, s_nodata = Raster.get_proj_geo_nodata(
        r'F:\专利申请\一种考虑地表形态特征的子流域与坡面判别方法\DATA\察隅验证\曲面\raster\delete\s1000link.tif')
    dem = Raster.get_raster(r'E:\察隅野外-202311\察隅采样\察隅流域\DEM\DEM.tif')
    dir = Raster.get_raster(r'F:\专利申请\一种考虑地表形态特征的子流域与坡面判别方法\DATA\察隅验证\run_data\Dir.tif')
    _, _, dir_nodata = Raster.get_proj_geo_nodata(
        r'F:\专利申请\一种考虑地表形态特征的子流域与坡面判别方法\DATA\察隅验证\run_data\Dir.tif')
    # A = Stream(stream, dem, dir, s_nodata, dir_nodata)
    # result = A.find_longest_path()
    # print(s_geo)
    id = [5591,3381,3127,5177]
    #   9414    6275  5668   8616
    c = [[(2935, 5423), (2935, 5422), (2935, 5421), (2935, 5420), (2935, 5419), (2935, 5418), (2935, 5417), (2936, 5416), (2937, 5415), (2938, 5415), (2939, 5414), (2940, 5413), (2940, 5412), (2941, 5411), (2941, 5410), (2941, 5409), (2940, 5408), (2940, 5407), (2940, 5406), (2939, 5405), (2939, 5404), (2940, 5403), (2940, 5402), (2941, 5402), (2942, 5402), (2943, 5402), (2944, 5402), (2945, 5402), (2946, 5402), (2947, 5402), (2948, 5403), (2949, 5404), (2950, 5405), (2951, 5406), (2952, 5407), (2953, 5408), (2954, 5409), (2955, 5410), (2956, 5411), (2957, 5412), (2958, 5412), (2959, 5413), (2960, 5414), (2961, 5414), (2962, 5415), (2963, 5416), (2964, 5416), (2965, 5416), (2966, 5416), (2967, 5416), (2968, 5416), (2969, 5416), (2970, 5415), (2971, 5414), (2971, 5413), (2972, 5412), (2973, 5411), (2974, 5411), (2975, 5412), (2976, 5412), (2977, 5412), (2978, 5412), (2979, 5412), (2980, 5412), (2981, 5411), (2982, 5410), (2983, 5410), (2984, 5409), (2985, 5409), (2986, 5408), (2987, 5407), (2988, 5407), (2989, 5407), (2990, 5407), (2991, 5407), (2992, 5407), (2993, 5406), (2994, 5406), (2995, 5406), (2996, 5406), (2997, 5406), (2998, 5406), (2999, 5406), (3000, 5405), (3001, 5405), (3002, 5404), (3003, 5404), (3004, 5403), (3005, 5403), (3006, 5403), (3007, 5402), (3008, 5401), (3009, 5401), (3010, 5401), (3011, 5401)],
    [(1849, 3580), (1848, 3581), (1848, 3582), (1848, 3583), (1849, 3584), (1849, 3585), (1849, 3586), (1850, 3587), (1850, 3588), (1851, 3588), (1852, 3589), (1853, 3589), (1854, 3590), (1855, 3590), (1856, 3590), (1857, 3590), (1858, 3590), (1859, 3590), (1860, 3591), (1861, 3591), (1862, 3591), (1863, 3591), (1864, 3591), (1865, 3591), (1866, 3590), (1867, 3590), (1868, 3590), (1869, 3591), (1870, 3591), (1871, 3591), (1872, 3591), (1873, 3591), (1874, 3591), (1875, 3591), (1876, 3591), (1877, 3591), (1878, 3591), (1879, 3590), (1880, 3589), (1881, 3588), (1881, 3587), (1881, 3586), (1882, 3585), (1883, 3584), (1884, 3583), (1885, 3583), (1886, 3582), (1887, 3581), (1888, 3581), (1889, 3580), (1890, 3579), (1891, 3578), (1892, 3578), (1893, 3578), (1894, 3577), (1895, 3577), (1896, 3577), (1897, 3577), (1898, 3576), (1899, 3575), (1900, 3574), (1901, 3573), (1902, 3573), (1903, 3573), (1904, 3573), (1905, 3573), (1906, 3573), (1907, 3573), (1908, 3572), (1909, 3572), (1910, 3572), (1911, 3572), (1912, 3572), (1913, 3572), (1914, 3572), (1915, 3572), (1916, 3572), (1917, 3572), (1918, 3572), (1919, 3572), (1920, 3573), (1921, 3573), (1922, 3572), (1923, 3572), (1924, 3572), (1925, 3572), (1926, 3572), (1927, 3572), (1928, 3572), (1929, 3571), (1930, 3570), (1931, 3569), (1931, 3568), (1932, 3567), (1932, 3566), (1933, 3565), (1934, 3564), (1935, 3564), (1936, 3563), (1937, 3562), (1937, 3561), (1937, 3560), (1937, 3559), (1937, 3558), (1937, 3557), (1937, 3556), (1937, 3555), (1938, 3554), (1939, 3553), (1940, 3552), (1940, 3551), (1941, 3550), (1942, 3549), (1942, 3548), (1943, 3547), (1944, 3546), (1945, 3545), (1946, 3544), (1947, 3543), (1948, 3542), (1949, 3541), (1950, 3540), (1950, 3539), (1950, 3538), (1951, 3537), (1951, 3536), (1951, 3535), (1951, 3534), (1951, 3533), (1951, 3532), (1951, 3531), (1951, 3530), (1951, 3529), (1951, 3528), (1951, 3527), (1952, 3526), (1952, 3525), (1952, 3524), (1952, 3523), (1952, 3522), (1952, 3521), (1952, 3520), (1953, 3519), (1953, 3518), (1953, 3517), (1953, 3516), (1953, 3515), (1953, 3514), (1954, 3513), (1955, 3512), (1955, 3511), (1955, 3510), (1955, 3509), (1954, 3508), (1955, 3507), (1955, 3506), (1955, 3505), (1955, 3504), (1955, 3503), (1955, 3502)],
    [(1769, 2281), (1770, 2280), (1771, 2279), (1772, 2278), (1773, 2277), (1773, 2276), (1772, 2275), (1771, 2274), (1771, 2273), (1771, 2272), (1771, 2271), (1771, 2270), (1771, 2269), (1772, 2268), (1772, 2267), (1772, 2266), (1772, 2265), (1772, 2264), (1772, 2263), (1772, 2262), (1771, 2261), (1771, 2260), (1771, 2259), (1771, 2258), (1771, 2257), (1771, 2256), (1771, 2255), (1771, 2254), (1771, 2253), (1771, 2252), (1771, 2251), (1771, 2250), (1771, 2249), (1771, 2248), (1771, 2247), (1771, 2246), (1772, 2245), (1773, 2244), (1774, 2243), (1774, 2242), (1774, 2241), (1774, 2240), (1774, 2239), (1774, 2238), (1774, 2237), (1775, 2236), (1776, 2235), (1776, 2234), (1776, 2233), (1776, 2232), (1777, 2231), (1777, 2230), (1777, 2229), (1777, 2228), (1778, 2227), (1779, 2226), (1779, 2225), (1780, 2224), (1781, 2223), (1782, 2222), (1783, 2221), (1784, 2220), (1785, 2219), (1786, 2218), (1787, 2217), (1788, 2216), (1789, 2215), (1790, 2215), (1791, 2214), (1792, 2213), (1792, 2212), (1792, 2211), (1792, 2210), (1792, 2209), (1792, 2208), (1792, 2207), (1792, 2206), (1792, 2205), (1792, 2204), (1793, 2203), (1793, 2202), (1793, 2201), (1794, 2200), (1794, 2199), (1794, 2198), (1794, 2197), (1794, 2196), (1794, 2195), (1793, 2194), (1793, 2193), (1792, 2192), (1791, 2191), (1791, 2190), (1790, 2189), (1790, 2188), (1790, 2187), (1790, 2186), (1790, 2185), (1790, 2184), (1790, 2183), (1790, 2182), (1790, 2181), (1790, 2180), (1790, 2179), (1790, 2178), (1790, 2177), (1790, 2176), (1790, 2175), (1790, 2174), (1790, 2173), (1790, 2172), (1790, 2171), (1790, 2170), (1790, 2169), (1790, 2168), (1789, 2167), (1789, 2166), (1788, 2165), (1788, 2164), (1788, 2163), (1788, 2162), (1788, 2161), (1788, 2160), (1789, 2159), (1789, 2158), (1789, 2157), (1789, 2156), (1790, 2155), (1791, 2154), (1791, 2153), (1792, 2152), (1793, 2151), (1793, 2150), (1794, 2149), (1795, 2148), (1795, 2147), (1796, 2146), (1795, 2145), (1795, 2144), (1795, 2143), (1795, 2142), (1796, 2141), (1797, 2140), (1797, 2139), (1797, 2138), (1797, 2137), (1797, 2136), (1797, 2135), (1797, 2134), (1797, 2133), (1797, 2132), (1798, 2131), (1798, 2130), (1798, 2129), (1798, 2128), (1798, 2127), (1798, 2126), (1798, 2125), (1798, 2124), (1798, 2123), (1798, 2122), (1798, 2121), (1798, 2120), (1798, 2119), (1798, 2118), (1798, 2117), (1798, 2116), (1798, 2115), (1799, 2114), (1799, 2113), (1799, 2112), (1799, 2111), (1799, 2110), (1799, 2109), (1799, 2108), (1799, 2107), (1799, 2106), (1799, 2105), (1799, 2104), (1798, 2103), (1798, 2102)],
    [(2727, 2832), (2726, 2832), (2726, 2831), (2726, 2830), (2726, 2829), (2726, 2828), (2727, 2827), (2728, 2826), (2728, 2825), (2728, 2824), (2727, 2823), (2727, 2822), (2727, 2821), (2727, 2820), (2728, 2819), (2728, 2818), (2728, 2817), (2728, 2816), (2728, 2815), (2728, 2814), (2728, 2813), (2728, 2812), (2727, 2811), (2727, 2810), (2727, 2809), (2727, 2808), (2728, 2807), (2728, 2806), (2729, 2805), (2730, 2804), (2731, 2803), (2731, 2802), (2731, 2801), (2732, 2800), (2732, 2799), (2733, 2798), (2733, 2797), (2733, 2796), (2734, 2795), (2734, 2794), (2734, 2793), (2734, 2792), (2734, 2791), (2734, 2790), (2734, 2789), (2734, 2788), (2735, 2787), (2735, 2786), (2735, 2785), (2735, 2784), (2735, 2783), (2736, 2782), (2736, 2781), (2737, 2780), (2737, 2779), (2737, 2778), (2738, 2777), (2738, 2776), (2738, 2775), (2738, 2774), (2737, 2773), (2737, 2772), (2738, 2771), (2738, 2770), (2738, 2769), (2738, 2768), (2738, 2767), (2739, 2766), (2739, 2765), (2740, 2764), (2741, 2763), (2742, 2762), (2742, 2761), (2742, 2760), (2742, 2759), (2742, 2758)]]
    for sid in range(len(c)):
        # cells = result[sid]
        cells = c[sid]
        print(cells)
        x = [0]
        for k in range(1,len(cells)):
            if abs(cells[k][0]-cells[k-1][0])==0 or abs(cells[k][1]-cells[k-1][1])==0:
                x.append(x[k - 1] + 30 * math.sqrt(2))
            else:
                x.append(x[k - 1] + 30 )


        y = [dem[i[0],i[1]] for i in cells]
        plt.plot(x,y,color='black')
        # plt.axis('equal')    # X Y轴等距
        plt.xlim(min(x)-100, max(x)+100)
        plt.ylim(min(y)-100, max(y)+100)

        # plt.xticks([])
        plt.show()

    # for sid in id:
    #     cells = result[sid]
    #
    #     print(cells)
    #     y = [dem[i[0],i[1]] for i in cells]
    #     plt.plot(y)
    #     plt.show()

def Draw_profile_hillslope():
    # 批量绘制最长流路的坡面
    # 构建研究区最长流路

    # 读取incision数据
    incision_file = r'F:\专利申请\一种考虑地表形态特征的子流域与坡面判别方法\DATA\察隅验证\Acc2000\Result\incision.csv'
    with open(incision_file,'r') as f:
        con = csv.reader(f)

        id_incision = []
        n = 0
        for i in con:
            if n>0:
                id_incision.append((int(i[0]),float(i[1])))
            n+=1
    hillslope_ids = []
    source_watershed_ids = []
    for i in id_incision:
        if i[1]<=0.35:
            hillslope_ids.append(i[0])
        else:
            source_watershed_ids.append(i[0])
    print(len(hillslope_ids))

    stream = Raster.get_raster(
        r'F:\专利申请\一种考虑地表形态特征的子流域与坡面判别方法\DATA\察隅验证\Acc2000\Stream_link.tif')
    s_proj, s_geo, s_nodata = Raster.get_proj_geo_nodata(
        r'F:\专利申请\一种考虑地表形态特征的子流域与坡面判别方法\DATA\察隅验证\Acc2000\Stream_link.tif')
    dem = Raster.get_raster(r'F:\专利申请\一种考虑地表形态特征的子流域与坡面判别方法\DATA\察隅验证\run_data\DEM.tif')
    dir = Raster.get_raster(r'F:\专利申请\一种考虑地表形态特征的子流域与坡面判别方法\DATA\察隅验证\run_data\Dir.tif')
    _, _, dir_nodata = Raster.get_proj_geo_nodata(
        r'F:\专利申请\一种考虑地表形态特征的子流域与坡面判别方法\DATA\察隅验证\run_data\Dir.tif')
    A = Stream(stream, dem, dir, s_nodata, dir_nodata,r'F:\专利申请\一种考虑地表形态特征的子流域与坡面判别方法\DATA\察隅验证\Acc2000\Result')
    result = A.find_longest_path()
    # print(s_geo)

    for sid in hillslope_ids:
        if sid in result:
            cells = result[sid]
            # print(cells)
            x = [0]
            for k in range(1, len(cells)):
                if abs(cells[k][0] - cells[k - 1][0]) == 0 or abs(cells[k][1] - cells[k - 1][1]) == 0:
                    x.append(x[k - 1] + 30 * math.sqrt(2))
                else:
                    x.append(x[k - 1] + 30)

            y = [dem[i[0], i[1]] for i in cells]
            plt.plot(x, y, color='black')
            # plt.axis('equal')
            plt.xlim(min(x) - 100, max(x) + 100)
            plt.ylim(min(y) - 100, max(y) + 100)

            # plt.xticks([])
            plt.savefig(os.path.join(r'F:\专利申请\一种考虑地表形态特征的子流域与坡面判别方法\DATA\察隅验证\Acc2000\Result\Hillslope',str(sid)+'.jpg'))
            plt.close()
    # plt.show()

    for sid in source_watershed_ids:
        if sid in result:
            cells = result[sid]

            x = [0]
            for k in range(1, len(cells)):
                if abs(cells[k][0] - cells[k - 1][0]) == 0 or abs(cells[k][1] - cells[k - 1][1]) == 0:
                    x.append(x[k - 1] + 30 * math.sqrt(2))
                else:
                    x.append(x[k - 1] + 30)

            y = [dem[i[0], i[1]] for i in cells]
            plt.plot(x, y, color='black')
            # plt.axis('equal')
            plt.xlim(min(x)-100, max(x)+100)
            plt.ylim(min(y)-100, max(y)+100)
            plt.savefig(
                os.path.join(r'F:\专利申请\一种考虑地表形态特征的子流域与坡面判别方法\DATA\察隅验证\Acc2000\Result\Watershed',
                             str(sid) + '.jpg'))
            plt.close()
            # plt.xticks([])
    # plt.show()

    # ids = [4202]
    # for sid in ids:
    #     if sid in result:
    #         cells = result[sid]
    #
    #         x = [0]
    #         for k in range(1, len(cells)):
    #             if abs(cells[k][0] - cells[k - 1][0]) == 0 or abs(cells[k][1] - cells[k - 1][1]) == 0:
    #                 x.append(x[k - 1] + 30 * math.sqrt(2))
    #             else:
    #                 x.append(x[k - 1] + 30)
    #
    #         y = [dem[i[0], i[1]] for i in cells]
    #         plt.plot(x, y, color='black')
    #         plt.axis('equal')
    #         # plt.xlim(min(x), max(x))
    #         # plt.ylim(min(y), max(y))
    #
    #         # plt.xticks([])
    # plt.show()

def density(watershed_file,stream_link_file,DEM_file,incision_file,Name,venu):
    # 计算河网密度

    watershed = Raster.get_raster(watershed_file)
    proj,geo,w_nodata = Raster.get_proj_geo_nodata(watershed_file)

    # stream = Raster.get_raster(stream_link_file)
    # proj,geo,s_nodata = Raster.get_proj_geo_nodata(stream_link_file)

    DEM = Raster.get_raster(DEM_file)
    print(geo)
    row,col = watershed.shape

    stream_area_dic = {}
    watershed_area = 0

    for i in range(row):
        for j in range(col):
            # if stream[i,j] != s_nodata:
            #     stream_area_dic.setdefault(stream[i,j],[]).append((i,j,DEM[i,j]))
            if watershed[i,j] != w_nodata:
                watershed_area += geo[1]*geo[1]/1000000



    x = [0,0.07,0.14,0.21,0.25,0.35]
    y = []
    x1 = []
    y1 = []
    for k in range(1,7):
        stream_area_dic = {}
        stream_file = os.path.join(venu,'Result1'+str(k),'modified_link.tif')
        Stream = Raster.get_raster(stream_file)
        proj, geo, s_nodata = Raster.get_proj_geo_nodata(stream_file)

        row,col = Stream.shape
        for i in range(row):
            for j in range(col):
                if Stream[i,j] != s_nodata:
                    stream_area_dic.setdefault(Stream[i,j],[]).append((i,j,DEM[i,j]))

        stream_len = 0
        for s_id in stream_area_dic:
            cells = stream_area_dic[s_id].copy()
            cells.sort(key=lambda x: x[2])
            temp_len = 0
            if len(cells) == 1:
                temp_len += geo[1] / 1000
            else:
                for i in range(len(cells) - 1):
                    start_cell = cells[i]
                    end_cell = cells[i + 1]
                    if (start_cell[0] - end_cell[0] == 0) or (start_cell[1] - end_cell[1] == 0):
                        temp_len += geo[1] * math.sqrt(2) / 1000
                    else:
                        temp_len += geo[1] / 1000
            stream_len += temp_len
        y.append(stream_len / watershed_area)
        y1.append(len(stream_area_dic))

    #
    #
    # # print(watershed_area)
    # # print(stream_len)
    # # print(stream_len/watershed_area)
    #
    # with open(incision_file,'r') as f:
    #     reader = csv.reader(f)
    #     n = 0
    #     con =[]
    #     for i in reader:
    #         if n>0:
    #             con.append((float(i[0]),float(i[1])))
    #         n += 1
    # # 计算不同阈值下的河网密度
    # x = []
    # y = []
    # x1 = []
    # y1 = []
    # incison_list = []
    # for incision_threshold in range(-20,80,5):
    #     x.append(incision_threshold/100)
    #     stream_len1 = stream_len
    #     hillslope_num = 0
    #     temp_incision = []
    #     for cell in con:
    #         if cell[1]<incision_threshold/100:
    #             stream_len1 -= stream_length_dic[cell[0]]
    #             hillslope_num += 1
    #             temp_incision.append(cell[1])
    #     y.append(stream_len1/watershed_area)
    #     x1.append(hillslope_num)
    #     y1.append(65-hillslope_num)
    #     incison_list.append(temp_incision)

    # 绘制河网密度图
    venu = r'F:\专利申请\一种考虑地表形态特征的子流域与坡面判别方法\论文\图\草图\Figure7'
    density_save_path = os.path.join(venu,Name+'_density.svg')
    f = interpolate.interp1d(x,y, kind='quadratic')
    xNew = np.linspace(min(x), max(x), 1000)
    yNew = f(xNew)
    plt.figure(figsize=(5, 4))
    plt.plot(x,y,zorder=1)
    plt.scatter(x, y)
    plt.savefig(density_save_path)
    # plt.show()
    plt.close()

    # 绘制hillslope和watershed的数量
    number_save_path = os.path.join(venu,Name+'_number.svg')
    plt.figure(figsize=(5, 4))
    # plt.scatter(x, x1,color=color(250,127,111))
    # plt.plot(x,x1,color=color(250,127,111))

    plt.scatter(x,y1,color=color(130,176,210))
    plt.plot(x, y1, color=color(130,176,210))
    plt.savefig(number_save_path)
    # plt.show()
    plt.close()

    # # 绘制误差棒
    # errorbar_save_path = os.path.join(venu,Name+'_error.svg')
    # plt.figure(figsize=(5,4))
    # plt.boxplot(incison_list,labels=x,sym='.')
    # plt.xticks(rotation=70,ha='right')
    # # plt.show()
    # plt.savefig(errorbar_save_path)

if __name__=='__main__':

    # file=r'F:\专利申请\一种考虑地表形态特征的子流域与坡面判别方法\DATA\NWEI\沱沱河\基础数据\subbemdding2.json'
    # Draw_scatter(file)

    # 精度绘制
    # verification_file=r'F:\专利申请\一种考虑地表形态特征的子流域与坡面判别方法\DATA\察隅验证\Acc300\valid.csv'
    # # draw_F1(verification_file)
    # # draw_verification(verification_file)
    # slope_file = r'F:\专利申请\一种考虑地表形态特征的子流域与坡面判别方法\DATA\察隅验证\地形因子\slope1.tif'
    # check_slope(slope_file)


    # 绘制3D surface
    # draw_3D_surface(r'F:\专利申请\一种考虑地表形态特征的子流域与坡面判别方法\DATA\察隅验证\曲面\raster\delete\valid_dem\3025.tif')

    # 绘制最长流路的剖面
    # Draw_profile()

    # 绘制三维地形
    draw_3D_surface(r'F:\专利申请\一种考虑地表形态特征的子流域与坡面判别方法\论文\图\草图\valid\3472.tif')

    # 批量绘制剖面高程图
    # Draw_profile_hillslope()

    # # 计算河网密度、hillslope数量、errorbar
    # density(r'F:\专利申请\一种考虑地表形态特征的子流域与坡面判别方法\DATA\研究区\喀斯特\data\watershed.tif',
    #         r'F:\专利申请\一种考虑地表形态特征的子流域与坡面判别方法\DATA\研究区\喀斯特\data\streamlink.tif',
    #         r'F:\专利申请\一种考虑地表形态特征的子流域与坡面判别方法\DATA\研究区\喀斯特\data\DEM.tif',
    #         r'F:\专利申请\一种考虑地表形态特征的子流域与坡面判别方法\DATA\研究区\喀斯特\data\Result\incision.csv','Kasite')

    # density(r'F:\专利申请\一种考虑地表形态特征的子流域与坡面判别方法\DATA\研究区\高山区\data\watershed.tif',
    #         r'F:\专利申请\一种考虑地表形态特征的子流域与坡面判别方法\DATA\研究区\高山区\data\streamlink.tif',
    #         r'F:\专利申请\一种考虑地表形态特征的子流域与坡面判别方法\DATA\研究区\高山区\data\DEM.tif',
    #         r'F:\专利申请\一种考虑地表形态特征的子流域与坡面判别方法\DATA\研究区\高山区\data\Result\incision.csv',
    #         'Gaoshan',r'F:\专利申请\一种考虑地表形态特征的子流域与坡面判别方法\DATA\研究区\高山区\data')

    # density(r'F:\专利申请\一种考虑地表形态特征的子流域与坡面判别方法\DATA\研究区\水库\data\watershed.tif',
    #         r'F:\专利申请\一种考虑地表形态特征的子流域与坡面判别方法\DATA\研究区\水库\data\streamlink.tif',
    #         r'F:\专利申请\一种考虑地表形态特征的子流域与坡面判别方法\DATA\研究区\水库\data\DEM.tif',
    #         r'F:\专利申请\一种考虑地表形态特征的子流域与坡面判别方法\DATA\研究区\水库\data\Result\incision.csv',
    #         'servior')
    #
    # density(r'F:\专利申请\一种考虑地表形态特征的子流域与坡面判别方法\DATA\研究区\武镇\data\watershed.tif',
    #         r'F:\专利申请\一种考虑地表形态特征的子流域与坡面判别方法\DATA\研究区\武镇\data\streamlink.tif',
    #         r'F:\专利申请\一种考虑地表形态特征的子流域与坡面判别方法\DATA\研究区\武镇\data\Wuzhen_DEM.tif',
    #         r'F:\专利申请\一种考虑地表形态特征的子流域与坡面判别方法\DATA\研究区\武镇\data\Result\incision.csv',
    #         'Wuzhen')

    # !/usr/bin/python3
    # code-python(3.6)


    pass