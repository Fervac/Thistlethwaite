#!/usr/local/bin/python3

from random import randint

#######
#
# CONST_VAR
# global_var
#
#######
TOTAL_MOVES = 42
MOVES_TAB = ['F', 'B', 'L', 'R', 'U', 'D', "F'", "B'", "L'", "R'", "U'", "D'", 'F2', 'B2', 'L2', 'R2', 'U2', 'D2']
GOAL = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
USAGE = "usage: ./rubik.py -vtrh mix\n\t-v unity visu\n\t-t trace phase by phase\n\t-r random mix generator\n\t-h print usage\n/!\\ Warning /!\\ Any argument after mix or -r will be ignored /!\\ Warning /!\\"
state = GOAL[:]
moves_log = list()
opt = [False, False, False]
mix = ""
#######
#
#######

# These 40 integers represent the entire Rubik's cube state:
# * 0 - 11:	edge positions		(UF UR UB UL DF DR DB DL FR FL BR BL)	{0, ..., 11}
# * 12 - 19:	corner positions	(UFR URB UBL ULF DRF DFL DLB DBR)		{12, ..., 19}
# * 20 - 31:	edge orientations	(UF UR UB UL DF DR DB DL FR FL BR BL)	{0, 1}
# * 32 - 39:	corner orientations	(UFR URB UBL ULF DRF DFL DLB DBR)		{0, 1, 2}

#[UF, UR, UB, UL, DF, DR, DB, DL, FR, FL, BR, BL, UFR, URB, UBL, ULF, DRF, DFL, DLB, DBR
# 0   1   2   3   4   5   6   7   8   9  10  11   12   13   14   15   16   17   18   19

#######
#
# def rotation(state):
#       edges positions swap
#       corners positions swap
#       edges orientations swap
#       corners orientations swap
#
#######

#F
#[9, 1, 2, 3, 8, 5, 6, 7, 0, 4, 10, 11, 15, 13, 14, 17, 12, 16, 18, 19, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 2, 0, 0, 1, 1, 2, 0, 0]
def front_rotation(state):
    state[0], state[4], state[8], state[9] = state[9], state[8], state[0], state[4]
    state[12], state[15], state[16], state[17] = state[15], state[17], state[12], state[16]
    state[20], state[24], state[28], state[29] = (state[29] + 1) % 2, (state[28] + 1) % 2, (state[20] + 1) % 2, (state[24] + 1) % 2
    state[32], state[35], state[36], state[37] = (state[35] + 2) % 3, (state[37] + 1) % 3, (state[32] + 1) % 3, (state[36] + 2) % 3

#B
#[0, 1, 10, 3, 4, 5, 11, 7, 8, 9, 6, 2, 12, 19, 13, 15, 16, 17, 14, 18, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 2, 0, 0, 0, 1, 2]
def back_rotation(state):
    state[2], state[6], state[10], state[11] = state[10], state[11], state[6], state[2]
    state[13], state[14], state[18], state[19] = state[19], state[13], state[14], state[18]
    state[22], state[26], state[30], state[31] = (state[30] + 1) % 2, (state[31] + 1) % 2, (state[26] + 1) % 2, (state[22] + 1) % 2
    state[33], state[34], state[38], state[39] = (state[39] + 1) % 3, (state[33] + 2) % 3, (state[34] + 1) % 3, (state[38] + 2) % 3

#R
#[0, 8, 2, 3, 4, 10, 6, 7, 5, 9, 1, 11, 16, 12, 14, 15, 19, 17, 18, 13, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 0, 0, 2, 0, 0, 1]
def right_rotation(state):
    state[1], state[5], state[8], state[10] = state[8], state[10], state[5], state[1]
    state[12], state[13], state[16], state[19] = state[16], state[12], state[19], state[13]
    state[21], state[25], state[28], state[30] = state[28], state[30], state[25], state[21]
    state[32], state[33], state[36], state[39] = (state[36] + 1) % 3, (state[32] + 2) % 3, (state[39] + 2) % 3, (state[33] + 1) % 3

#L
#[0, 1, 2, 11, 4, 5, 6, 9, 8, 3, 10, 7, 12, 13, 18, 14, 16, 15, 17, 19, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 0, 1, 2, 0]
def left_rotation(state):
    state[3], state[7], state[9], state[11] = state[11], state[9], state[3], state[7]
    state[14], state[15], state[17], state[18] = state[18], state[14], state[15], state[17]
    state[23], state[27], state[29], state[31] = state[31], state[29], state[23], state[27]
    state[34], state[35], state[37], state[38] = (state[38] + 1) % 3, (state[34] + 2) % 3, (state[35] + 1) % 3, (state[37] + 2) % 3

#U
#[1, 2, 3, 0, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14, 15, 12, 16, 17, 18, 19, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
def up_rotation(state):
    state[0], state[1], state[2], state[3] = state[1], state[2], state[3], state[0]
    state[12], state[13], state[14], state[15] = state[13], state[14], state[15], state[12]
    state[20], state[21], state[22], state[23] = state[21], state[22], state[23], state[20]
    state[32], state[33], state[34], state[35] = state[33], state[34], state[35], state[32]

