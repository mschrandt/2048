from random import random, choice
LEFT = (0, -1)
RIGHT = (0, 1)
UP = (-1, 0)
DOWN = (1, 0)
directions = [LEFT, UP, RIGHT, DOWN]

class Board:

    def __init__(self, boardSize = 4):
        self.boardSize = boardSize
        self.board = [[0]*boardSize for i in range(boardSize)]
        self.score = 0
        self.addTile()
        self.addTile()
    def __str__(self):
        outStr = ''
        for i in self.board:
            outStr += '\t'.join(map(str,i))
            outStr += '\n'
        return outStr

    def __getitem__(self, key):
        return self.board[key]

    # Return list of tuples containing indexes of open tiles
    def getOpenTiles(self):
        openTiles = []
        for i in range(self.boardSize):
            for j in range(self.boardSize):
                if self.board[i][j] == 0:
                    openTiles.append((i,j))
        return openTiles

    # Add a random tile to the board
    # Throws exception if board is full
    # 90% - 2
    # 10% - 4
    def addTile(self, pos = None, tileToAdd = 0):
        if pos == None:
            openTiles = self.getOpenTiles()
            if len(openTiles) == 0:
                raise Exception("Unable to add tile, board is full")
            pos = choice(openTiles)

        if tileToAdd == 0:
            if random() < 0.9:
                tileToAdd = 2
            else:
                tileToAdd = 4

        self.board[pos[0]][pos[1]] = tileToAdd

    # Slide all tiles towards direction, combining tiles that slide into eachother
    # dir: tuple containing x,y modifier to move towards
    # Returns sum of newly combined tiles
    def move(self,dir,addNextTile=True):
        hadCollision = [[False]*self.boardSize for i in range(self.boardSize)]
        hadMovement = False
        score = 0

        xStart = 0
        xEnd = self.boardSize
        if dir[1] > 0:
            xStart = self.boardSize - 1
            xEnd = -1

        yStart = 0
        yEnd = self.boardSize
        if dir[0] > 0:
            yStart = self.boardSize - 1
            yEnd = -1
        for y in range(yStart, yEnd, -dir[0] if dir[0] != 0 else 1):
            for x in range(xStart, xEnd, -dir[1] if dir[1] != 0 else 1):
                if self.board[y][x] == 0:
                    continue

                yCheck = y + dir[0]
                xCheck = x + dir[1]

                while yCheck >= 0 and yCheck < self.boardSize \
                    and xCheck >= 0 and xCheck < self.boardSize \
                    and self.board[yCheck][xCheck] == 0:
                    yCheck += dir[0]
                    xCheck += dir[1]
                # Move back if we went out of bounds
                if yCheck < 0 or yCheck >= self.boardSize \
                    or xCheck < 0 or xCheck >= self.boardSize:
                    yCheck -= dir[0]
                    xCheck -= dir[1]
                # If no movement, break
                if yCheck == y and xCheck == x:
                    continue
                elif self.board[y][x] == self.board[yCheck][xCheck] and not hadCollision[yCheck][xCheck]:
                    # else If Equal and not combined already, combine
                    hadCollision[yCheck][xCheck] = True
                    hadMovement = True
                    self.board[yCheck][xCheck] += self.board[y][x]
                    score += self.board[yCheck][xCheck]
                    self.board[y][x] = 0
                elif self.board[yCheck][xCheck] == 0:
                    # else if movement into empty tile, simply move
                    hadMovement = True
                    self.board[yCheck][xCheck] = self.board[y][x]
                    self.board[y][x] = 0
                else:
                    # Else, move back
                    yCheck -= dir[0]
                    xCheck -= dir[1]
                    if yCheck == y and xCheck == x:
                        continue
                    hadMovement = True
                    temp = self.board[y][x]
                    self.board[y][x] = 0
                    self.board[yCheck][xCheck] = temp
        self.score += score
        if hadMovement and addNextTile:
            self.addTile()
        return score, hadMovement

    # Returns True if no legal moves exist
    def checkLoss(self):
        for y in range(self.boardSize):
            for x in range(self.boardSize):
                if self.board[y][x] == 0:
                    return False
                for dir in directions:
                    if y + dir[0] >= 0 and y + dir[0] < self.boardSize \
                        and x + dir[1] >= 0 and x + dir[1] < self.boardSize \
                        and self.board[y][x] == self.board[y+dir[0]][x+dir[1]]:
                        return False
        return True
