from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys
import csv
## 구상 : 설정창에서 기타세션 최소 충족 인원 수 등등을 정할 수 있게 하고,
##        결과창에서 가능여부, 가능하면 그 곡의 맴버들을 정해줌. 

class voteSongs(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('voteSongs')
        self.resize(700,400)
        #open window at center
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        self.windowPage = QStackedWidget()
        self.loadFile()
        self.songDictionary = {}

        self.show()

    def addWindowPage(self, Groupbox):
        self.windowPage.addWidget(Groupbox)
        self.setCentralWidget(self.windowPage)

    def selectWindowPage(self, QWid):
        self.windowPage.setCurrentWidget(QWid)

    def sorting(self):
        #defining numberOfPeople
        with open(self.fname[0], 'r',encoding="utf-8") as w:
            lines = w.readlines()
            self.numberOfPeople = len(lines)-1
        
        sortingGroupBox = QGroupBox()
        sortingHbox = QHBoxLayout()
        sortingVbox = QVBoxLayout()
        sortingHbox.addStretch(1)
        sortingHbox.addLayout(sortingVbox)
        sortingHbox.addStretch(1)

        sortingGroupBox.setLayout(sortingHbox)

        self.addWindowPage(sortingGroupBox)
        self.selectWindowPage(sortingGroupBox)

        self.bigfont = QFont()
        self.bigfont.setPointSizeF(20)

        self.smallfont = QFont()
        self.smallfont.setPointSizeF(15)

        #make informing label 
        for i in range(0,((self.numberOfPeople)//2)+1):
            if i == 0:
                self.label0 = QLabel('모두가 동의 한 곡', self)
            else:
                setattr(self, f"label{i}", QLabel(f'{i}명 빼고 동의한 곡'))

        #songDictionary Emptying
        with open(self.fname[0],'r', newline='', encoding='utf-8') as work:
            content = csv.DictReader(work)
            for songs in content:
                for i, song in enumerate(songs.keys()):
                    if i == 0 or i == 1:
                        continue
                    self.songDictionary[song] = list()

        #songDictionary making
        with open(self.fname[0],'r', newline='', encoding='utf-8') as work:
            content = csv.DictReader(work)
            for songs in content:
                for i, song in enumerate(songs.keys()):
                    if i == 0 or i == 1:
                        continue
                    self.songDictionary[song].append(songs[song])

            #agreeList making
            for i in range(0,(self.numberOfPeople//2)+1):
                setattr(self, f'agreeList{i}', list())
                for song in self.songDictionary.keys():
                    if self.songDictionary[song].count("good") == self.numberOfPeople-i:
                        getattr(self, f'agreeList{i}').append(song)

            #Labelling
            for i in range(0,(self.numberOfPeople//2)+1):
                getattr(self,f"label{i}").setFont(self.bigfont)
                sortingVbox.addWidget(getattr(self,f"label{i}"))
                for song in getattr(self,f'agreeList{i}'):
                    label = QLabel(song)
                    label.setFont(self.smallfont)
                    sortingVbox.addWidget(label)
                sortingVbox.addSpacing(25)

    def showFileDialog(self):
        while True:
            self.fname = QFileDialog.getOpenFileName(self,'Open csv file','./','csv Files(*.csv)')
            if self.fname[0]:
                break
            else:
                QMessageBox.question(self, 'Error','please choose file.', QMessageBox.Yes, QMessageBox.Yes)
        self.sorting()

    # loadFileBox < loadFileGroupbox < windowPage
    def loadFile(self):
        loadFileGroupbox = QGroupBox()
        informBtn = QPushButton('Click to load .csv file')
        informBtn.clicked.connect(self.showFileDialog)
        loadFileVbox = QVBoxLayout()
        loadFileVbox.addWidget(informBtn)
        loadFileHbox = QHBoxLayout()
        loadFileHbox.addStretch(1)
        loadFileHbox.addLayout(loadFileVbox)
        loadFileHbox.addStretch(1)

        loadFileGroupbox.setLayout(loadFileHbox)

        self.addWindowPage(loadFileGroupbox)
        self.selectWindowPage(loadFileGroupbox)


if __name__ =="__main__":
    app =QApplication(sys.argv)
    ex = voteSongs()
    sys.exit(app.exec_())