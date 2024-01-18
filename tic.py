import sys
sys.setrecursionlimit(2147483647)

import ticlib
board = ticlib.board
ticlib.disBoard(board)

import time
def get_time():
    return time.time()

while True:
    #PLAYER INPUT
    ticlib.makemovep(board,input("Make move: "))
    ticlib.checkwin(board)


    #CPU INPUT
    #print(len(ticlib.get_sorted_legal_moves(board)))
    then = get_time()
    move = ticlib.cpumove(board,3,ticlib.cpu)
    board[move[0]][move[1]] = ticlib.cpu
    ticlib.disBoard(board)
    ticlib.checkwin(board)
    print(f"Time elapsed: {int(get_time()-then)}s")
    

#os.system('cls||clear') #111111111111111111111111
            #disBoard(board) #11111111111111111111dddf
    
'''while True:
    #PLAYER INPUT
    then = get_time()
    move = ticlib.cpumove(board,1,ticlib.p1)
    board[move[0]][move[1]] = ticlib.p1
    ticlib.disBoard(board)
    ticlib.checkwin(board)
    print(f"Time elapsed: {int(get_time()-then)}s")


    #CPU INPUT
    #print(len(ticlib.get_sorted_legal_moves(board)))
    then = get_time()
    move = ticlib.cpumove(board,1,ticlib.cpu)
    board[move[0]][move[1]] = ticlib.cpu
    ticlib.disBoard(board)
    ticlib.checkwin(board)
    print(f"Time elapsed: {int(get_time()-then)}s")'''