# -*- coding: utf-8 -*-
from PIL import Image, ImageEnhance, ImageFilter
import numpy as np
from scipy.misc import imread
import random, string
import os
import os.path



def cut_pic(filename):  # 图片处理（灰度化，二值化，切割图片）
    filepath = filename
    print count
    #print filename
    im = Image.open(filepath)
    # imgSize = im.size #
    # print imgSize   #(130, 50)
    imgry = im.convert('L')  # 灰度化

    # imgry.show()
    # 二值化
    threshold = 120
    table = []

    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
    biPic = imgry.point(table, '1')
    # biPic.show()


    bi_w = biPic.width
    bi_h = biPic.height

    data = biPic.getdata()
    data = np.matrix(data, dtype='int32')
    # new_data = np.reshape(data,(width,height))
    imarray = np.reshape(data, (bi_h, bi_w))

    reversedarray = 1 - imarray
    # print imarray.shape[1]   #列数
    # print reversedImg
    colSumList = np.asarray(reversedarray.sum(axis=0))[0]  # 每一列的元素和
    index_filter = [i for i in range(len(colSumList)) if colSumList[i] < 5]
    # blank_length = len(index_filter)
    # print "blank_length is " + str(blank_length)
    for col in index_filter:
        reversedarray[:, col:col + 1] = 0  # 作为分隔的空白列
    np.savetxt("aa.txt", reversedarray, fmt="%d")

    index_roi = [i for i in range(len(colSumList)) if i not in index_filter]  # 非空白列，可能是字符
    roi_cols_list = []
    tmp_list = []
    roi_height = 42
    roi_weight = 26
    for i in range(1, len(index_roi)):
        if (index_roi[i] - index_roi[i - 1] < 15):  # 连续的作为一个字符的列，最好是1，不过可能有噪声，所以定位4
            tmp_list.append(index_roi[i])
        else:
            # print "tmp_list is ", tmp_list
            while len(tmp_list) > roi_weight * 2:
                roi_cols_list.append(tmp_list[0:roi_weight])
                tmp_list = tmp_list[roi_weight:len(tmp_list)]

            roi_cols_list.append(tmp_list)
            tmp_list = []
    roi_cols_list.append(tmp_list)
    #     for i in roi_cols_list:
    #         print len(i)
    # print roi_cols_list

    child_img_list = []
    roi_rows_list = []
    badFlag = False
    for k in range(len(roi_cols_list)):
        # print "a"
        # print roi_cols_list[k]
        if roi_cols_list[k]:
            start_col = roi_cols_list[k][0]
            start_dict = {}
            for j in range(50 - roi_height):
                maxsum = reversedarray[j:j + roi_height, start_col:].sum()
                start_dict[maxsum] = j
            start_row = start_dict[max(start_dict.keys())]

            roi_rows_list.append(range(start_row, start_row + roi_height))
        else:
            badFlag = True

    #print "roi_cols_list", roi_cols_list
    #print "roi_rows_list", roi_rows_list
    if not badFlag:
        for i in range(len(roi_cols_list)):
            if roi_cols_list[i]:
                start_row = roi_rows_list[i][0]
                end_row = start_row + roi_height
        
                col_margin = (roi_weight - len(roi_cols_list[i])) / 2
                start_col = roi_cols_list[i][0] - col_margin
                end_col = start_col + roi_weight
                tmp_array = 255 * (1 - reversedarray[start_row:end_row, start_col:end_col])
                # print tmp_array.shape
                tmp_image = Image.fromarray(np.uint8(tmp_array))
                child_img_list.append(tmp_image)
                # tmp_image.show()
            else:
                child_img_list = []

    return child_img_list


def random_str(randomlength=8):
    a = list(string.ascii_letters + string.digits)
    random.shuffle(a)
    return ''.join(a[:randomlength])


if __name__ == '__main__':
    indir = r'D:/kerascode/geneImgs/'
    count = 0
    savename =""
    dirlist = os.listdir(indir)
    # print dirlist
    for i in range(0, len(dirlist)):
        surdir = os.path.join(indir, dirlist[i])
        # print surdir
        filelist = os.listdir(surdir)
        # print filelist
        for i in range(0, len(filelist)):
            filename = surdir + r"/" + filelist[i]
            # print filename
            if os.path.isfile(filename):
                child_img_list = cut_pic(filename)
                # print child_img_list
                cut_str = filename.split("_")[0].split(r"/")[-1]
                # print cut_str
                # print cut_str
                # 保存切割的图片
                # print "cut_str is "+ cut_str
                if (len(child_img_list) == len(cut_str)):
                    for i in range(0, len(child_img_list)):
                        dst_dir = cut_str[i].lower()
                        # print child_img_list[i].size    #(28, 28)
                        savename = "D:/kerascode/keras/testall/test_singlepress/%s/%s.jpg" % (cut_str[i], random_str(10))
                        # print "savename is " + savename
                        child_img_list[i].save(savename)
                        count = count+1
                        print count
                else:
                    pass
            

