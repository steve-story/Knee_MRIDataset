"""
# @file name : create_dataset
# @author : steve
# @date : 2024/6/26
# @brief : image processing
"""
import pydicom
import os
import matplotlib.pyplot as plt
from skimage import img_as_float
import cv2


path = r"C:\Users\Administrator\Desktop\train\5\3"
output_path = r'C:\Users\Administrator\Desktop\train\5\3png'
# path_2 = "./data/train/Data"

def get_pixeldata(dicom_path):
    dataset = pydicom.dcmread(dicom_path)
    # dataset = dcmread(os.path.join(DATA_PATH, dcm_file)
    plt.imshow(dataset.pixel_array, cmap=plt.cm.gray)
    plt.show()
    # print('Dataset tags:\n',dataset,dataset.pixel_array)

    # 提取图像像素数据
    image = dataset.pixel_array.astype(float)
    image = cv2.resize(image, (224, 224))
    # 归一化
    image = (image - image.mean()) / image.std()
    print(image)

    return image


def dicom2png(dicom_path, savefile, width, height):
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    dcm = pydicom.dcmread(dicom_path)
    print(dcm)
    # fileName = os.path.basename(file)
    imageX = dcm.pixel_array
    temp = imageX.copy()
    picMax = imageX.max()
    vmin = imageX.min()
    vmax = temp[temp < picMax].max()
    # print("vmin : ", vmin)
    # print("vmax : ", vmax)
    imageX[imageX > vmax] = 0
    imageX[imageX < vmin] = 0
    # result = exposure.is\_low\_contrast(imageX)
    # # print(result)
    image = img_as_float(imageX)
    plt.cla()
    plt.figure('adjust\_gamma', figsize=(width / 100, height / 100))
    plt.subplots_adjust(top=1, bottom=0, left=0, right=1, hspace=0, wspace=0)
    plt.imshow(image, 'gray')
    plt.axis('off')
    plt.savefig(savefile)


names = os.listdir(path)
print(names)
for i in range(len(names)):
    dicom_path = os.path.join(path, names[i])
    png_name = os.path.splitext(names[i])[0]
    dst_path = os.path.join(output_path, (png_name + '.png'))
    pixel_array = get_pixeldata(dicom_path)
    # dicom to png
    dicom2png(dicom_path, dst_path, 256, 256)
