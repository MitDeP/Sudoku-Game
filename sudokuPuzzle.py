import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QDialog, QMainWindow, QTextEdit, QAction, QMenu, QMessageBox, QCheckBox, QLabel, QHBoxLayout
from PyQt5.QtGui import QIcon, QPainter, QFont, QPen
from PyQt5.QtCore import pyqtSlot, Qt, QTimer

from sudokuEngine import *


class optionsMenu(QWidget):
    def __init__(self, mainWindow):
        super().__init__()
        self.mainWindow = mainWindow
        self.title = 'options'
        self.left = 20
        self.top = 20
        self.width = 320
        self.height = 400
        self.setWindowFlags(self.windowFlags() | Qt.CustomizeWindowHint)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowCloseButtonHint)
        #self.setWindowFlag(Qt.Window.CloseButtonHint, False)
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.passiveChecking = True
        self.activeChecking = True
        self.instantSolve = False
        self.cancelButton = QPushButton('Cancel', self)
        self.saveChangesButton = QPushButton('Save Changes', self)
        self.cancelButton.clicked.connect(self.exitClick)
        self.saveChangesButton.clicked.connect(self.saveClick)
        self.passiveCheckingBox = QCheckBox('Check while solving', self)
        self.activeCheckingBox = QCheckBox('Check at Submission Time', self)

        self.passiveCheckingBox.move(100, 100)
        self.passiveCheckingBox.resize(180, 40)
        self.activeCheckingBox.move(100, 200)
        self.activeCheckingBox.resize(320, 40)
        self.passiveCheckingBox.setChecked(self.passiveChecking)
        self.activeCheckingBox.setChecked(self.activeChecking)
        self.saveChangesButton.move(75, 300)
        self.cancelButton.move(200, 300)


    def openMenu(self):
        self.passiveCheckingBox.setChecked(self.passiveChecking)
        self.activeCheckingBox.setChecked(self.activeChecking)
        self.show()



    def saveClick(self):
        self.mainWindow.setEnabled(True)
        if self.activeCheckingBox.isChecked():
            self.activeChecking = True
        else:
            self.activeChecking = False

        if self.passiveCheckingBox.isChecked():
            self.passiveChecking = True
            self.mainWindow.passiveCheck()
        else:
            self.passiveChecking = False
            self.mainWindow.clearHighlights()

        self.close()



    def exitClick(self):
        self.close()
        self.mainWindow.setEnabled(True)


    

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
        self.activeHints = True
        self.passiveHints = True
        
    def initUI(self):
        self.makingPuzzle = False
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.optionsMenu = optionsMenu(self)
        
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
                b.textChanged.connect(self.setInputasValue)
                b.textChanged.connect(self.passiveCheck)

            ypos += 65


        menubar = self.menuBar()
        puzzleMenu = menubar.addMenu('Puzzle')
        optionMenu = menubar.addMenu('Options')
        generateMenu = QMenu('Generate New', self)
        clear = QAction('Reset', self)
        startOver = QAction('Clear Inputs', self)
        generateVEasyDifficulty = QAction('Very Easy', self)
        generateEasyDifficulty = QAction('Easy', self)
        generateMedDifficulty = QAction('Medium', self)
        generateHardDifficulty = QAction('Hard', self)
        generateVHardDifficulty = QAction('Very Hard', self)
        generateImpossibleDifficulty = QAction('Impossible', self)
        solvePuzzle = QAction('Solve Puzzle', self)
        openOptions = QAction('Hints', self)
        puzzleMenu.addAction(solvePuzzle)
        puzzleMenu.addAction(clear)
        puzzleMenu.addAction(startOver)
        optionMenu.addAction(openOptions)
        generateMenu.addAction(generateVEasyDifficulty)
        generateMenu.addAction(generateEasyDifficulty)
        generateMenu.addAction(generateMedDifficulty)
        generateMenu.addAction(generateHardDifficulty)
        generateMenu.addAction(generateVHardDifficulty)
        generateMenu.addAction(generateImpossibleDifficulty)
        optionMenu.addAction(openOptions)

        generateVEasyDifficulty.triggered.connect(self.generateVEasyPuzzle)
        generateEasyDifficulty.triggered.connect(self.generateEasyPuzzle)
        generateMedDifficulty.triggered.connect(self.generateMedPuzzle)
        generateHardDifficulty.triggered.connect(self.generateHardPuzzle)
        generateVHardDifficulty.triggered.connect(self.generateVHardPuzzle)
        generateImpossibleDifficulty.triggered.connect(self.generateImpossiblePuzzle)
        solvePuzzle.triggered.connect(self.solveCurrentPuzzle)
        clear.triggered.connect(self.clearBoard)
        startOver.triggered.connect(self.clearAnswers)

        openOptions.triggered.connect(self.openOptions)

        puzzleMenu.addMenu(generateMenu)

        self.solving = False





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
        self.makingPuzzle = True
        self.clearBoard()
        for i in range(9):
            for j in range(9):
                if(puzzle.board[i][j]['val'] != ' '):
                    self.boxes[i][j].setText(str(puzzle.board[i][j]['val']))
        self.setSquareValues()
        self.makingPuzzle = False

    def clearBoard(self):
        for row in self.boxes:
            for content in row:
                content.setText("")
                content.setEnabled(True)
        
    def clearAnswers(self):
        for row in self.boxes:
            for content in row:
                if(content.isEnabled()):
                    content.setText("")
    
    def checkSolution(self):
        numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
        message = QMessageBox()
        message.setStandardButtons(QMessageBox.Ok)
        message.buttonClicked.connect(self.clearHighlights)
        finished = True
        for i in range(9):
            for j in range(9):
                text = self.boxes[i][j].text()
                if(text not in numbers):
                    finished = False
                else:
                        self.puzzle.board[i][j]['val'] = int(text)

        self.activeCheck()
        
        if(finished):
            if(self.puzzle.colCheck() and self.puzzle.rowCheck() and self.puzzle.sectorCheck()):
                message.setText('Your solution was correct! Congrats!')
                message.exec_()
            else: 
                message.setText('Sorry, that solution is not correct.')
                message.exec_()
        else:
            message.setText('The solution you submitted as invalid!\nLook through it to see what went wrong.')
            message.exec_()

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

    def openOptions(self):
        print(self.optionsMenu.title)
        self.optionsMenu.openMenu()
        self.setEnabled(False)
    
    def solveCurrentPuzzle(self):
        self.solving = True
        self.puzzle.intelligentSolve()
        if(self.optionsMenu.instantSolve):
            for i in range(9):
                for j in range(9):
                    self.boxes[i][j].setText(str(self.puzzle.board[i][j]['val']))
            self.solving = False
        else:
            self.timer = QTimer(self)
            self.counter = 0
            self.timer.timeout.connect(self.onTimeout)
            self.timer.start(400)

    def onTimeout(self):
        if(self.counter >= len(self.puzzle.eventStack)):
            self.sovling = False
            self.clearHighlights()
            self.timer.stop()
        else:
            guessFlag = False
            square = self.puzzle.eventStack[self.counter]
            print(square)
            if(square[0] == 'remove'):
                self.boxes[square[2]][square[3]].setText(str(" "))
                self.changeHighlights('red', square[2],square[3])
            elif(square[0] == 'exclusive' and  not guessFlag):
                self.boxes[square[2]][square[3]].setText(str(square[1]))
                self.changeHighlights('green', square[2],square[3])
            elif(square[0] == 'exclusive' and guessFlag):
                self.boxes[square[2]][square[3]].setText(str(square[1]))
                self.changeHighlights('yellow', square[2],square[3])
            elif(square[0] == 'guess'):
                self.guessFlag = True
                self.boxes[square[2]][square[3]].setText(str(square[1]))
                self.changeHighlights('orange', square[2],square[3])
            elif(square[0] == 'bad guess'):
                self.guessFlag = False
                self.boxes[square[2]][square[3]].setText(str(square[1]))
                self.changeHighlights('red', square[2],square[3])
            self.counter += 1

    def changeHighlights(self, color, x, y):
        cell = self.boxes[x][y]
        if(color == 'clear'):
            cell.setStyelSheet("")
        elif(color == 'red'):
            cell.setStyleSheet('''
                QLineEdit {
            border: 2px solid rgb(63, 63, 63);
            color: rgb(255, 255, 255);
            background-color: rgb(255, 0, 0);
            }
                            ''')
        elif(color == 'yellow'):
            cell.setStyleSheet('''
                QLineEdit {
            border: 2px solid rgb(63, 63, 63);
            color: rgb(255, 255, 255);
            background-color: rgb(255, 255, 0);
            }
                            ''')

        elif(color == 'green'):
            cell.setStyleSheet('''
                QLineEdit {
            border: 2px solid rgb(63, 63, 63);
            color: rgb(255, 255, 255);
            background-color: rgb(0, 255, 0);
            }
                            ''')
        elif(color == 'orange'):
            cell.setStyleSheet('''
                QLineEdit {
            border: 2px solid rgb(63, 63, 63);
            color: rgb(255, 255, 255);
            background-color: rgb(255, 165, 0);
            }
                            ''')
        

    def clearHighlights(self):
        for row in self.boxes:
            for cell in row:
                cell.setStyleSheet("")

    def passiveCheck(self):
        if(self.optionsMenu.passiveChecking):
            remove = []
            for i in range(9):
                for j in range(9):
                    remove += self.puzzle.findRowConfliction(i, j) + self.puzzle.findColConfliction(i, j) + self.puzzle.findSectorConfliction(i, j) 
                    
            for i in range(9):
                for j in range(9):                 
                    if([i,j] not in remove):
                        cell = self.boxes[i][j]
                        cell.setStyleSheet("")
            self.highlight(remove)

    def activeCheck(self):
        if(self.optionsMenu.activeChecking and not self.optionsMenu.passiveChecking):
            remove = []
            for i in range(9):
                for j in range(9):
                    remove += self.puzzle.findRowConfliction(i, j) + self.puzzle.findColConfliction(i, j) + self.puzzle.findSectorConfliction(i, j) 
                    
            for i in range(9):
                for j in range(9):                 
                    if([i,j] not in remove):
                        cell = self.boxes[i][j]
                        cell.setStyleSheet("")
            self.highlight(remove)

    def highlight(self,wrong):
        for coords in wrong:
            cell = self.boxes[coords[0]][coords[1]]
            if(cell.isEnabled()):
                cell.setStyleSheet('''
                QLineEdit {
            border: 2px solid rgb(63, 63, 63);
            color: rgb(255, 255, 255);
            background-color: rgb(255, 100, 100);
            }
                                ''')
            else:
                cell.setStyleSheet('''
                QLineEdit {
            border: 2px solid rgb(63, 63, 63);
            color: rgb(255, 255, 255);
            background-color: rgb(150, 0, 0);
            }
                                ''')

    def setInputasValue(self):
        numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
        if(not self.makingPuzzle and not self.solving):
            for x in range(9):
                for y in range(9):
                    cell = self.boxes[x][y]
                    ans = cell.text()
                    if(ans in numbers):
                        self.puzzle.board[x][y]['val'] = int(ans)
                    else:
                        self.puzzle.board[x][y]['val'] = ' '


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

