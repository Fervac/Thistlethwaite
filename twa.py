#!/usr/local/bin/python3

import moves as mov
from collections import deque

FORWARD = 1
BACKWARD = 2
PHASE_MOVES =   [["F","B","L","R","U","D","F'","B'","L'","R'","U'","D'","F2","B2","L2","R2","U2","D2"], # From G0 to G1 u can do all moves
                ["L","R","U","D","L'","R'","U'","D'","F2","B2","L2","R2","U2","D2"], # From G1 to G2 you can't do 1/4 turns Front and Back moves
                ["U","D","U'","D'","F2","B2","L2","R2","U2","D2"], # From G2 to G3 1/4 turns are allowed only for Up and Down moves
                ["F2","B2","L2","R2","U2","D2"]] # From G3 to G4 no 1/4 turns at all

def get_id(state, phase):
    if phase == 0:
        #########
        # PHASE 0 - Getting from G0 to G1
        #
        # tuple[0:11] is edges orientations
        #
        #########
        return tuple(state[20:32])
    elif phase == 1:
        #########
        # PHASE 1 - Getting from G1 to G2
        #
        # tuple[0:3] is edges positions from 8-11
        # tuple[4:15] is corners orientations
        #
        #########
        result = state[0:12]
        i = 0
        while i < 12:
            if result[i] > 7 and result[i] < 12:
                result[i] = 1
            else:
                result[i] = 0
            i += 1
        result.extend(state[32:40])
        return tuple(result)
    elif phase == 2:
        #########
        # PHASE 2 - Getting from G2 to G3
        #
        # tuple[0:7] is corners good position
        # tuple[8:15] is edges respectively on M or S slices
        # tuple[16:19] is edges E slice good placement or half turned
        #
        #########
        result = state[12:20]
        result.append(1 if state[0] == 0 or state[0] == 2 or state[0] == 4 or state[0] == 6 else 0) # UF -> UB DF DB
        result.append(1 if state[2] == 0 or state[2] == 2 or state[2] == 4 or state[2] == 6 else 0) # UB -> UF DF DB
        result.append(1 if state[4] == 0 or state[4] == 2 or state[4] == 4 or state[4] == 6 else 0) # DF -> UF UB DB
        result.append(1 if state[6] == 0 or state[6] == 2 or state[6] == 4 or state[6] == 6 else 0) # DB -> UF UB DF
        result.append(1 if state[1] == 1 or state[1] == 3 or state[1] == 5 or state[1] == 7 else 0) # UR -> UL DR DL
        result.append(1 if state[3] == 1 or state[3] == 3 or state[3] == 5 or state[3] == 7 else 0) # UL -> UR DR DL
        result.append(1 if state[5] == 1 or state[5] == 3 or state[5] == 5 or state[5] == 7 else 0) # DR -> UR UL DL
        result.append(1 if state[7] == 1 or state[7] == 3 or state[7] == 5 or state[7] == 7 else 0) # DL -> UR UL DR
        result.append(1 if state[8] == 8 or state[8] == 11 else 0) # FR
        result.append(1 if state[11] == 8 or state[11] == 11 else 0) # BL
        result.append(1 if state[9] == 9 or state[9] == 10 else 0) # FL
        result.append(1 if state[10] == 9 or state[10] == 10 else 0) # BR
        return tuple(result)
    else:
        #########
        # PHASE 3 - Getting from G3 to G4
        #
        # tuple[0:39] full state
        #
        #########
        return tuple(state)

def inverse_move(move):
    if len(move) is 2:
        if move[1] is '2':
            return move
        else:
            return move[0]
    return move + "'"

def bi_dir_bfs(phase, start_id, goal_id):
    nodes_dict = { start_id:[FORWARD, None, None, mov.state], goal_id:[BACKWARD, None, None, mov.GOAL]} # nodes_dict[id] = [direction, move, parent, state]
    queue = deque([nodes_dict[start_id], nodes_dict[goal_id]]) # classic queue first in first out
    while True:
        current_node = queue.popleft()
        for move in PHASE_MOVES[phase]:
            new_state = current_node[3][:]
            mov.move(new_state, move)
            new_id = get_id(new_state, phase)
            new_node = nodes_dict.get(new_id)
            if new_node != None and new_node[0] != current_node[0]: # phase solved
                if current_node[0] == BACKWARD: # swap current and new nodes
                    current_node, new_node = new_node, current_node
                    move = inverse_move(move)
                moves = [move]
                while list(nodes_dict.keys())[list(nodes_dict.values()).index(current_node)] != start_id: # traverse to beginning state
                    moves.insert(0, current_node[1])
                    current_node = current_node[2]
                while list(nodes_dict.keys())[list(nodes_dict.values()).index(new_node)] != goal_id: # traverse to goal state
                    moves.append(inverse_move(new_node[1]))
                    new_node = new_node[2]
                return moves
            elif new_node is None: # create new node
                nodes_dict[new_id] = [current_node[0], move, current_node, new_state]
                queue.append(nodes_dict[new_id])
        current_node[3] = None # delete State to save Memory

def solver():
    for phase in range(4):
        start_id = get_id(mov.state, phase)
        goal_id = get_id(mov.GOAL, phase)
        if start_id == goal_id:
            continue
        moves = bi_dir_bfs(phase, start_id, goal_id)
        tmp = ""
        for m in moves:
            mov.move(mov.state, m)
            tmp += m + ' '
        if mov.opt[1] is True:
            print('Phase ' + str(phase) + ': ' + tmp)
        mov.moves_log.extend(moves)