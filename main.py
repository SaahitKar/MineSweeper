#Saahit Karumuri

import random
import re

class Board:
    def __init__(self, minsize, bombsmax):
        self.minsize = minsize
        self.bombsmax = bombsmax
        self.board = self.makenb()
        self.valstob()
        self.dug = set()

    def valstob(self):
        for r in range(self.minsize):
            for c in range(self.minsize):
                if self.board[r][c] == '*':
                    continue
                self.board[r][c] = self.neighborbn(r, c)

    def neighborbn(self, row, col):
        numBombs = 0
        for r in range(max(0, row - 1), min(self.minsize - 1, row + 1) +1):
            for c in range(max(0, col -1), min(self.minsize -1, col + 1) +1):
                if r == row and c == col:
                    continue
                if self.board[r][c] == '*':
                    numBombs += 1
        
        return numBombs

    def makenb(self):
        board = [[None for _ in range(self.minsize)] for _ in range(self.minsize)]
        plantB = 0
        while plantB < self.bombsmax:
            loc = random.randint(0, self.minsize**2-1)
            row = loc // self.minsize
            col = loc % self.minsize
            if board[row][col] == '*':
                continue
            
            board[row][col] = '*'
            plantB += 1
        return board

    def dig(self, row, col):
        self.dug.add((row, col))
        if self.board[row][col] == '*':
            return False
        elif self.board[row][col] > 0:
            return True
        for r in range(max(0, row - 1), min(self.minsize - 1, row + 1) +1):
            for c in range(max(0, col -1), min(self.minsize -1, col + 1) +1):
                if (r, c) in self.dug:
                    continue
                self.dig(r, c)
        return True

    def __str__(self):
        visible_board = [[None for _ in range(self.minsize)] for _ in range(self.minsize)]
        for row in range(self.minsize):
            for col in range(self.minsize):
                if (row, col) in self.dug:
                    visible_board[row][col] = str(self.board[row][col])
                else:
                    visible_board[row][col] = ' '
        strrep = ''
        widths = []
        for idx in range(self.minsize):
            columns = map(lambda x: x[idx], visible_board)
            widths.append(
                len(
                    max(columns, key = len)
                )
            )

        index = [i for i in range(self.minsize)]
        index_row = '   '
        arr = []
        for idx, col in enumerate(index):
            format = '%-' + str(widths[idx]) + "s"
            arr.append(format % (col))
        index_row += '  '.join(arr)
        index_row += '  \n'
        
        for i in range(len(visible_board)):
            row = visible_board[i]
            strrep += f'{i} |'
            arr = []
            for idx, col in enumerate(row):
                format = '%-' + str(widths[idx]) + "s"
                arr.append(format % (col))
            strrep += ' |'.join(arr)
            strrep += ' |\n'

        str_len = int(len(strrep) / self.minsize)
        strrep = index_row + '-'*str_len + '\n' + strrep + '-'*str_len

        return strrep
 

def play(minsize = 10, bombsmax = 10):
    board = Board(minsize, bombsmax)
    safe = True
    
    while len(board.dug) < board.minsize**2 - bombsmax:
        print(board)
        isValid = False

        while isValid == False:
            try:
                user_input = re.split(',(\\s)*', input("Where will you dig? R,C >>> "))
                row, col = int(user_input[0]), int(user_input[-1])
                isValid = True
            except:
                print('\nPosition was entered incorrectly.')
                continue     

        if row < 0 or row >= board.minsize or col < 0 or col > board.minsize:
            print('\nPosition is outside of bounds. Please re-enter position >>> \n')
            continue
        safe = board.dig(row, col)
        if not safe:
            break
    if safe:
        print('\nCONGRATULATIONS!!! YOU CLEARED ALL THE MINES!')
    else:
        print('\nBOOM!!! SORRY GAME OVER...')
        board.dug = [(r, c) for r in range(board.minsize) for c in range(board.minsize)] 
        print(board)

if __name__ == '__main__':
    play()
