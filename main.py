import Judge_by_Surface_Morphology
import Draw
import Raster
import single_acc_threshold
import valid
from osgeo import gdal
import check
def OSM(OSMfile,outfile):

    OSM = Raster.get_raster(OSMfile)
    proj,geo,nodata = Raster.get_proj_geo_nodata(OSMfile)

    OSM[OSM == 0] = nodata
    OSM[OSM != nodata] = 1
    out = OSM.copy()
    row,col = OSM.shape
    from osgeo import gdal
    for i in range(row):
        for j in range(col):
            if OSM[i,j] == 1:
                out[i-3:i+3,j-3:j+3] = 2
    Raster.save_raster(outfile,out,proj,geo,gdal.GDT_Byte,nodata)

def reclass(infile,outfile):
    arr = Raster.get_raster(infile)
    proj,geo,nodata = Raster.get_proj_geo_nodata(infile)

    mask = (arr > 0.6)
    arr[mask] = 0.5

    mask = (0 < arr) & (arr <0.1)
    arr[mask] = 10

    mask = (0.1 < arr) & (arr < 0.2)
    arr[mask] = 20

    mask = (0.2 < arr) & (arr < 0.3)
    arr[mask] = 30

    mask = (0.3 < arr) & (arr < 0.4)
    arr[mask] = 40

    mask = (0.4 < arr) & (arr < 0.6)
    arr[mask] = 50

    Raster.save_raster(outfile,arr,proj,geo,gdal.GDT_Byte,0)

# reclass(r'E:\基于多源卫星数据的黑臭水体探测\Paper_Prepare\数据\图5\band2.tif',
#         r'E:\基于多源卫星数据的黑臭水体探测\Paper_Prepare\数据\图6\TP.tif')




