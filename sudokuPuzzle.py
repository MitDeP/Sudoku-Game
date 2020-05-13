import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QDialog, QMainWindow, QTextEdit, QAction, QMenu
from PyQt5.QtGui import QIcon, QPainter, QFont, QPen
from PyQt5.QtCore import pyqtSlot, Qt

from sudokuEngine import *

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
        
        self.setAutoFillBackground(True)
        pal = self.palette()
        pal.setColor(self.backgroundRole(), Qt.white)
        self.setPalette(pal)
        self.m = PaintWidget(self)
        self.m.move(0,0)
        self.m.resize(self.width, self.height)

        setButton = QPushButton('Set', self)
        setButton.move(1000, 450)
        setButton.clicked.connect(self.setSquareValues)

        solveButton = QPushButton('Solve', self)
        solveButton.move(1000,500)
        

        checkButton = QPushButton('Check Solution', self)
        checkButton.move(1000, 550)

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


        menubar = self.menuBar()
        puzzleMenu = menubar.addMenu('Puzzle')
        generateMenu = QMenu('Generate New', self)
        generateVEasyDifficulty = QAction('Very Easy', self)
        generateEasyDifficulty = QAction('Easy', self)
        generateMedDifficulty = QAction('Medium', self)
        generateHardDifficulty = QAction('Hard', self)
        generateVHardDifficulty = QAction('Very Hard', self)
        generateImpossibleDifficulty = QAction('Impossible', self)
        generateMenu.addAction(generateVEasyDifficulty)
        generateMenu.addAction(generateEasyDifficulty)
        generateMenu.addAction(generateMedDifficulty)
        generateMenu.addAction(generateHardDifficulty)
        generateMenu.addAction(generateVHardDifficulty)
        generateMenu.addAction(generateImpossibleDifficulty)

        generateVEasyDifficulty.triggered.connect(self.generateVEasyPuzzle)

        puzzleMenu.addMenu(generateMenu)





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


    def generateVEasyPuzzle(self):
        puzzle = sudokuPuzzle()
        puzzle.createPuzzle(5)
        for row in puzzle.board:
            for cell in row:
                print(cell['val'])
        self.loadPuzzle(puzzle)

    def loadPuzzle(self, puzzle):
        for i in range(9):
            for j in range(9):
                if(puzzle.board[i][j]['val'] != ' '):
                    self.boxes[i][j].setText(str(puzzle.board[i][j]['val']))
        self.setSquareValues() 
        



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

