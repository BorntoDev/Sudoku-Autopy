import autopy
import time

boardPosX = 917
boardPosY = 430
boardWidth = 370
boardHeight = 370

sudoku = []
for i in range(9):
    sudoku.append([0, 0, 0, 0, 0, 0, 0, 0, 0])

boardBitmap = autopy.bitmap.capture_screen()

pointerX = boardPosX
pointerY = boardPosY
boxsize = boardWidth//9

def fillSudoku(number,pos):
    x = (pos[0]-boardPosX)//boxsize
    y = (pos[1]-boardPosY)//boxsize
    sudoku[int(y)][int(x)] = number

def findNextCellToFill(sudoku):
    for x in range(9):
        for y in range(9):
            if sudoku[x][y] == 0:
                return x, y
    return -1, -1

def isValid(sudoku, i, j, e):
    rowOk = all([e != sudoku[i][x] for x in range(9)])
    if rowOk:
        columnOk = all([e != sudoku[x][j] for x in range(9)])
        if columnOk:
            secTopX, secTopY = 3*(i//3), 3*(j//3)
            for x in range(secTopX, secTopX+3):
                for y in range(secTopY, secTopY+3):
                    if sudoku[x][y] == e:
                        return False
            return True
    return False

def solveSudoku(sudoku, i=0, j=0):
    i, j = findNextCellToFill(sudoku)
    if i == -1:
        return True

    for e in range(1, 10):
        if isValid(sudoku, i, j, e):
            sudoku[i][j] = e
            if solveSudoku(sudoku, i, j):
                return True
            sudoku[i][j] = 0
    return False

def insertNumber(number, x, y):
    boxX = boardPosX + boxsize * x + 20
    boxY = boardPosY + boxsize * y + 20
    autopy.mouse.smooth_move(boxX,boxY)
    autopy.mouse.click()
    autopy.mouse.click()
    autopy.key.type_string(str(number))

def fastInsertNumber(number, x, y):
    boxX = boardPosX + boxsize * x + 20
    boxY = boardPosY + boxsize * y + 20
    autopy.mouse.move(boxX,boxY)
    time.sleep(0.005)
    autopy.mouse.click()
    autopy.key.type_string(str(number))

def searchNumber():
    print("loading")
    for i in range(1,10):
        print(".")
        number = autopy.bitmap.Bitmap.open(str(i)+'.png')
        x = boardBitmap.find_every_bitmap(number,0.52,((boardPosX,boardPosY),(boardWidth,boardHeight)))
        for pos in x:
            fillSudoku(i,pos)
    print(" Done!")

def printSudoku():
    print("=======================")
    for row in sudoku:
        print(*row)

def insertSudoku():
    for i in range(9):
        for j in range(9):
            insertNumber(sudoku[i][j],j,i)
            #fastInsertNumber(sudoku[i][j],j,i)

searchNumber()
printSudoku()
solveSudoku(sudoku)
printSudoku()
insertSudoku()
