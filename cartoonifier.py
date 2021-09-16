import cv2

# EasyGUI is a module for very simple, very easy GUI programming in Python. EasyGUI is different from other GUI generators in that EasyGUI 
# is NOT event-driven. Instead, all GUI interactions are invoked by simple function calls.
# EasyGui provides an easy-to-use interface for simple GUI interaction with a user. It does not require the programmer to know anything about tkinter,
#  frames, widgets, callbacks or lambda.
import easygui
import numpy as np

# Imageio is a Python library that provides an easy interface to read and write a wide range of image data, including animated images, 
# volumetric data, and scientific formats. It is cross-platform, runs on Python 3.5+, and is easy to install.
import imageio
from matplotlib import pyplot as plt
import os
import sys
import tkinter as tk
from tkinter.messagebox import showerror
from PIL import ImageTk, Image


def upload():
    path = easygui.fileopenbox(title='Please Select an Image:')
    if path:
        imagePath.set(path)
        oImage.image = ImageTk.PhotoImage(Image.open(imagePath.get()).resize((400, 400)))
        oImage.configure(image=oImage.image)
        if cImage.image:
            cImage.image = None


"""NOTE:
When the image file is read with the **OpenCV** function imread(), the order of colors is **BGR** (blue, green, red). 

On the other hand, in **Pillow**, the order of colors is assumed to be **RGB** (red, green, blue).

Therefore, if you want to use both the Pillow function and the OpenCV function, you need to convert BGR and RGB.

    cv2.cvtColor(src, code[, dst[, dstCn]])

**Parameters**:
- src: It is the image whose color space is to be changed.
- code: It is the color space conversion code.
- dst: It is the output image of the same size and depth as src image. It is an optional parameter.
- dstCn: It is the number of channels in the destination image. If the parameter is 0 then the number of the channels is derived automatically from  src and code. It is an optional parameter.

**Return Value**: 
It returns an image.
"""


def cartoonify(ImagePath):
    originalImage = cv2.imread(ImagePath)

    global figures
    figures = {}
    
    RGBImage = cv2.cvtColor(originalImage, cv2.COLOR_BGR2RGB)
    # NOTE: We resize the image after each transformation to display all the images on a similar scale at last.
    reSized1 = cv2.resize(RGBImage, (1536, 1024))
    figures['Colored'] = reSized1

    #converting an image to grayscale
    grayScaleImage = cv2.cvtColor(originalImage, cv2.COLOR_BGR2GRAY)
    reSized2 = cv2.resize(grayScaleImage, (1536, 1024))
    figures['GrayScaled'] = reSized2

    #applying median blur to smoothen an image
    smoothGrayScale = cv2.medianBlur(grayScaleImage, 5)
    reSized3 = cv2.resize(smoothGrayScale, (1536, 1024))
    figures['Smoothened Gray'] = reSized3

    #retrieving the edges for cartoon effect by using thresholding technique.
    getEdge = cv2.adaptiveThreshold(smoothGrayScale, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
    reSized4 = cv2.resize(getEdge, (1536, 1024))
    figures['Extracted Edges'] = reSized4

    #applying bilateral filter to remove noise and keep edge sharp as required
    colorImage = cv2.bilateralFilter(RGBImage, 9, 300, 300)
    reSized5 = cv2.resize(colorImage, (1536, 1024))
    figures['lightened color'] = reSized5

    #masking edged image with our "BEAUTIFY" image
    cartoonImage = cv2.bitwise_and(colorImage, colorImage, mask=getEdge)
    reSized6 = cv2.resize(cartoonImage, (1536, 1024))
    figures['Cartoon Image'] = reSized6

    cImage.image = ImageTk.PhotoImage(Image.fromarray(reSized6).resize((400, 400)))
    cImage.configure(image=cImage.image)



def visualizeTransformations():
    fig = plt.figure()
    i = 1
    for figure in figures.keys():
        ax = fig.add_subplot(2, 3, i)
        plt.xticks([]), plt.yticks([])
        ax.imshow(figures[figure], cmap='gray')
        ax.set_title(figure)
        i += 1
    plt.show()



root = tk.Tk()
root.geometry('1400x720+50+50')
root.title('Cartoonifier')
root.resizable(0, 0)

imagePath = tk.StringVar()

header = tk.Label(root, text='Cartoonify Images with OpenCV', font='arial 20 bold', justify=tk.CENTER, bg='black', fg='white',
               height=2)

middle = tk.Frame(root)
originalImage = tk.Frame(middle)
oImage = tk.Label(originalImage)
originalImage.pack(fill=tk.BOTH)
oImage.pack(fill=tk.BOTH)
originalImage.pack(fill=tk.BOTH, side=tk.LEFT, padx=(70, 100))

cartoonifiedImage = tk.Frame(middle)
cImage = tk.Label(cartoonifiedImage)
cartoonifiedImage.pack()
cImage.pack(fill=tk.BOTH)

tail = tk.Frame(root)

tools = tk.Frame(tail)
uploadButton = tk.Button(tools, text='Upload Image', bg='black', fg='white',font='arial 13', command=upload)
cartoonifyButton = tk.Button(tools, text='Cartoonify', bg='black', fg='white',font='arial 13', command=lambda: cartoonify(imagePath.get()))
visualizeButton = tk.Button(tools, text='visualize Transformations', bg='black', fg='white',font='arial 13', command=visualizeTransformations)
uploadButton.pack(side=tk.LEFT, padx=(450, 20))
cartoonifyButton.pack(side=tk.LEFT, padx=(0, 20))
visualizeButton.pack(side=tk.LEFT, padx=(0, 20))
tools.pack(fill=tk.BOTH, pady=(0, 20))

blackBar = tk.Label(tail, bg='black', height=2)
blackBar.pack(side=tk.BOTTOM, fill=tk.BOTH)

header.pack(fill=tk.BOTH)
middle.pack(fill=tk.BOTH, pady=(50, 100))
tools.pack(fill=tk.BOTH)
tail.pack(fill=tk.BOTH, side=tk.BOTTOM)

root.mainloop()