# # 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
#     """
#     Judge_by_Surface_Morphology.sbatch_get_basin_embedding(
#         "/datanode05/zhangbin/hillslope_and_subbasin/DATA/NHD/ablq/Filleddem.tif",
#         "/datanode05/zhangbin/hillslope_and_subbasin/DATA/NHD/ablq/dir.tif",
#         "/datanode05/zhangbin/hillslope_and_subbasin/DATA/NHD/ablq/slink.tif",
#         "/datanode05/zhangbin/hillslope_and_subbasin/DATA/NHD/ablq/watershed.tif",
#         "/datanode05/zhangbin/hillslope_and_subbasin/DATA/NHD/ablq/venu")
#     Judge_by_Surface_Morphology.sbatch_get_basin_embedding(
#         "/datanode05/zhangbin/hillslope_and_subbasin/DATA/NHD/mssi/Filleddem.tif",
#         "/datanode05/zhangbin/hillslope_and_subbasin/DATA/NHD/mssi/dir.tif",
#         "/datanode05/zhangbin/hillslope_and_subbasin/DATA/NHD/mssi/slink.tif",
#         "/datanode05/zhangbin/hillslope_and_subbasin/DATA/NHD/mssi/watershed.tif",
#         "/datanode05/zhangbin/hillslope_and_subbasin/DATA/NHD/mssi/venu")
#     Judge_by_Surface_Morphology.sbatch_get_basin_embedding(
#         "/datanode05/zhangbin/hillslope_and_subbasin/DATA/NHD/dkss/Filleddem.tif",
#         "/datanode05/zhangbin/hillslope_and_subbasin/DATA/NHD/dkss/dir.tif",
#         "/datanode05/zhangbin/hillslope_and_subbasin/DATA/NHD/dkss/slink.tif",
#         "/datanode05/zhangbin/hillslope_and_subbasin/DATA/NHD/dkss/watershed.tif",
#         "/datanode05/zhangbin/hillslope_and_subbasin/DATA/NHD/dkss/venu")
#     Judge_by_Surface_Morphology.sbatch_get_basin_embedding(
#         "/datanode05/zhangbin/hillslope_and_subbasin/DATA/NHD/klld/Filleddem.tif",
#         "/datanode05/zhangbin/hillslope_and_subbasin/DATA/NHD/klld/dir.tif",
#         "/datanode05/zhangbin/hillslope_and_subbasin/DATA/NHD/klld/slink.tif",
#         "/datanode05/zhangbin/hillslope_and_subbasin/DATA/NHD/klld/watershed.tif",
#         "/datanode05/zhangbin/hillslope_and_subbasin/DATA/NHD/klld/venu")
#     """
#     # Draw.density("klld","/datanode05/zhangbin/hillslope_and_subbasin/DATA/NHD/klld")
#
#
    # single_acc_threshold.sbatch_extract_stream("/datanode05/zhangbin/hillslope_and_subbasin/DATA/NHD/ablq")
    # Judge_by_Surface_Morphology.sbatch_get_basin_embedding_combination("/datanode05/zhangbin/hillslope_and_subbasin/DATA/NHD/ablq")
    # valid.sbatch_erroer_matrix("/datanode05/zhangbin/hillslope_and_subbasin/DATA/NHD/ablq")
    # valid.sbatch_erroer_matrix1("/datanode05/zhangbin/hillslope_and_subbasin/DATA/NHD/ablq")
    # check.check_order_main("/datanode05/zhangbin/hillslope_and_subbasin/DATA/NHD/ablq")
    # check.check_order_main2("/datanode05/zhangbin/hillslope_and_subbasin/DATA/NHD/ablq")
    check.check_initial_NHD("/datanode05/zhangbin/hillslope_and_subbasin/DATA/NHD/ablq/visual_stream.tif","/datanode05/zhangbin/hillslope_and_subbasin/DATA/NHD/ablq/Stream3/450/slink.tif",
                      "/datanode05/zhangbin/hillslope_and_subbasin/DATA/NHD/ablq/stream_order.tif")

    # valid.error_matrix(r'F:\专利申请\一种考虑地表形态特征的子流域与坡面判别方法\DATA\研究区\NHD\阿巴拉契亚山脉\albq_stream_buffer.tif',
    #                    r'F:\专利申请\一种考虑地表形态特征的子流域与坡面判别方法\DATA\研究区\NHD\阿巴拉契亚山脉\venu\15\modified_link.tif')
    # valid.sbatch_erroer_matrix("/datanode05/zhangbin/hillslope_and_subbasin/DATA/NHD/mssi")
    # valid.sbatch_erroer_matrix("/datanode05/zhangbin/hillslope_and_subbasin/DATA/NHD/klld")
    # valid.sbatch_erroer_matrix("/datanode05/zhangbin/hillslope_and_subbasin/DATA/NHD/ablq")
    #
    # single_acc_threshold.sbatch_extract_stream("/datanode05/zhangbin/hillslope_and_subbasin/DATA/NHD/dkss")
    # Judge_by_Surface_Morphology.sbatch_get_basin_embedding_combination("/datanode05/zhangbin/hillslope_and_subbasin/DATA/NHD/dkss")
    # valid.sbatch_erroer_matrix("/datanode05/zhangbin/hillslope_and_subbasin/DATA/NHD/dkss")

    # single_acc_threshold.sbatch_extract_stream("/datanode05/zhangbin/hillslope_and_subbasin/DATA/NHD/mssi")
    # Judge_by_Surface_Morphology.sbatch_get_basin_embedding_combination("/datanode05/zhangbin/hillslope_and_subbasin/DATA/NHD/mssi")
    # valid.sbatch_erroer_matrix("/datanode05/zhangbin/hillslope_and_subbasin/DATA/NHD/mssi")

    # single_acc_threshold.sbatch_extract_stream("/datanode05/zhangbin/hillslope_and_subbasin/DATA/NHD/klld")
    # Judge_by_Surface_Morphology.sbatch_get_basin_embedding_combination("/datanode05/zhangbin/hillslope_and_subbasin/DATA/NHD/klld")
    # valid.sbatch_erroer_matrix("/datanode05/zhangbin/hillslope_and_subbasin/DATA/NHD/klld")

# # 访问 https://www.jetbrains.com/help/pycharm/ 获取 PyCharm 帮助
