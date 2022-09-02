'''from PIL import Image
import pytesseract
import sys
from pdf2image import convert_from_path
import os

# Creating a text file to write the output
outfile = "out_text.txt"

# Open the file in append mode so that
# All contents of all images are added to the same file
f = open(outfile, "a")

filename = "resources/2.png"
file = Image.open(filename)

# Recognize the text as string in image using pytesserct
text = str(pytesseract.image_to_string(file,lang='spa'))

# The recognized text is stored in variable text
# Any string processing may be applied on text
# Here, basic formatting has been done:
# In many PDFs, at line ending, if a word can't
# be written fully, a 'hyphen' is added.
# The rest of the word is written in the next line
# Eg: This is a sample text this word here GeeksF-
# orGeeks is half on first line, remaining on next.
# To remove this, we replace every '-\n' to ''.
text = text.replace('-\n', '')

# Finally, write the processed text to the file.
f.write(text)

# Close the file after writing all the text.
f.close()'''



'''from PIL import Image

# Morphological filtering
from skimage.morphology import opening
from skimage.morphology import disk

# Data handling
import numpy as np

# Connected component filtering
import cv2

black = 0
white = 255
threshold = 160

# Open input image in grayscale mode and get its pixels.
img = Image.open("resources/wea.png").convert("LA")
pixels = np.array(img)[:,:,0]

# Remove pixels above threshold
pixels[pixels > threshold] = white
pixels[pixels < threshold] = black


# Morphological opening
blobSize = 1 # Select the maximum radius of the blobs you would like to remove
structureElement = disk(blobSize)  # you can define different shapes, here we take a disk shape
# We need to invert the image such that black is background and white foreground to perform the opening
pixels = np.invert(opening(np.invert(pixels), structureElement))


# Create and save new image.
newImg = Image.fromarray(pixels).convert('RGB')
newImg.save("xd2.PNG")

# Find the connected components (black objects in your image)
# Because the function searches for white connected components on a black background, we need to invert the image
nb_components, output, stats, centroids = cv2.connectedComponentsWithStats(np.invert(pixels), connectivity=8)

# For every connected component in your image, you can obtain the number of pixels from the stats variable in the last
# column. We remove the first entry from sizes, because this is the entry of the background connected component
sizes = stats[1:,-1]
nb_components -= 1

# Define the minimum size (number of pixels) a component should consist of
minimum_size = 100

# Create a new image
newPixels = np.ones(pixels.shape)*255

# Iterate over all components in the image, only keep the components larger than minimum size
for i in range(1, nb_components):
    if sizes[i] > minimum_size:
        newPixels[output == i+1] = 0

# Create and save new image.
newImg = Image.fromarray(newPixels).convert('RGB')
newImg.save("xd3.PNG")'''

'''import cv2
import numpy as np

img = cv2.imread('resources/1.png')

imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
imgBlur = cv2.GaussianBlur(imgGray,(5,5),0)
ret, binary = cv2.threshold(imgBlur, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_TRIANGLE)

kernel = np.ones((5, 5))
imgThres = cv2.erode(binary, kernel, iterations=1)

cv2.imshow('uwu',img)
cv2.imshow('owo',binary)

cv2.waitKey(0)'''

from tkinter import *
import pyautogui
import cv2
import imutils
from tkinter import *
from tkinter import filedialog
import pytesseract
from PIL import Image
from PIL import ImageTk
import xerox
import datetime

band = 0

