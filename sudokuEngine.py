import copy
import random

class sudokuPuzzle():

    def __init__(self, given = None):
        self.board = None
        if(given is None):
            sudokuRow = ["" for i in range(9)]
            self.board = [copy.deepcopy(sudokuRow) for i in range(9)]
        else:
            self.board = given
        
        self.board = self.initPuzzle(self.board)

    def initPuzzle(self, board):
        baseCell = {
            'val' : None,
            'type' : 'empty',
            'possible' : set([]),
            'excluded' : set([]),
        }

        baseRow = [copy.deepcopy(baseCell) for i in range(9)]
        basePuzzle = [copy.deepcopy(baseRow) for i in range(9)]

        for i in range(9):
            for j in range(9):
                if(board[i][j] != ""):
                    basePuzzle[i][j]['val'] = int(board[i][j])
                    basePuzzle[i][j]['type'] = 'given'
                else:
                    basePuzzle[i][j]['val'] = " "
                    basePuzzle[i][j]['type'] = 'empty'

        return basePuzzle

    def rowCheck(self):
        passed = True
        checkList = [0]*9
        for row in self.board:
            for cell in row:
                value = cell['val']
                if(value != " " and int(value) < 10 and int(value) > 0):
                    checkList[int(value)-1] += 1

        if(checkList.count(1) != 9):
            return not passed
        else:
            return passed

    def colCheck(self):
        passed = True
        checkList = [0]*9
        for i in range(9):
            for j in range(9):
                value = self.board[i][j]['val']
                if(value != " " and int(value) < 10 and int(value) > 0):
                    checkList[int(value)-1] += 1

        if(checkList.count(1) != 9):
            return not passed
        else:
            return passed

    def sectorCheck(self):
        passed = True
        for h in range(0, 9, 3):
            for i in range(0, 9, 3):
                checkList = [0]*9
                for j in range(3):
                    for k in range(3):
                        value = self.board[h+j][k+i]['val']
                        if(value != " " and int(value) < 10 and int(value) > 0):
                            checkList[int(value)-1] += 1

                if(checkList.count(1) != 9):
                    return not passed
        return passed

    def exclusiveRowSweep(self, x, y):
        cell = self.board[y][x]
        temp = cell['possible']
        for j in range(9):
            if(j != x):
                temp = temp.difference(self.board[y][j])
        return temp

    def exclusiveColSweep(self, x, y):
        cell = self.board[y][x]
        temp = cell['possible']
        for i in range(9):
            if(i != y):
                temp = temp.difference(self.board[i][x])
        return temp

    def exclusiveSectorSweep(self, x, y):
        startX = 0
        startY = 0


        if(x < 3 and y < 3):
            pass
        elif(x < 6 and y < 3):
            startX = 3
        elif(x >= 6 and y < 3):
            startX = 6
        elif(x < 3 and y < 6):
            startY = 3
        elif(x < 6 and y < 6):
            startX = 3
            startY = 3
        elif(x >= 6 and y < 6):
            startX = 6
            startY = 3
        elif(x < 3 and y >= 6):
            startY = 6
        elif(x < 6 and y >= 6):
            startX = 3
            startY = 6
        else:
            startX = 6
            startY = 6

        cell = self.board[x][y]
        temp = cell['possible']
        for i in range(startY, startY+3):
            for j in range(startX, startX+3):
                if(i == y and j == x):
                    pass
                else:
                    temp = temp.difference(self.board[i][j]['possible'])
        return temp

    def findPossibleValuesForRow(self, x, y):
        numbers = set([1, 2, 3, 4, 5, 6, 7, 8, 9])
        present = []
        for j in range(9):
            if(self.board[x][j]['val'] != ' '):
                present.append(self.board[x][j]['val'])

        return numbers - set(present) - self.board[x][y]['excluded']

    def findPossibleValuesForCol(self, x, y):
        numbers = set([1, 2, 3, 4, 5, 6, 7, 8, 9])
        present = []
        for i in range(9):
            if(self.board[i][y]['val'] != " "):
                present.append(self.board[i][y]['val'])

        return numbers - set(present) - self.board[x][y]['excluded']

    def findPossibleValuesForSector(self, x, y):
        startX = 0
        startY = 0


        if(x < 3 and y < 3):
            pass
        elif(x < 6 and y < 3):
            startX = 3
        elif(x >= 6 and y < 3):
            startX = 6
        elif(x < 3 and y < 6):
            startY = 3
        elif(x < 6 and y < 6):
            startX = 3
            startY = 3
        elif(x >= 6 and y < 6):
            startX = 6
            startY = 3
        elif(x < 3 and y >= 6):
            startY = 6
        elif(x < 6 and y >= 6):
            startX = 3
            startY = 6
        else:
            startX = 6
            startY = 6

        numbers = set([1, 2, 3, 4, 5, 6, 7, 8, 9])
        present = []    
        for i in range(startY, startY+3):
            for j in range(startX, startX+3):
                value = self.board[j][i]['val']
                if(value != " "):
                    present.append(value)
        myPossibles = numbers - set(present) - self.board[x][y]['excluded']
        return myPossibles

    def possibleState(self):
        possible = True
        for i in range(9):
            for j in range(9):
                if(len(self.board[i][j]['possible']) == 0 and self.board[i][j]['val'] == ' '):
                    return not possible
        return possible

    def completed(self):
        solved = True
        for i in range(9):
            for j in range(9):
                if(self.board[i][j]['val'] == ' '):
                    return not solved
        return solved

    def findLeastDiverseUnsolvedCell(self):
        x = 0
        y = 0
        minPossibles = 100
        counter = 0
        for i in range(9):
            for j in range(9):
                if(self.board[i][j]['val'] == ' '):
                    counter = len(self.board[i][j]['possible'])
                    if(counter < minPossibles):
                        minPossibles = counter
                        x = i
                        y = j

        return (x, y)

    def updatePossibles(self):
        for i in range(9):
            for j in range(9):
                cell = self.board[i][j]
                if(cell['val'] == ' '):
                    possible = self.findPossibleValuesForCol(i, j) & self.findPossibleValuesForRow(i, j) & self.findPossibleValuesForSector(i, j)
                    cell['possible'] = possible

    def intelligentSolve(self):
        previousStates = []
        gStack = []

        isPossible = True
        progressMade = True

        while(not self.completed() and isPossible):
            while(progressMade):
                progressMade = False
                self.updatePossibles()

                for i in range(9):
                    for j in range(9):
                        if(self.board[i][j]['val'] == ' '):
                            possibleExclusives = self.exclusiveRowSweep(j, i) & self.exclusiveColSweep(j, i) & self.exclusiveSectorSweep(j, i)
                            if(len(possibleExclusives) == 1):
                                self.board[i][j]['val'] = possibleExclusives.pop()
                                self.board[i][j]['possible'].clear()
                                progressMade = True
                
                isPossible = self.possibleState()


                if(not self.completed()):
                    if(self.possibleState()):
                        info = self.findLeastDiverseUnsolvedCell()
                        buffer = copy.deepcopy(self.board)
                        previousStates.append(buffer)
                        x = info[0]
                        y = info[1]
                        guess = self.board[x][y]['possible'].pop()
                        self.board[x][y]['val'] = guess
                        gStack.append([guess, x, y])
                        self.board[x][y]['possible'].clear()
                        progressMade = True

                    elif(len(gStack) > 0):
                        self.board = previousStates.pop()
                        previousGuess = gStack.pop()
                        value = previousGuess[0]
                        x = previousGuess[1]
                        y = previousGuess[2]
                        self.board[x][y]['excluded'].add(value)
                        self.board[x][y]['possible'].discard(value)
                        isPossible = self.possibleState()
                        progressMade = True

                    else:
                        return False
                else:
                    return True

    def createPuzzle(self, difficulty):
        numsToRemove = 0
        if(difficulty == 0): #impossible 17 - 20 values
            numsToRemove = random.randint(60, 64)
        elif(difficulty == 1):  #very hard  21 - 25 values
            numsToRemove = random.randint(55, 59)
        elif(difficulty == 2):  #hard   26 - 35 values
            numsToRemove = random.randint(45, 54)
        elif(difficulty == 3):  #medium 36 - 50 values
            numsToRemove = random.randint(40, 45)
        elif(difficulty == 4):  #easy   51 - 65 values
            numsToRemove = random.randint(34, 39)
        else:                   #very easy  66 - 75 values
            numsToRemove = random.randint(25, 34)

        order = []
        for i in range(9):
            for j in range(9):
                order.append((i,j))
        numsRemoved = 0
        puzzle = self._designPuzzle()
        random.shuffle(order)

        while(numsRemoved < numsToRemove):
            cell = order.pop()
            x = cell[0]
            y = cell[1]
            puzzle[x][y]['val'] = " "
            puzzle[x][y]['type'] = 'empty'
            numsRemoved +=1

        for i in range(9):
            for j in range(9):
                puzzle[i][j]['possible'].clear()

        self.board = puzzle

    def _designPuzzle(self):
        self.updatePossibles()

        numsToPlace = random.randint(17, 20)


        solvable = False
        stableState = None

        tempPuzzle = sudokuPuzzle()

        while(not solvable):
            numsPlaced = 0
            tempPuzzle = sudokuPuzzle()
            tempPuzzle.updatePossibles()
            while(numsPlaced != numsToPlace and tempPuzzle.possibleState()):
                x = random.randint(0, 8)
                y = random.randint(0, 8)
                possibleValues = list(tempPuzzle.board[x][y]['possible'])
                if(len(possibleValues) > 0):
                    stableState = copy.deepcopy(tempPuzzle.board)
                    tempPuzzle.board[x][y]['val'] = possibleValues[random.randint(0, len(possibleValues)-1)]
                    tempPuzzle.board[x][y]['possible'].clear()
                    tempPuzzle.board[x][y]['type'] = 'given'
                    if(tempPuzzle.possibleState()):
                        numsPlaced += 1
                    else:
                        forbidden = tempPuzzle.board[x][y]['val']
                        tempPuzzle.board = stableState
                        tempPuzzle.board[x][y]['excluded'].add(forbidden)

                tempPuzzle.updatePossibles()

            solvable = tempPuzzle.possibleState() and tempPuzzle.intelligentSolve()

        for i in range(9):
            for j in range(9):
                tempPuzzle.board[i][j]['excluded'].clear()


        return tempPuzzle.board