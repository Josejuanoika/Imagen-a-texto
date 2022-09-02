import cv2
import imutils
from tkinter import *
from tkinter import filedialog
import pytesseract
from PIL import Image
from PIL import ImageTk
import xerox

def center(toplevel):
    toplevel.update_idletasks()
    w = toplevel.winfo_screenwidth()
    h = toplevel.winfo_screenheight()
    size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
    x = (w / 2 - size[0] / 2)
    y = (h / 2 - size[1] / 2) - 40
    toplevel.geometry("%dx%d+%d+%d" % (size + (x, y)))

main = Tk()
main.title("Img to Text")
main.minsize(width=1100, height=1000)
main.resizable(width=FALSE, height=FALSE)
center(main)

lblImgOriginal = Label(main)
lblImgOriginal.configure(bg="#808080")
lblImgOriginal.place(x=50,y=10,height=550,width=495)

lblImgPro = Label(main)
lblImgPro.configure(bg="#808080")
lblImgPro.place(x=560,y=10,height=550,width=495)

resultado = Text(main)
resultado.place(x=50,y=570,height=370,width=1000)

scroll = Scrollbar(main)
resultado.config(yscrollcommand=scroll.set)
scroll.config(command=resultado.yview)
scroll.place(x=1050,y=570,height=370,width=20)

def textArea():
    file = Image.open('temp/temp1.png')
    text = str(pytesseract.image_to_string(file, lang='spa'))

    return text

def prepro(img):

    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 0)
    ret, binary = cv2.threshold(imgBlur, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_TRIANGLE)

    cv2.imwrite("temp/temp1.png", binary)

def resiz(imagen):

    pro = 495 / imagen.shape[1]
    w = 495
    h = int(imagen.shape[0] * pro)

    if h > 550:
        pro = 550 / imagen.shape[0]
        w = int(imagen.shape[1] * pro)
        h = 550

    return w,h


def cargar():
    resultado.delete('1.0', END)
    filetypes = (
        ('PNG files', '*.png'),
        ('JPEG files', '*.jpeg'),
        ('JPG files', '*.jpg'),
    )
    dirImage = filedialog.askopenfilename(filetypes=filetypes)
    imagen = cv2.imread(dirImage)

    w,h = resiz(imagen)

    imgWarped = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
    imgWarped0 = imutils.resize(imgWarped, height=h, width=w)
    im2 = Image.fromarray(imgWarped0)
    img2 = ImageTk.PhotoImage(image=im2)
    lblImgOriginal.configure(image=img2)
    lblImgOriginal.image = img2

    prepro(imagen)

    imagen = cv2.imread('temp/temp1.png')

    w,h = resiz(imagen)

    imgWarped = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
    imgWarped0 = imutils.resize(imgWarped, height=h, width=w)
    im2 = Image.fromarray(imgWarped0)
    img2 = ImageTk.PhotoImage(image=im2)
    lblImgPro.configure(image=img2)
    lblImgPro.image = img2

    text = textArea()
    resultado.insert(INSERT, text)

btnSalir = Button(main,text="Cargar Imagen",command=cargar)
btnSalir.place(x=50,y=950,height=40,width=300)

def limpiar():
    resultado.delete('1.0', END)
    lblImgPro.configure(image='')
    lblImgOriginal.configure(image='')

btnLimpiar = Button(main,text="Limpiar",command=limpiar)
btnLimpiar.place(x=400,y=950,height=40,width=300)

def copiar():
    xerox.copy(resultado.get('1.0', END))

btnAceptar = Button(main,text="Copiar",command=copiar)
btnAceptar.place(x=750,y=950,height=40,width=300)

main.mainloop()