class Application():
    def __init__(self, master):
        global band
        self.master = master
        self.rect = None
        self.x = self.y = 0
        self.start_x = None
        self.start_y = None
        self.curX = None
        self.curY = None

        # root.configure(background = 'red')
        # root.attributes("-transparentcolor","red")

        def center(toplevel):
            toplevel.update_idletasks()
            w = toplevel.winfo_screenwidth()
            h = toplevel.winfo_screenheight()
            size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
            x = (w / 2 - size[0] / 2)
            y = (h / 2 - size[1] / 2) - 40
            toplevel.geometry("%dx%d+%d+%d" % (size + (x, y)))

        main.title("Img to Text")
        main.minsize(width=1100, height=1000)
        main.resizable(width=FALSE, height=FALSE)
        center(main)

        lblImgPro = Label(main)
        lblImgPro.configure(bg="#808080")
        lblImgPro.place(x=560, y=10, height=5, width=5)

        lblImgOriginal = Label(main)
        lblImgOriginal.configure(bg="#808080")
        lblImgOriginal.place(x=50, y=10, height=550, width=990)



        resultado = Text(main)
        resultado.place(x=50, y=570, height=370, width=1000)

        scroll = Scrollbar(main)
        resultado.config(yscrollcommand=scroll.set)
        scroll.config(command=resultado.yview)
        scroll.place(x=1050, y=570, height=370, width=20)

        def textArea():
            file = Image.open('temp/temp1.png')
            text = str(pytesseract.image_to_string(file, lang='spa'))

            return text

        def prepro(img):
            imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            '''imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 0)'''
            ret, binary = cv2.threshold(imgGray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_TRIANGLE)

            cv2.imwrite("temp/temp1.png", img)

        def resiz(imagen):
            pro = 990 / imagen.shape[1]
            w = 990
            h = int(imagen.shape[0] * pro)

            if h > 550:
                pro = 550 / imagen.shape[0]
                w = int(imagen.shape[1] * pro)
                h = 550

            return w, h

        def cargarScreen():

            imagen = cv2.imread('temp/screenTemp.png')

            w, h = resiz(imagen)

            imgWarped = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
            imgWarped0 = imutils.resize(imgWarped, height=h, width=w)
            im2 = Image.fromarray(imgWarped0)
            img2 = ImageTk.PhotoImage(image=im2)
            lblImgOriginal.configure(image=img2)
            lblImgOriginal.image = img2

            prepro(imagen)

            imagen = cv2.imread('temp/temp1.png')

            w, h = resiz(imagen)

            imgWarped = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
            imgWarped0 = imutils.resize(imgWarped, height=h, width=w)
            im2 = Image.fromarray(imgWarped0)
            img2 = ImageTk.PhotoImage(image=im2)
            lblImgPro.configure(image=img2)
            lblImgPro.image = img2

            text = textArea()
            resultado.insert(INSERT, text)

        def cargar():
            resultado.delete('1.0', END)
            filetypes = (
                ('PNG files', '*.png'),
                ('JPEG files', '*.jpeg'),
                ('JPG files', '*.jpg'),
            )
            try:
                dirImage = filedialog.askopenfilename(filetypes=filetypes)
                imagen = cv2.imread(dirImage)

                w, h = resiz(imagen)

                imgWarped = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
                imgWarped0 = imutils.resize(imgWarped, height=h, width=w)
                im2 = Image.fromarray(imgWarped0)
                img2 = ImageTk.PhotoImage(image=im2)
                lblImgOriginal.configure(image=img2)
                lblImgOriginal.image = img2

                prepro(imagen)

            except:
                pass

            imagen = cv2.imread('temp/temp1.png')

            w, h = resiz(imagen)

            imgWarped = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
            imgWarped0 = imutils.resize(imgWarped, height=h, width=w)
            im2 = Image.fromarray(imgWarped0)
            img2 = ImageTk.PhotoImage(image=im2)
            lblImgPro.configure(image=img2)
            lblImgPro.image = img2

            text = textArea()
            resultado.insert(INSERT, text)

        btnCargar = Button(main, text="Cargar Imagen", command=cargar)
        btnCargar.place(x=50, y=950, height=40, width=242)

        btnCragarS = Button(main, text="Tomar Captura", command=self.createScreenCanvas)
        btnCragarS.place(x=302, y=950, height=40, width=242)

        print(band)
        if band == 1:
            cargarScreen()

        def limpiar():
            resultado.delete('1.0', END)
            lblImgPro.configure(image='')
            lblImgOriginal.configure(image='')

        btnLimpiar = Button(main, text="Limpiar", command=limpiar)
        btnLimpiar.place(x=554, y=950, height=40, width=242)

        def copiar():
            xerox.copy(resultado.get('1.0', END))

        btnCopiar = Button(main, text="Copiar", command=copiar)
        btnCopiar.place(x=806, y=950, height=40, width=242)


        self.master_screen = Toplevel(main)
        self.master_screen.withdraw()
        self.master_screen.attributes("-transparent", "blue")
        self.picture_frame = Frame(self.master_screen, background = "blue")
        self.picture_frame.pack(fill=BOTH, expand=YES)

    def takeBoundedScreenShot(self, x1, y1, x2, y2):
        im = pyautogui.screenshot(region=(x1, y1, x2, y2))
        im.save('temp/screenTemp.png')

    def createScreenCanvas(self):
        self.master_screen.deiconify()
        main.withdraw()

        self.screenCanvas = Canvas(self.picture_frame, cursor="cross", bg="grey11")
        self.screenCanvas.pack(fill=BOTH, expand=YES)

        self.screenCanvas.bind("<ButtonPress-1>", self.on_button_press)
        self.screenCanvas.bind("<B1-Motion>", self.on_move_press)
        self.screenCanvas.bind("<ButtonRelease-1>", self.on_button_release)

        self.master_screen.attributes('-fullscreen', True)
        self.master_screen.attributes('-alpha', .3)
        self.master_screen.lift()
        self.master_screen.attributes("-topmost", True)

    def on_button_release(self, event):
        self.recPosition()

        if self.start_x <= self.curX and self.start_y <= self.curY:
            print("right down")
            self.takeBoundedScreenShot(self.start_x, self.start_y, self.curX - self.start_x, self.curY - self.start_y)

        elif self.start_x >= self.curX and self.start_y <= self.curY:
            print("left down")
            self.takeBoundedScreenShot(self.curX, self.start_y, self.start_x - self.curX, self.curY - self.start_y)

        elif self.start_x <= self.curX and self.start_y >= self.curY:
            print("right up")
            self.takeBoundedScreenShot(self.start_x, self.curY, self.curX - self.start_x, self.start_y - self.curY)

        elif self.start_x >= self.curX and self.start_y >= self.curY:
            print("left up")
            self.takeBoundedScreenShot(self.curX, self.curY, self.start_x - self.curX, self.start_y - self.curY)

        self.exitScreenshotMode()
        return event

    def exitScreenshotMode(self):
        global band
        print("Screenshot mode exited")
        band = 1
        self.screenCanvas.destroy()
        self.master_screen.withdraw()
        main.deiconify()
        app = Application(main)

    def exit_application(self):
        print("Application exit")
        main.quit()

    def on_button_press(self, event):
        # save mouse drag start position
        self.start_x = self.screenCanvas.canvasx(event.x)
        self.start_y = self.screenCanvas.canvasy(event.y)

        self.rect = self.screenCanvas.create_rectangle(self.x, self.y, 1, 1, outline='red', width=3, fill="blue")

    def on_move_press(self, event):
        self.curX, self.curY = (event.x, event.y)
        # expand rectangle as you drag the mouse
        self.screenCanvas.coords(self.rect, self.start_x, self.start_y, self.curX, self.curY)

    def recPosition(self):
        print(self.start_x)
        print(self.start_y)
        print(self.curX)
        print(self.curY)

if __name__ == '__main__':
    main = Tk()
    app = Application(main)
    main.mainloop()