#D
#[0, 1, 2, 3, 7, 4, 5, 6, 8, 9, 10, 11, 12, 13, 14, 15, 17, 18, 19, 16, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
def down_rotation(state):
    state[4], state[5], state[6], state[7] = state[7], state[4], state[5], state[6]
    state[16], state[17], state[18], state[19] = state[17], state[18], state[19], state[16]
    state[24], state[25], state[26], state[27] = state[27], state[24], state[25], state[26]
    state[36], state[37], state[38], state[39] = state[37], state[38], state[39], state[36]

#F'
#[8, 1, 2, 3, 9, 5, 6, 7, 4, 0, 10, 11, 16, 13, 14, 12, 17, 15, 18, 19, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 2, 0, 0, 1, 1, 2, 0, 0]
def front_prime_rotation(state):
    state[0], state[4], state[8], state[9] = state[8], state[9], state[4], state[0]
    state[12], state[15], state[16], state[17] = state[16], state[12], state[17], state[15]
    state[20], state[24], state[28], state[29] = (state[28] + 1) % 2, (state[29] + 1) % 2, (state[24] + 1) % 2, (state[20] + 1) % 2
    state[32], state[35], state[36], state[37] = (state[36] + 2) % 3, (state[32] + 1) % 3, (state[37] + 1) % 3, (state[35] + 2) % 3

#B'
#[0, 1, 11, 3, 4, 5, 10, 7, 8, 9, 2, 6, 12, 14, 18, 15, 16, 17, 19, 13, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 2, 0, 0, 0, 1, 2]
def back_prime_rotation(state):
    state[2], state[6], state[10], state[11] = state[11], state[10], state[2], state[6]
    state[13], state[14], state[18], state[19] = state[14], state[18], state[19], state[13]
    state[22], state[26], state[30], state[31] = (state[31] + 1) % 2, (state[30] + 1) % 2, (state[22] + 1) % 2, (state[26] + 1) % 2
    state[33], state[34], state[38], state[39] = (state[34] + 1) % 3, (state[38] + 2) % 3, (state[39] + 1) % 3, (state[33] + 2) % 3

#R'
#[0, 10, 2, 3, 4, 8, 6, 7, 1, 9, 5, 11, 13, 19, 14, 15, 12, 17, 18, 16, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 0, 0, 2, 0, 0, 1]
def right_prime_rotation(state):
    state[1], state[5], state[8], state[10] = state[10], state[8], state[1], state[5]
    state[12], state[13], state[16], state[19] = state[13], state[19], state[12], state[16]
    state[21], state[25], state[28], state[30] = state[30], state[28], state[21], state[25]
    state[32], state[33], state[36], state[39] = (state[33] + 1) % 3, (state[39] + 2) % 3, (state[32] + 2) % 3, (state[36] + 1) % 3

#L'
#[0, 1, 2, 9, 4, 5, 6, 11, 8, 7, 10, 3, 12, 13, 15, 17, 16, 18, 14, 19, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 0, 1, 2, 0]
def left_prime_rotation(state):
    state[3], state[7], state[9], state[11] = state[9], state[11], state[7], state[3]
    state[14], state[15], state[17], state[18] = state[15], state[17], state[18], state[14]
    state[23], state[27], state[29], state[31] = state[29], state[31], state[27], state[23]
    state[34], state[35], state[37], state[38] = (state[35] + 1) % 3, (state[37] + 2) % 3, (state[38] + 1) % 3, (state[34] + 2) % 3

#U'
#[3, 0, 1, 2, 4, 5, 6, 7, 8, 9, 10, 11, 15, 12, 13, 14, 16, 17, 18, 19, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
def up_prime_rotation(state):
    state[0], state[1], state[2], state[3] = state[3], state[0], state[1], state[2]
    state[12], state[13], state[14], state[15] = state[15], state[12], state[13], state[14]
    state[20], state[21], state[22], state[23] = state[23], state[20], state[21], state[22]
    state[32], state[33], state[34], state[35] = state[35], state[32], state[33], state[34]

#D'
#[0, 1, 2, 3, 5, 6, 7, 4, 8, 9, 10, 11, 12, 13, 14, 15, 19, 16, 17, 18, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
def down_prime_rotation(state):
    state[4], state[5], state[6], state[7] = state[5], state[6], state[7], state[4]
    state[16], state[17], state[18], state[19] = state[19], state[16], state[17], state[18]
    state[24], state[25], state[26], state[27] = state[25], state[26], state[27], state[24]
    state[36], state[37], state[38], state[39] = state[39], state[36], state[37], state[38]

#F2
#[4, 1, 2, 3, 0, 5, 6, 7, 9, 8, 10, 11, 17, 13, 14, 16, 15, 12, 18, 19, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
def front_double_rotation(state):
    state[0], state[4], state[8], state[9] = state[4], state[0], state[9], state[8]
    state[12], state[15], state[16], state[17] = state[17], state[16], state[15], state[12]
    state[20], state[24], state[28], state[29] = state[24], state[20], state[29], state[28]
    state[32], state[35], state[36], state[37] = state[37], state[36], state[35], state[32]

