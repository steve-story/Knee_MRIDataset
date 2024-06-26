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


path = r"C:\Users\Administrator\Desktop\train\2\20200113003910"  # kneedata is dataset's name
output_path = r'./dataset/train'
# path_2 = "./data/train/Data"


def get_pixeldata(dicom_path):
    dataset = pydicom.dcmread(dicom_path)
    # dataset = dcmread(os.path.join(DATA_PATH, dcm_file)
    plt.imshow(dataset.pixel_array, cmap=plt.cm.gray)
    plt.show()
    # print('Dataset tags:\n',dataset,dataset.pixel_array)

    # Extract Image Pixel Data
    image = dataset.pixel_array.astype(float)
    image = cv2.resize(image, (224, 224))

    # Scale normalization
    image = (image - image.mean()) / image.std()
    # print(image)

    return image


def dicom2png(dicom_path, savefile, width, height):
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    dcm = pydicom.dcmread(dicom_path)
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
    image = img_as_float(imageX)

    plt.cla()
    # plt.figure('adjust\_gamma', figsize=(width / 100, height / 100))
    # plt.subplots_adjust(top=1, bottom=0, left=0, right=1, hspace=0, wspace=0)
    plt.imshow(image, 'gray')
    plt.axis('off')
    plt.savefig(savefile)


if __name__ == '__main__':
    filenumber = os.listdir(path)
    for i in range(len(filenumber)):
        filepath = os.path.join(path, filenumber[i])
        filenames = os.listdir(filepath)
        for i in range(len(filenames)):
            dicom_path = os.path.join(filepath, filenames[i])
            png_name = os.path.splitext(filenames[i])[0]
            dst_path = os.path.join(output_path, (png_name + '.png'))、
            
            pixel_array = get_pixeldata(dicom_path)
            # dicom to png
            dicom2png(dicom_path, dst_path, 256, 256)
