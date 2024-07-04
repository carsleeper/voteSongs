import csv
from tkinter import filedialog
from tkinter import *
from tkinter import messagebox

filedir = ""
songDictionary = {}

#frame change
def openFrame(frame):
    frame.tkraise()
    
#loading csv file
def fileSelection():
    global filedir
    filePath = filedialog.askopenfilename(title="파일을 선택하세요",filetypes=[("csv files", "*.csv")])
    if filePath:
        global numberOfPeople
        filedir = f"{filePath}"
        openFrame(mainFrame)
        with open(filedir, 'r',encoding="utf-8") as w:
            lines = w.readlines()
            numberOfPeople = len(lines)-1
            createLabels()
    else:
        messagebox.showwarning("오류", "파일을 선택하세요.")

def createLabels():
    global label0
    for i in range(0,((numberOfPeople)//2)+1):
        if i == 0:
            label0 = Label(mainFrame, text="모두가 동의 한 곡:",font=("Arial", 20))
            label0.place(relx=0.5,rely=0, anchor="n")
        else:
            globals()[f"label{i}"] = Label(mainFrame,text=f"{i}명 빼고 동의한 곡:", font=("Arial", 20))
            globals()[f"label{i}"].place(relx=0.5,rely=i/(((numberOfPeople)//2)+2), anchor="n")
    mainFrame.update_idletasks()
    sorting()


def sorting():
    global songDictionary
    # CSV 파일을 열고 DictReader를 사용하여 읽기
    with open(filedir, newline='') as work:
        content = csv.DictReader(work)
        #songDictionary Emptying
        for songs in content:
            for i, song in enumerate(songs.keys()):
                if i == 0 or i == 1:
                    continue
                songDictionary[song] = list()

    with open(filedir, newline='') as work:
        content = csv.DictReader(work)
        #songDictionary making
        for songs in content:
            for i, song in enumerate(songs.keys()):
                if i == 0 or i == 1:
                    continue
                songDictionary[song].append(songs[song])

        #agreeList making
        for i in range(0,(numberOfPeople//2)+1):
            globals()[f"agree{i}List"] = list()
            for song in songDictionary.keys():
                if songDictionary[song].count("good") == numberOfPeople-i:
                    globals()[f"agree{i}List"].append(song)
            

        #label attaching
        for j in range(0,(numberOfPeople//2)+1):
            for i, song in enumerate(globals()[f"agree{j}List"], start=1):
                    label = Label(mainFrame, text = song, font=("Arial", 13))
                    if j == 0:
                        label.place(relx=0.5,rely= (label0.winfo_y()+(label1.winfo_y() - label0.winfo_y())*(i/(len(globals()[f"agree{j}List"])+1))) / mainFrame.winfo_height(), anchor="n")
                    elif j == (numberOfPeople//2):
                        label.place(relx=0.5,rely=(globals()[f"label{j}"].winfo_y()+float((1 - (mainFrame.winfo_height())*globals()[f"label{j}"].winfo_y())*(i/(len(globals()[f"agree{j}List"])+1)))) / mainFrame.winfo_height(), anchor="n")
                    else:
                        label.place(relx=0.5,rely=(globals()[f"label{j}"].winfo_y()+float((globals()[f"label{j+1}"].winfo_y() - globals()[f"label{j}"].winfo_y())*(i/(len(globals()[f"agree{j}List"])+1)))) / mainFrame.winfo_height(), anchor="n")


#fundametal settings
window = Tk()
window.title("선곡")
window.geometry("1200x700")

#main frame
mainFrame = Frame(window)
mainFrame.place(x=0,y=0, relheight=1,relwidth=1)



#csv selection frame
previousFrame = Frame(window)
previousFrame.place(x=0,y=0, relheight=1,relwidth=1)
inform = Label(previousFrame, text="csv파일을 선택하세요", font=("Arial", 20))
inform.place(relx=0.5,rely=0.4,anchor="center")
csvSeletion = Button(previousFrame,text="선택", command= fileSelection)
csvSeletion.place(relx=0.5,rely=0.5,anchor="center")

openFrame(previousFrame)
window.mainloop()


