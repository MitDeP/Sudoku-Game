import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QDialog, QMainWindow, QTextEdit
from PyQt5.QtGui import QIcon, QPainter, QFont, QPen
from PyQt5.QtCore import pyqtSlot, Qt

class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'Sudoku Puzzle Game'
        self.left = 10
        self.top = 10
        self.width = 1250
        self.height = 800
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        menu = self.menuBar()
        puzzleMenu = menu.addMenu('Puzzle')

        self.setAutoFillBackground(True)
        pal = self.palette()
        pal.setColor(self.backgroundRole(), Qt.white)
        self.setPalette(pal)
        self.m = PaintWidget(self)
        self.m.move(0,0)
        self.m.resize(self.width, self.height)

        setButton = QPushButton('Set', self)
        setButton.move(500, 750)
        setButton.clicked.connect(self.setSquareValues)

        #enterButton = QPushButton("You should not see this", self)
        #enterButton.clicked.connect(self.enter)

        l1 = [QTextEdit(self) for i in range(9)]
        l2 = [QTextEdit(self) for i in range(9)]
        l3 = [QTextEdit(self) for i in range(9)]
        l4 = [QTextEdit(self) for i in range(9)]
        l5 = [QTextEdit(self) for i in range(9)]
        l6 = [QTextEdit(self) for i in range(9)]
        l7 = [QTextEdit(self) for i in range(9)]
        l8 = [QTextEdit(self) for i in range(9)]
        l9 = [QTextEdit(self) for i in range(9)]

        self.boxes =[l1, l2, l3, l4, l5, l6, l7, l8, l9]

        ypos = 50
        for row in self.boxes:
            xpos = 300
            for b in row:
                b.move(xpos, ypos)
                b.resize(60, 60)
                xpos += 65
                b.setFont(QFont('Arial', 10))
                #b.returnPressed.connect(self.enter)

            ypos += 65





        self.show()

    #@pyqtSlot()
    def setSquareValues(self):
        for row in self.boxes:
            for box in row:
                text = box.toPlainText()
                print(text)
                if(text != ""):
                    box.setAlignment(Qt.AlignCenter)
                    box.setFont(QFont('Arial', 20))
                    box.setEnabled(False)

    #@pyqtSlot()
    def enter(self):
        for row in self.boxes:
            for box in row:
                if(len(box.text()) == 1):
                    box.setAlignment(Qt.AlignCenter)
                    box.setFont(QFont('Arial', 20))
                else:
                    box.setAlignment(Qt.AlignRight)
                    box.setFont(QFont('Arial', 8))



class PaintWidget(QWidget):
    def paintEvent(self, event):
        qp = QPainter(self)
        qp.setPen(QPen(Qt.black, 5, Qt.SolidLine))
        size = self.size()

        #qp.drawRect(292, 42, 595, 595)
        qp.drawRect(297, 47, 586, 586)
        qp.drawRect(297, 47, 195, 195)
        qp.drawRect(491, 47, 195, 195)
        qp.drawRect(687, 47, 195, 195)

        qp.drawRect(297, 242, 195, 195)
        qp.drawRect(491, 242, 195, 195)
        qp.drawRect(687, 242, 195, 195)

        qp.drawRect(297, 437, 195, 195)
        qp.drawRect(491, 437, 195, 195)
        qp.drawRect(687, 437, 195, 195)      

        

        
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

