import os
import json
import csv
import time
def get_time():
    return time.time()


board = [["🌑","🌑","🌑","🌑","🌑","🌑","🌑","🌑","🌑","🌑","🌑","🌑"],["🌑","🌑","🌑","🌑","🌑","🌑","🌑","🌑","🌑","🌑","🌑","🌑"],["🌑","🌑","🌑","🌑","🌑","🌑","🌑","🌑","🌑","🌑","🌑","🌑"],["🌑","🌑","🌑","🌑","🌑","🌑","🌑","🌑","🌑","🌑","🌑","🌑"],["🌑","🌑","🌑","🌑","🌑","🌑","🌑","🌑","🌑","🌑","🌑","🌑"],["🌑","🌑","🌑","🌑","🌑","🌑","🌑","🌑","🌑","🌑","🌑","🌑"],["🌑","🌑","🌑","🌑","🌑","🌑","🌑","🌑","🌑","🌑","🌑","🌑"],["🌑","🌑","🌑","🌑","🌑","🌑","🌑","🌑","🌑","🌑","🌑","🌑"],["🌑","🌑","🌑","🌑","🌑","🌑","🌑","🌑","🌑","🌑","🌑","🌑"],["🌑","🌑","🌑","🌑","🌑","🌑","🌑","🌑","🌑","🌑","🌑","🌑"],["🌑","🌑","🌑","🌑","🌑","🌑","🌑","🌑","🌑","🌑","🌑","🌑"],["🌑","🌑","🌑","🌑","🌑","🌑","🌑","🌑","🌑","🌑","🌑","🌑"]]
p1 = "💀"
cpu = "😡"
direc = [1,-1]


def disBoard(b):
    c=0
    new = ["XX.","🅐 ","🅑 ","🅒 ","🅓 ","🅔 ","🅕 ","🅖 ","🅗 ","🅘 ","🅙 ","🅚 ","🅛 ","\n"]
    for i in b:
        new.append(("0" if len(str(c+1))==1 else "1" ) + str(c+1)[-1])
        for o in i:
            new.append(o)
        new.append("\n")
        c+=1
    print("".join(new)+f"Board Eval for {cpu}: {str(evaluate(b))}")


def makemovep(ba,move):
    while True:
        try:
            a = move[:1].upper()
            a = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"].index(a)
            b = int(move[1:])-1
            ba[b][a] = p1
            break
        except:
            move = input("Enter a valid move (e.g. a1): ")
    return disBoard(ba)

def checkwin(b):
    directions = [(0, 1), (1, 0), (1, 1), (-1, 1)]
    for row in range(12):
        for col in range(12):
            for dr, dc in directions:
                count = 1
                r, c = row + dr, col + dc
                while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == board[row][col] and board[r][c] != "🌑":
                    count += 1
                    r += dr
                    c += dc
                r, c = row - dr, col - dc
                while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == board[row][col] and board[r][c] != "🌑":
                    count += 1
                    r -= dr
                    c -= dc
                if count >= 5:
                    print(f"{board[row][col]} WINS!!")
                    quit()
                else:
                    pass

def checkwineval(board):
    directions = [(0, 1), (1, 0), (1, 1), (-1, 1)]
    for row in range(12):
        for col in range(12):
            for dr, dc in directions:
                count = 1
                r, c = row + dr, col + dc
                while 0 <= r < 12 and 0 <= c < 12 and board[r][c] == board[row][col] and board[r][c] != "🌑":
                    count += 1
                    if count >= 5:
                        print(f"{board[row][col]} WINS!!")
                        return board[row][col]
                    r += dr
                    c += dc
                r, c = row - dr, col - dc
                while 0 <= r < 12 and 0 <= c < 12 and board[r][c] == board[row][col] and board[r][c] != "🌑":
                    count += 1
                    if count >= 5:
                        print(f"{board[row][col]} WINS!!")
                        return board[row][col]
                    r -= dr
                    c -= dc
    return "ongoing"


def is_board_full(board):
    for i in board:
        for n in i:
            if n == "🌑":
                return False
    return True

def evaluate_pattern(board, row, col, dr, dc, player):
    pattern_score = 0
    pattern_length = 0
    r, c = row, col

    while 0 <= r < 12 and 0 <= c < 12 and board[r][c] == player:
        pattern_length += 1
        r += dr
        c += dc

        pattern_score += pattern_length**pattern_length  # Give higher score for longer patterns

    return pattern_score

