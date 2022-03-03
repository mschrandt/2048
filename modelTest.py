import model
import random

board = model.Board()
print(board)
input('Press enter to continue...')

print('Moving left...')
board.move(model.LEFT)
print(board)
input('Press enter to continue...')

print('Moving up...')
board.move(model.UP)
print(board)
input('Press enter to continue...')

print('Moving right...')
board.move(model.RIGHT)
print(board)
input('Press enter to continue...')

print('Moving down...')
board.move(model.DOWN)
print(board)
input('Press enter to continue...')

print('Playing game randomly until lost...')
while not board.checkLoss():
    board.move(random.choice(model.directions))
print(board)
print('Final score: {}'.format(board.score))
