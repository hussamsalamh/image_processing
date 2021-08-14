import tkinter as tk
import tkinter.font as tkFont
from fill_id_number import *
from imageProcessing import *
LARGEFONT = ("Verdana", 35)


class GUI(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        width = 774
        height = 632
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.geometry(alignstr)
        self.resizable(width=False, height=False)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (MainPage,CalculationPage,fillIdPage):
            frame = F(container, self)
            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(MainPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()



class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        GLabel_338 = tk.Label(self)
        GLabel_338["activeforeground"] = "#cc2e2e"
        GLabel_338["anchor"] = "center"
        GLabel_338["bg"] = "#fefdfd"
        GLabel_338["disabledforeground"] = "#ffffff"
        ft = tkFont.Font(family='Times', size=18)
        GLabel_338["font"] = ft
        GLabel_338["fg"] = "#333333"
        GLabel_338["justify"] = "center"
        GLabel_338["text"] = "Main Page "
        GLabel_338.place(x=260, y=70, width=215, height=39)

        GButton_258 = tk.Button(self)
        GButton_258["bg"] = "#8f8f8f"
        ft = tkFont.Font(family='Times', size=10)
        GButton_258["font"] = ft
        GButton_258["fg"] = "#000000"
        GButton_258["justify"] = "center"
        GButton_258["text"] = "Fill Id Number"
        GButton_258.place(x=10, y=570, width=159, height=49)
        GButton_258["command"] = lambda :controller.show_frame(fillIdPage)

        GButton_585 = tk.Button(self)
        GButton_585["bg"] = "#7e7e7e"
        ft = tkFont.Font(family='Times', size=10)
        GButton_585["font"] = ft
        GButton_585["fg"] = "#000000"
        GButton_585["justify"] = "center"
        GButton_585["text"] = "Calculate Grades"
        GButton_585.place(x=620, y=570, width=145, height=49)
        GButton_585["command"] = lambda :controller.show_frame(CalculationPage)


class CalculationPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        GLabel_338 = tk.Label(self)
        GLabel_338["activeforeground"] = "#cc2e2e"
        GLabel_338["anchor"] = "center"
        GLabel_338["bg"] = "#fefdfd"
        GLabel_338["disabledforeground"] = "#ffffff"
        ft = tkFont.Font(family='Times', size=18)
        GLabel_338["font"] = ft
        GLabel_338["fg"] = "#333333"
        GLabel_338["justify"] = "center"
        GLabel_338["text"] = "Calculation Grade"
        GLabel_338.place(x=10, y=20, width=215, height=39)

        GButton_258 = tk.Button(self)
        GButton_258["bg"] = "#8f8f8f"
        ft = tkFont.Font(family='Times', size=10)
        GButton_258["font"] = ft
        GButton_258["fg"] = "#000000"
        GButton_258["justify"] = "center"
        GButton_258["text"] = "Fill Id Number"
        GButton_258.place(x=10, y=570, width=159, height=49)
        GButton_258["command"] = lambda :controller.show_frame(fillIdPage)

        GButton_585 = tk.Button(self)
        GButton_585["bg"] = "#7e7e7e"
        ft = tkFont.Font(family='Times', size=10)
        GButton_585["font"] = ft
        GButton_585["fg"] = "#000000"
        GButton_585["justify"] = "center"
        GButton_585["text"] = "Main Page"
        GButton_585.place(x=620, y=570, width=145, height=49)
        GButton_585["command"] = lambda :controller.show_frame(MainPage)

        GButton_970 = tk.Button(self)
        GButton_970["bg"] = "#c6c6c6"
        ft = tkFont.Font(family='Times', size=10)
        GButton_970["font"] = ft
        GButton_970["fg"] = "#000000"
        GButton_970["justify"] = "center"
        GButton_970["text"] = "Make Calculation"
        GButton_970.place(x=310, y=430, width=155, height=53)
        GButton_970["command"] = self.MakeCalculationButton

        GLabel_730 = tk.Label(self)
        GLabel_730["activebackground"] = "#cfcbcb"
        GLabel_730["activeforeground"] = "#e3e1e1"
        GLabel_730["bg"] = "#9a9a9a"
        ft = tkFont.Font(family='Times', size=10)
        GLabel_730["font"] = ft
        GLabel_730["fg"] = "#333333"
        GLabel_730["justify"] = "center"
        GLabel_730["text"] = "Image Path"
        GLabel_730.place(x=60, y=140, width=113, height=45)

        self.imagePath = tk.Text(self, height=2,
                                 width=30,
                                 bg="light yellow")
        self.imagePath.place(x=180, y=140)

        GLabel_641 = tk.Label(self)
        GLabel_641["bg"] = "#a0a0a0"
        ft = tkFont.Font(family='Times', size=10)
        GLabel_641["font"] = ft
        GLabel_641["fg"] = "#333333"
        GLabel_641["justify"] = "center"
        GLabel_641["text"] = "Student folder path "
        GLabel_641.place(x=60, y=210, width=112, height=43)

        self.studentImagesPath = tk.Text(self, height=2,
                                  width=30,
                                  bg="light yellow")
        self.studentImagesPath.place(x=180, y=210)

        GLabel_218 = tk.Label(self)
        GLabel_218["bg"] = "#a4a4a4"
        ft = tkFont.Font(family='Times', size=10)
        GLabel_218["font"] = ft
        GLabel_218["fg"] = "#333333"
        GLabel_218["justify"] = "center"
        GLabel_218["text"] = "Type of chapter"
        GLabel_218.place(x=60, y=280, width=112, height=51)

        self.chapterType = tk.Text(self, height=2,
                                   width=30,
                                   bg="light yellow")
        self.chapterType.place(x=180, y=280)


    def MakeCalculationButton(self):
        imgPath = self.imagePath.get("1.0", "end-1c")
        studentPath = self.studentImagesPath.get("1.0", "end-1c")
        chapterType = self.chapterType.get("1.0", "end-1c")
        if imgPath == '' or studentPath == '' or chapterType == '' or len(chapterType) != 8:
            return
        pro = imageProcessing(imgPath, studentPath, chapterType)
        pro.doAction()






class fillIdPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        GLabel_863=tk.Label(self)
        ft = tkFont.Font(family='Times',size=20)
        GLabel_863["font"] = ft
        GLabel_863["fg"] = "#333333"
        GLabel_863["justify"] = "center"
        GLabel_863["text"] = "Fill the Id"
        GLabel_863.place(x=0,y=10,width=223,height=38)

        GButton_223=tk.Button(self)
        GButton_223["bg"] = "#aeaeae"
        ft = tkFont.Font(family='Times',size=10)
        GButton_223["font"] = ft
        GButton_223["fg"] = "#000000"
        GButton_223["justify"] = "center"
        GButton_223["text"] = "Main Page"
        GButton_223.place(x=620, y=570, width=145, height=49)
        GButton_223["command"] = lambda :controller.show_frame(MainPage)

        GButton_430=tk.Button(self)
        GButton_430["bg"] = "#b3b3b3"
        ft = tkFont.Font(family='Times',size=10)
        GButton_430["font"] = ft
        GButton_430["fg"] = "#000000"
        GButton_430["justify"] = "center"
        GButton_430["text"] = "Calculation Grade"
        GButton_430.place(x=10, y=570, width=159, height=49)
        GButton_430["command"] = lambda:controller.show_frame(CalculationPage)

        GButton_854=tk.Button(self)
        GButton_854["bg"] = "#d3d2d2"
        ft = tkFont.Font(family='Times',size=10)
        GButton_854["font"] = ft
        GButton_854["fg"] = "#000000"
        GButton_854["justify"] = "center"
        GButton_854["text"] = "fill the id "
        GButton_854.place(x=310, y=430, width=155, height=53)
        GButton_854["command"] = self.fillIdButton

        # image path
        GLabel_730 = tk.Label(self)
        GLabel_730["activebackground"] = "#cfcbcb"
        GLabel_730["activeforeground"] = "#e3e1e1"
        GLabel_730["bg"] = "#9a9a9a"
        ft = tkFont.Font(family='Times', size=10)
        GLabel_730["font"] = ft
        GLabel_730["fg"] = "#333333"
        GLabel_730["justify"] = "center"
        GLabel_730["text"] = "Image"
        GLabel_730.place(x=60, y=140, width=113, height=45)

        self.imagePath = tk.Text(self, height=2,
                        width=30,
                        bg="light yellow")
        self.imagePath.place(x= 180 ,y=140)


        GLabel_641 = tk.Label(self)
        GLabel_641["bg"] = "#a0a0a0"
        ft = tkFont.Font(family='Times', size=10)
        GLabel_641["font"] = ft
        GLabel_641["fg"] = "#333333"
        GLabel_641["justify"] = "center"
        GLabel_641["text"] = "output Path"
        GLabel_641.place(x=60, y=210, width=112, height=43)

        self.outputPath = tk.Text(self, height=2,
                                  width=30,
                                  bg="light yellow")
        self.outputPath.place(x=180, y=210)


        GLabel_218 = tk.Label(self)
        GLabel_218["bg"] = "#a4a4a4"
        ft = tkFont.Font(family='Times', size=10)
        GLabel_218["font"] = ft
        GLabel_218["fg"] = "#333333"
        GLabel_218["justify"] = "center"
        GLabel_218["text"] = "Students Info"
        GLabel_218.place(x=60, y=280, width=112, height=51)


        self.studentPath = tk.Text(self, height=2,
                             width=30,
                             bg="light yellow")
        self.studentPath.place(x=180, y=280)



    def fillIdButton(self):
        imgPath = self.imagePath.get("1.0","end-1c")
        outPath = self.outputPath.get("1.0","end-1c")
        studentP = self.studentPath.get("1.0","end-1c")
        if imgPath == '' or outPath == '' or studentP == '':
            return
        fi = fillID(imgPath,studentP,outPath)
        fi.makePic()


if __name__ == "__main__":
    root = GUI()
    root.mainloop()
