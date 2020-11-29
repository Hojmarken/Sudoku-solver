def printSudoku(sudoku):
    for array in sudoku:
        print(" ".join(map(str, array)))


def placeNum(num, x, y, sudoku, notes):
    sudoku[y][x] = num
    notes[y][x] = []
    updateNotes(x, y, sudoku, notes)


def isOnlyHori(num, x, y, notes):
    for i in range(9):
        if i == x:
            continue
        if len(notes[y][i]) > 0:
            if notes[y][i][num - 1]:
                return False
    return True


def isOnlyVerti(num, x, y, notes):
    for i in range(9):
        if i == y:
            continue
        if len(notes[i][x]) > 0:
            if notes[i][x][num - 1]:
                return False
    return True


def isOnlySquare(num, x, y, notes):
    squarePos = [x // 3, y // 3]
    for xOff in range(3):
        for yOff in range(3):
            curY = squarePos[1] * 3 + yOff
            curX = squarePos[0] * 3 + xOff
            if len(notes[curY][curX]) > 0:
                if notes[curY][curX][num - 1]:
                    return False
    return True


def isGuaranteedPlacement(num, x, y, notes):
    return isOnlyHori(num, x, y, notes) or isOnlyVerti(num, x, y, notes) or isOnlySquare(num, x, y, notes)


def simpleSolve(sudoku, notes):
    doAgain = True
    while doAgain:
        doAgain = False
        for y in range(9):
            for x in range(9):
                for i, possible in enumerate(notes[y][x]):
                    if possible and isGuaranteedPlacement(i + 1, x, y, notes):
                        placeNum(i + 1, x, y, sudoku, notes)
                        doAgain = True


def updateNotes(x, y, sudoku, notes):
    num = sudoku[y][x]
    for i in range(9):
        if len(notes[y][i]) > 0:
            notes[y][i][num - 1] = False
        if len(notes[i][x]) > 0:
            notes[i][x][num - 1] = False
    squarePos = [x // 3, y // 3]
    for xOff in range(3):
        for yOff in range(3):
            curY = squarePos[1] * 3 + yOff
            curX = squarePos[0] * 3 + xOff
            if len(notes[curY][curX]) > 0:
                notes[curY][curX][num - 1] = False


def createNotes(sudoku):
    notes = [[[] for j in range(9)] for i in range(9)]
    for y in range(9):
        for x in range(9):
            if sudoku[y][x] == 0:
                notes[y][x] = [True for i in range(9)]
    for y in range(9):
        for x in range(9):
            if sudoku[y][x] != 0:
                updateNotes(x, y, sudoku, notes)
    return notes


def notCompleted(sudoku):
    for array in sudoku:
        for e in array:
            if e == 0:
                return True
    return False


def getPosWithMostClues(notes):
    min = float("inf")
    pos = [0, 0]
    for x in range(9):
        for y in range(9):
            if len(notes[y][x]) > 0:
                amount = notes[y][x].count(True)
                if amount < min:
                    min = amount
                    pos = [x, y]
                    if min == 2:
                        return pos
    return pos


def isInvalid(sudoku, notes):
    for x in range(9):
        for y in range(9):
            if sudoku[y][x] == 0 and notes[y][x].count(False) == 9:
                return True
    return False


def getBestGuess(notes):
    pos = getPosWithMostClues(notes)
    num = 0
    for i, e in enumerate(notes[pos[1]][pos[0]]):
        if e:
            num = i + 1
            break
    return [num] + pos


def solveSudoku(sudoku, notes):
    simpleSolve(sudoku, notes)
    if notCompleted(sudoku):
        if isInvalid(sudoku, notes):
            return None
        else:
            guess = getBestGuess(notes)
            branchSudoku = [e[:] for e in sudoku]
            branchNotes = [[e[:] for e in array] for array in notes]
            placeNum(guess[0], guess[1], guess[2], branchSudoku, branchNotes)
            branch = solveSudoku(branchSudoku, branchNotes)
            if branch == None:
                notes[guess[2]][guess[1]][guess[0] - 1] = False
                return solveSudoku(sudoku, notes)
            else:
                return branch
    else:
        return sudoku


def checkSolution(sudoku):
    for i in range(9):
        hori = set()
        verti = set()
        for j in range(9):
            if 0 >= sudoku[j][i] or 9 < sudoku[j][i] or sudoku[j][i] in verti:
                return False
            else:
                verti.add(sudoku[j][i])
            if sudoku[i][j] in hori:
                return False
            else:
                hori.add(sudoku[i][j])
    for xSq in range(3):
        for ySq in range(3):
            square = set()
            for x in range(3):
                for y in range(3):
                    if sudoku[ySq * 3 + y][xSq * 3 + x] in square:
                        return False
                    else:
                        square.add(sudoku[ySq * 3 + y][xSq * 3 + x])
    return True


grid = [
    [0, 0, 0, 0, 0, 2, 0, 0, 0],
    [8, 9, 0, 7, 0, 0, 0, 0, 4],
    [0, 0, 0, 0, 3, 4, 6, 5, 0],
    [4, 7, 0, 0, 8, 0, 0, 0, 0],
    [0, 0, 8, 0, 0, 0, 3, 0, 0],
    [0, 0, 0, 0, 2, 0, 0, 1, 7],
    [0, 5, 7, 6, 9, 0, 0, 0, 0],
    [9, 0, 0, 0, 0, 3, 0, 6, 5],
    [0, 0, 0, 1, 0, 0, 0, 0, 0]
]

printSudoku(grid)
print()
printSudoku(solveSudoku([array[:] for array in grid], createNotes(grid)))