#B2
#[0, 1, 6, 3, 4, 5, 2, 7, 8, 9, 11, 10, 12, 18, 19, 15, 16, 17, 13, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
def back_double_rotation(state):
    state[2], state[6], state[10], state[11] = state[6], state[2], state[11], state[10]
    state[13], state[14], state[18], state[19] = state[18], state[19], state[13], state[14]
    state[22], state[26], state[30], state[31] = state[26], state[22], state[31], state[30]
    state[33], state[34], state[38], state[39] = state[38], state[39], state[33], state[34]

#L2
#[0, 1, 2, 7, 4, 5, 6, 3, 8, 11, 10, 9, 12, 13, 17, 18, 16, 14, 15, 19, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
def left_double_rotation(state):
    state[3], state[7], state[9], state[11] = state[7], state[3], state[11], state[9]
    state[14], state[15], state[17], state[18] = state[17], state[18], state[14], state[15]
    state[23], state[27], state[29], state[31] = state[27], state[23], state[31], state[29]
    state[34], state[35], state[37], state[38] = state[37], state[38], state[34], state[35]

#R2
#[0, 5, 2, 3, 4, 1, 6, 7, 10, 9, 8, 11, 19, 16, 14, 15, 13, 17, 18, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
def right_double_rotation(state):
    state[1], state[5], state[8], state[10] = state[5], state[1], state[10], state[8]
    state[12], state[13], state[16], state[19] = state[19], state[16], state[13], state[12]
    state[21], state[25], state[28], state[30] = state[25], state[21], state[30], state[28]
    state[32], state[33], state[36], state[39] = state[39], state[36], state[33], state[32]

#U2
#[2, 3, 0, 1, 4, 5, 6, 7, 8, 9, 10, 11, 14, 15, 12, 13, 16, 17, 18, 19, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
def up_double_rotation(state):
    state[0], state[1], state[2], state[3] = state[2], state[3], state[0], state[1]
    state[12], state[13], state[14], state[15] = state[14], state[15], state[12], state[13]
    state[20], state[21], state[22], state[23] = state[22], state[23], state[20], state[21]
    state[32], state[33], state[34], state[35] = state[34], state[35], state[32], state[33]

#D2
#[0, 1, 2, 3, 6, 7, 4, 5, 8, 9, 10, 11, 12, 13, 14, 15, 18, 19, 16, 17, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
def down_double_rotation(state):
    state[4], state[5], state[6], state[7] = state[6], state[7], state[4], state[5]
    state[16], state[17], state[18], state[19] = state[18], state[19], state[16], state[17]
    state[24], state[25], state[26], state[27] = state[26], state[27], state[24], state[25]
    state[36], state[37], state[38], state[39] = state[38], state[39], state[36], state[37]

def move(state, m):
    if m == 'F':
        front_rotation(state)
    elif m == 'B':
        back_rotation(state)
    elif m == 'L':
        left_rotation(state)
    elif m == 'R':
        right_rotation(state)
    elif m == 'U':
        up_rotation(state)
    elif m == 'D':
        down_rotation(state)
    elif m == "F'":
        front_prime_rotation(state)
    elif m == "B'":
        back_prime_rotation(state)
    elif m == "L'":
        left_prime_rotation(state)
    elif m == "R'":
        right_prime_rotation(state)
    elif m == "U'":
        up_prime_rotation(state)
    elif m == "D'":
        down_prime_rotation(state)
    elif m == "F2":
        front_double_rotation(state)
    elif m == "B2":
        back_double_rotation(state)
    elif m == "L2":
        left_double_rotation(state)
    elif m == "R2":
        right_double_rotation(state)
    elif m == "U2":
        up_double_rotation(state)
    elif m == "D2":
        down_double_rotation(state)
    else:
        print("Parsing Error: " + m + " is not a move, quiting program")
        exit()

def parse_mix(mix_str):
    global mix
    moves_tab = mix_str.split()
    for m in moves_tab:
        mix += m + ' '
        move(state, m)

def random_mix():
    global mix
    my_randoms = [MOVES_TAB[randint(0,17)] for x in range(TOTAL_MOVES)]
    for m in my_randoms:
        mix += m + ' '
    print('random mix: ' + mix)
    for m in my_randoms:
        move(state, m)

########
#
# Possible arguments:
# standard list of moves "F, B, L, R, U, D, F', B', L', R', U', D', F2, B2, L2, R2, U2, D2"
# -v unity visu
# -r random gen
# -t trace
# -h usage
#
########

def parse_opt(opt_str):
    i = 1
    while i < len(opt_str):
        if opt_str[i] == 'v':
            opt[0] = True
        elif opt_str[i] == 't':
            opt[1] = True
        elif opt_str[i] == 'r':
            opt[2] = True
            random_mix()
        elif opt_str[i] == 'h':
            print(USAGE)
            exit()
        else:
            print("Parsing Error: " + opt_str[i] + " is not allowed as option, quiting program")
            exit()
        i += 1
