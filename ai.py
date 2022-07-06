LOWEST = -1e7
HIGHEST = 1e7

def com(TTT, XO, depth, alpha, beta):
    game_over, val = terminal_state(TTT)
    if game_over:
        return val+depth, None    
    
    v = HIGHEST
    turn = False
    if not XO:
        v = LOWEST
        turn = True

    moves = possible_actions(TTT)
    take = moves[0]
    for move in moves:
        temp_v, temp = com(apply_action(TTT, move, XO), turn, depth+1, alpha, beta)
        
        if temp_v < v and XO:
            take = move
            v = temp_v
            beta = max(beta, temp_v)
        if temp_v > v and not XO:
            take = move
            v = temp_v
            alpha = max(alpha, temp_v)
        apply_action(TTT, move, None)
        if beta<=alpha:
            break
    return v, take


def terminal_state(TTT):
    for i in range(0,3):
        # Check for winning rows
        if ((TTT[i][0] is not None) and (TTT[i][0]==TTT[i][1]==TTT[i][2])):
            return True, LOWEST if TTT[i][0] else HIGHEST
        # Check for winning columns
        if ((TTT[0][i] is not None) and (TTT[0][i]==TTT[1][i]==TTT[2][i])):
            return True, LOWEST if TTT[0][i] else HIGHEST
    
    if ((TTT[1][1] is not None) and ((TTT[0][0]==TTT[1][1]==TTT[2][2]) or (TTT[0][2]==TTT[1][1]==TTT[2][0]))):
        return True, LOWEST if TTT[1][1] else HIGHEST
    
    if not any(None in row for row in TTT):
        return True, 0
    
    return False, None


def possible_actions(TTT):
    moves = []
    for row in range(0,3):
        for col in range(0,3):
            if TTT[row][col]==None:
                moves.append([row, col])
    return moves


def apply_action(TTT, move, XO):
    TTT[move[0]][move[1]] = XO
    return TTT
