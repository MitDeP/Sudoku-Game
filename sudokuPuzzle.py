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
        self.puzzle = sudokuPuzzle()
        
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
        checkButton.clicked.connect(self.checkSolution)

        #enterButton = QPushButton("You should not see this", self)
        #enterButton.clicked.connect(self.enter)

        l1 = [QLineEdit(self) for i in range(9)]
        l2 = [QLineEdit(self) for i in range(9)]
        l3 = [QLineEdit(self) for i in range(9)]
        l4 = [QLineEdit(self) for i in range(9)]
        l5 = [QLineEdit(self) for i in range(9)]
        l6 = [QLineEdit(self) for i in range(9)]
        l7 = [QLineEdit(self) for i in range(9)]
        l8 = [QLineEdit(self) for i in range(9)]
        l9 = [QLineEdit(self) for i in range(9)]

        self.boxes =[l1, l2, l3, l4, l5, l6, l7, l8, l9]

        ypos = 50
        for row in self.boxes:
            xpos = 300
            for b in row:
                b.move(xpos, ypos)
                b.resize(60, 60)
                xpos += 65
                b.setFont(QFont('Arial', 10))
                b.textChanged.connect(self.enter)

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
        generateEasyDifficulty.triggered.connect(self.generateEasyPuzzle)
        generateMedDifficulty.triggered.connect(self.generateMedPuzzle)
        generateHardDifficulty.triggered.connect(self.generateHardPuzzle)
        generateVHardDifficulty.triggered.connect(self.generateVHardPuzzle)
        generateImpossibleDifficulty.triggered.connect(self.generateImpossiblePuzzle)

        puzzleMenu.addMenu(generateMenu)





        self.show()

    #@pyqtSlot()
    def setSquareValues(self):
        for row in self.boxes:
            for box in row:
                text = box.text()
                if(text != "" and len(text) == 1):
                    box.setAlignment(Qt.AlignCenter)
                    box.setFont(QFont('Arial', 20))
                    box.setEnabled(False)


    def generateVEasyPuzzle(self):
        self.puzzle = sudokuPuzzle()
        self.puzzle.createPuzzle(5)
        self.loadPuzzle(self.puzzle)

    def generateEasyPuzzle(self):
        self.puzzle = sudokuPuzzle()
        self.puzzle.createPuzzle(4)
        self.loadPuzzle(self.puzzle)
    
    def generateMedPuzzle(self):
        self.puzzle = sudokuPuzzle()
        self.puzzle.createPuzzle(3)
        self.loadPuzzle(self.puzzle)
    
    def generateHardPuzzle(self):
        self.puzzle = sudokuPuzzle()
        self.puzzle.createPuzzle(2)
        self.loadPuzzle(self.puzzle)

    def generateVHardPuzzle(self):
        self.puzzle = sudokuPuzzle()
        self.puzzle.createPuzzle(1)
        self.loadPuzzle(self.puzzle)

    def generateImpossiblePuzzle(self):
        self.puzzle = sudokuPuzzle()
        self.puzzle.createPuzzle(0)
        self.loadPuzzle(self.puzzle)

    def loadPuzzle(self, puzzle):
        self.clearBoard()
        for i in range(9):
            for j in range(9):
                if(puzzle.board[i][j]['val'] != ' '):
                    self.boxes[i][j].setText(str(puzzle.board[i][j]['val']))
        self.setSquareValues() 

    def clearBoard(self):
        for row in self.boxes:
            for content in row:
                content.setText("")
                content.setEnabled(True)
        
    def checkSolution(self):
        numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
        finished = True
        for i in range(9):
            for j in range(9):
                text = self.boxes[i][j].text()
                if(text not in numbers):
                    finished = False
                else:
                        self.puzzle.board[i][j]['val'] = int(text)
        
        if(finished):
            if(self.puzzle.colCheck() and self.puzzle.rowCheck() and self.puzzle.sectorCheck()):
                print("Valid solution")
            else:
                print("Incorrect solution")
        else:
            print("Your submission was invalid!")

    def enter(self):
        for row in self.boxes:
            for box in row:
                values = box.text()
                if(len(values) > 0):
                    box.setFont(QFont('Arial', 21-len(values)))
                    box.setAlignment(Qt.AlignCenter)
                else:
                    box.setFont(QFont('Arial', 10))
                    box.setAlignment(Qt.AlignLeft)




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