def evaluate(board):
    result = checkwineval(board)
    evalscore = 0
    
    if result == "💀":
        return -99999999999999
    elif result == "😡":
        return 99999999999999
    elif is_board_full(board):
        return 0
    else:
        directions = [(0, 1), (1, 0), (1, 1), (-1, 1)]
        for row in range(12):
            for col in range(12):
                for dr, dc in directions:
                    bad = evaluate_pattern_count(board, row, col, dr, dc, "💀") * 1.1
                    evalscore -= bad * bad

                    good = evaluate_pattern_count(board, row, col, dr, dc, "😡")
                    evalscore += good * good

                    pbcount = evaluate_pattern_count(board, row, col, dr, dc, "😡", "💀")
                    evalscore += pbcount ** bad

                    pacount = evaluate_pattern_count(board, row, col, dr, dc, "💀", "😡") * 4
                    evalscore -= pacount * good

                    ptcount = evaluate_pattern_count(board, row, col, dr, dc, "😡", "💀") * 4
                    evalscore += ptcount * good

                    r, c = row - dr, col - dc
                    distance_to_edge = min(r, c, 11 - r, 11 - c)

                    if 0 <= r < 12 and 0 <= c < 12 and board[r][c] == "😡" and board[row][col] == "💀":
                        evalscore += bad * bad

                    if 0 <= r < 12 and 0 <= c < 12 and (board[r][c] != "🌑" or board[r][c] != "😡") and board[row][col] == "😡":
                        r += dr
                        c += dc
                        if distance_to_edge < 20:
                            evalscore -= bad * bad
                
    return evalscore-576

def evaluate_pattern_count(board, row, col, dr, dc, player, opponent=None):
    count = 0
    r, c = row, col

    while 0 <= r < 12 and 0 <= c < 12 and board[r][c] == player:
        count += 1
        r += dr
        c += dc

    if opponent:
        r, c = row - dr, col - dc
        while 0 <= r < 12 and 0 <= c < 12 and board[r][c] == opponent:
            count += 1
            r -= dr
            c -= dc

    return count



def negamax(board, depth, player, alpha, beta):
    score = evaluate(board)

    if depth == 0 or abs(score) > 9999:
        return 9999999999999999999

    legal_moves = get_sorted_legal_moves(board)
    legal_moves = legal_moves[:max(1, int(len(legal_moves) * 0.1))]

    if player == '💀':
        min_eval = float('inf')
        for move in legal_moves:
            i, j = move
            board[i][j] = '💀'
            eval_score = -negamax(board, depth - 1, "😡", -beta, -alpha)
            os.system('cls||clear') #1111111111111111111111111111111111111111111111111111111111
            disBoard(board) #11111111111111111111dd11111111111111111111111111111111111111111111
            board[i][j] = '🌑'
            min_eval = min(min_eval, eval_score)
            beta = min(beta, eval_score)
            if alpha >= beta:
                break
        # print(f"Time elapsed: {get_time()-then}s")
        return min_eval
    elif player == "😡":
        max_eval = float('-inf')
        for move in legal_moves:
            i, j = move
            board[i][j] = "😡"
            eval_score = -negamax(board, depth - 1, '💀', -beta, -alpha)
            os.system('cls||clear') #111111111111111111111111#11111111111111111111dd11111111111
            disBoard(board) #11111111111111111111dd11111111111111111111111111111111111111111111
            board[i][j] = '🌑'
            max_eval = max(max_eval, eval_score)
            alpha = max(alpha, eval_score)
            if alpha >= beta:
                break
        # print(f"Time elapsed: {get_time()-then}s")
        return max_eval

    

def get_legal_moves(board):
    legal_moves = [(i, j) for i in range(12) for j in range(12) if board[i][j] == '🌑']
    return legal_moves

def get_sorted_legal_moves(board):
    legal_moves = [(i, j) for i in range(12) for j in range(12) if board[i][j] == '🌑']
    # Sort the legal moves based on a heuristic evaluation
    sorted_moves = sorted(legal_moves, key=lambda move: evaluate_after_move(board, move), reverse=True)
    return sorted_moves
    
    
def cpumove(board, depth, player):

    ordered_moves = get_sorted_legal_moves(board)
    best_value = float('-inf')
    best_move = None

    for move in ordered_moves[:max(1,int(len(ordered_moves)*0.1))]:
        i, j = move
        board[i][j] = player
        move_value = negamax(board, depth, cpu, float('-inf'), float('inf'))
        print(move_value)
        board[i][j] = '🌑'  
        if move_value > best_value:
            best_value = move_value
            best_move = move
            return best_move
        else: return move

    return best_move

def evaluate_after_move(board, move):
    i, j = move
    board[i][j] = "😡"
    score = evaluate(board)
    board[i][j] = '🌑'
    return score




  