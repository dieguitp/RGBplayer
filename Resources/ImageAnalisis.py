from matplotlib import pyplot as plt
from skimage import data, feature
from skimage.feature import blob_doh
from skimage.color import rgb2gray
from math import sqrt
from PIL import Image
import os

if not os.path.isfile("Im.png"):
    path = '/Users/Diego/Desktop/Projet lutherie 1/colorcircle.jpg'
    im = Image.open(path)

    #Image size
    size = im.size
    print size

    #image to gray for analysis
    image = data.load(path)[0:size[0],0:size[1]]
    image_gray = rgb2gray(image)

    blobs_doh = blob_doh(image_gray, max_sigma=30, threshold=.006)

    #Blob data (x,y,sigma)
    datblobx = []
    datbloby = []
    datblobrad = []
    datblob = data.coins()
    feature.blob_doh(datblob)
    datblobx.append(datblob[0])
    datbloby.append(datblob[1])
    datblobrad.append(datblob[2])
    coeff = size[0]*0.0015625
    if coeff < 1:
        coeff = 640./size[0]
    print coeff
        

    blobs_list = [blobs_doh]
    colors = ['yellow']
    titles = ['Image Player']
    sequence = zip(blobs_list, colors, titles)

    for blobs, color, title in sequence:
        fig, ax = plt.subplots(1, 1, figsize=(8,8))
        ax.imshow(image, interpolation='nearest')
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        for blob in blobs:
            y, x, r = blob
            c = plt.Circle((x, y), r, color=color, linewidth=2, fill=False) 
            ax.add_patch(c)
        plt.savefig('Im.png',transparent=True, bbox_inches='tight',pad_inches=0)

#Imimage size
Im = Image.open('Im.png')
imsize = Im.size