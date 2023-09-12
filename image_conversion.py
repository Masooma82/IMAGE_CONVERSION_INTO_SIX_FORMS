import cv2
import easygui # provides an easy-to-use interface for graphical user input
import os # used for interacting with the operating system, including file operations
import tkinter as tk #creating graphical user interfaces (GUIs) 
from tkinter import *
import matplotlib.pyplot as plt
root=tk.Tk()  #Tkinter root window, which is the main window of the GUI application
root.geometry('700x700')
root.title("Choose to convert !")
root.configure(background='light gray')

def u():
    Imagepath = easygui.fileopenbox() # opens a file dialog box using EasyGUI and assigns the selected file's path to the 'Imagepath'
    c(Imagepath)
def c(Imagepath):
    originalimage = cv2.imread(Imagepath) # uses OpenCV to read the image located at Imagepath and assigns it to the 'originalimage'
    originalimage = cv2.cvtColor(originalimage, cv2.COLOR_BGR2RGB) #convert color format of 'originalimage' from BGR to RGB
    
    if originalimage is None:
        print("Can not find out any image !!")
        sys.exit() # This exits the program if the image loading fails
    R_1 = cv2.resize(originalimage, (930,510))
    
    greyScaleImage = cv2.cvtColor(originalimage,cv2.COLOR_BGR2GRAY) #grayScale...each element of image contains a single intensity value (0 to 255)
    R_2 = cv2.resize(greyScaleImage, (930,510))
    
    smoothGrayImage = cv2.medianBlur(greyScaleImage, 5) #smoothGrayImage...contain the grayscale image with reduced noise and smoother transitions between pixel values
    R_3 = cv2.resize(smoothGrayImage, (930,510))
    
    getedge = cv2.adaptiveThreshold(smoothGrayImage, 255, cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY, 9, 9)
#cv2.ADAPTIVE_THRESH_MEAN_C: This parameter specifies the adaptive thresholding method. It uses the mean (average) of pixel values in a local neighborhood to determine the threshold. 
#cv2.THRESH_BINARY: This parameter specifies that pixels with values above the calculated threshold are set to the maximum value (255), and pixels below the threshold are set to 0. This results in a binary image.
#9: This is the size of the neighborhood used for calculating the adaptive threshold. In this case, it's a 9x9 pixel neighborhood.
#9: This is a constant subtracted from the mean (or weighted mean) value calculated in the neighborhood to fine-tune the threshold.
    R_4 = cv2.resize(getedge, (930, 510))
    
    colorImage = cv2.bilateralFilter(originalimage,9,300,300)#colorImage...typically smoother and less noisy than the original image while preserving important details and edges
    R_5 = cv2.resize(colorImage,(930, 510))
    
    cartoonImage = cv2.bitwise_and(colorImage,colorImage,mask=getedge) 
    R_6 = cv2.resize(cartoonImage, (930,510))
    
    
    images = [R_1,R_2,R_3,R_4,R_5,R_6]
    
    fig, axes = plt.subplots(3,2,figsize=(8,8), subplot_kw={'xticks':[],'yticks':[]},gridspec_kw = dict(hspace = 0.1, wspace = 0.1))#function call creates a grid of subplots within the main figure
    #3, 2: These parameters specify the number of rows and columns in the grid of subplots
    # specifies that the x-axis and y-axis ticks (labels) should be empty
    #spacing b/w subplots: hspace (vertical spacing) and wspace (horizontal spacing) are set to 0.1
    for i,ax in enumerate(axes.flat): # used to populate each subplot within the grid of subplots (axes) with images from the 'images' list 
        ax.imshow(images[i], cmap='gray')
    
    save1 = Button(root, text="Save Cartoon Image",command=lambda:save(R_6,Imagepath),padx=30,pady=5) #create a button
    save1.configure(background="red",foreground='yellow',font=('arial',20,"bold"))
    save1.pack(side=TOP,pady=50) #determines the position of button on window
    plt.show()

def save(Resized6, Imagepath):
    newname = "Converted Image"
    path1 = os.path.dirname(Imagepath) #path of original image
    extension = os.path.splitext(Imagepath)[1] #file format of original file
    path = os.path.join(path1,newname + extension) #create a path, file name and extension to save cartoon image there
    cv2.imwrite(path, cv2.cvtColor(Resized6, cv2.COLOR_RGB2BGR))
    I = "The saved image of the name "+ newname + "at" + path
    tk.messagebox.showinfo(title=None, message=I) 

a = Button(root,text="Conversion of image",command=u, padx=15, pady=10)
a.configure(background="black",foreground="white",font=("arial",30,"bold"))
a.pack(side=TOP,pady=50) 

root.mainloop()
    
    