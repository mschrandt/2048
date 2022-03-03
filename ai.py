import model
import copy
import multiprocessing as mp

INF = 2**64
PERFECT_SNAKE = [[2,   2**2, 2**3, 2**4],
                [2**8, 2**7, 2**6, 2**5],
                [2**9, 2**10,2**11,2**12],
                [2**16,2**15,2**14,2**13]]

def snakeHeuristic(board):
    h = 0
    for i in range(board.boardSize):
        for j in range(board.boardSize):
            h += board[i][j] * PERFECT_SNAKE[i][j]

    return h

def getNextBestMoveExpectiminimax(board, pool, depth = 2):

    bestScore = -INF
    bestNextMove = model.directions[0]
    results = []
    for dir in model.directions:
        simBoard = copy.deepcopy(board)
        score, validMove = simBoard.move(dir, False)
        if not validMove:
            continue
        results.append(pool.apply_async(expectiminimax, (simBoard, depth, dir)))

    results = [res.get() for res in results]

    for res in results:
        if res[0] >= bestScore:
            bestScore = res[0]
            bestNextMove = res[1]

    return bestNextMove


def expectiminimax(board, depth, dir = None):
    if board.checkLoss():
        return -INF,dir
    elif depth < 0:
        return snakeHeuristic(board),dir

    a = 0
    if depth != int(depth):
        # Player's turn, pick max
        a = -INF
        for dir in model.directions:
            simBoard = copy.deepcopy(board)
            score, hadMovement = simBoard.move(dir, False)
            if hadMovement:
                res = expectiminimax(simBoard, depth-0.5, dir)[0]
                if res > a: a = res
    elif depth == int(depth):
        # Nature's turn, calc average
        a = 0
        openTiles = board.getOpenTiles()
        for addTileLoc in openTiles:
            board.addTile(addTileLoc, 2)
            a += 1.0/len(openTiles)*expectiminimax(board, depth - 0.5, dir)[0]
            #a += 1.0/len(openTiles)*0.9*expectiminimax(board, depth - 0.5, dir)[0]
            #board.addTile(addTileLoc, 4)
            #a += 1.0/len(openTiles)*0.1*expectiminimax(board, depth - 0.5, dir)[0]
            board.addTile(addTileLoc, 0)
    return (a, dir)
