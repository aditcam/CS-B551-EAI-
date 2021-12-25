# Simple quintris program! v0.2
# D. Crandall, Sept 2021

from AnimatedQuintris import *
from SimpleQuintris import *
from kbinput import *
import time, sys

class HumanPlayer:
    def get_moves(self, quintris):
        print("Type a sequence of moves using: \n  b for move left \n  m for move right \n  n for rotation\n  h for horizontal flip\nThen press enter. E.g.: bbbnn\n")
        moves = input()
        return moves

    def control_game(self, quintris):
        while 1:
            c = get_char_keyboard()
            commands =  { "b": quintris.left, "h": quintris.hflip, "n": quintris.rotate, "m": quintris.right, " ": quintris.down }
            commands[c]()

#####
# This is the part you'll want to modify!
# Replace our super simple algorithm with something better
#
class ComputerPlayer:
    # This function should generate a series of commands to move the piece into the "optimal"
    # position. The commands are a string of letters, where b and m represent left and right, respectively,
    # and n rotates. quintris is an object that lets you inspect the board, e.g.:
    #   - quintris.col, quintris.row have the current column and row of the upper-left corner of the
    #     falling piece
    #   - quintris.get_piece() is the current piece, quintris.get_next_piece() is the next piece after that
    #   - quintris.left(), quintris.right(), quintris.down(), and quintris.rotate() can be called to actually
    #     issue game commands
    #   - quintris.get_board() returns the current state of the board, as a list of strings.
    #
   

    def get_moves(self, quintris):
        # super simple current algorithm: just randomly move left, right, and rotate a few times
        successors = []
        board = quintris.get_board()
        state = quintris.state
        current_move = quintris.get_piece()
        def left_successors(state,current_move,quintris):
            left_suc = []
            i = current_move[2]
            temp_state = state
            counter = 1 
            while(i!=0):
                for j in range(counter):
                    quintris.left()
                quintris.down()
                left_suc.append(quintris.state)
                quintris.state = temp_state
                quintris.piece = current_move[0]
                quintris.row = current_move[1]
                quintris.col = current_move[2]
                counter+=1
                i-=1
            return left_suc
        def right_successors(state,current_move,quintris):
            right_suc = []
            i = current_move[2]
            temp_state = state
            counter = 1 
            while(i<15):
                for j in range(counter):
                    quintris.right()
                quintris.down()
                right_suc.append(quintris.state)
                quintris.state = temp_state
                quintris.piece = current_move[0]
                quintris.row = current_move[1]
                quintris.col = current_move[2]
                counter+=1
                i+=1
            return right_suc
       
        def rotate_suc(state,current_move,quintris,left_successors,right_successors):
            rot_suc = []
            temp_state = state
            rotate_counter = 1
            for j in range(0,3):
                quintris.rotate()
                current_move = quintris.get_piece()
                print(current_move)
                left = left_successors(state,current_move)
                right = right_successors(state,current_move)
                rot_suc.extend(left+right)
            return rot_suc

        successors = left_successors(state,current_move) + right_successors(state,current_move) + rotate_suc(state,current_move)

        def evaluation(board):
            row_weights = {}
            r = 25
            for i in range(0,25):
                row_weights[i] = r
                r-=1
            col_weights = {}
            c = 15
            for i in range(0,15):
                col_weights[i] = c
                c-=1
            x_counter_row = {}
           
            for i in range(0,25):
                x_counter = 0
                for j in range(0,15):
                    if board[i][j] == 'x':
                        x_counter+=1
                    x_counter_row[i] = x_counter * row_weights[i]
                   
            x_counter_col = {}
            for i in range(0,15):
                y_counter = 0
                for j in range(0,25):
                    if board[j][i] == 'x':
                        y_counter+=1
                    x_counter_col[i] = y_counter * col_weights[i]
           
            best_row = min(x_counter_row,key = x_counter_row.get)
            best_col = min(x_counter_col,key = x_counter_col.get)
           
        #return best_row,best_col
        return random.choice("mnbh") * random.randint(1, 10)
       
    # This is the version that's used by the animted version. This is really similar to get_moves,
    # except that it runs as a separate thread and you should access various methods and data in
    # the "quintris" object to control the movement. In particular:
    #   - quintris.col, quintris.row have the current column and row of the upper-left corner of the
    #     falling piece
    #   - quintris.get_piece() is the current piece, quintris.get_next_piece() is the next piece after that
    #   - quintris.left(), quintris.right(), quintris.down(), and quintris.rotate() can be called to actually
    #     issue game commands
    #   - quintris.get_board() returns the current state of the board, as a list of strings.
    #

    def control_game(self, quintris):
        # another super simple algorithm: just move piece to the least-full column
        while 1:
            time.sleep(0.1)

            board = quintris.get_board()
            column_heights = [ min([ r for r in range(len(board)-1, 0, -1) if board[r][c] == "x"  ] + [100,] ) for c in range(0, len(board[0]) ) ]
            index = column_heights.index(max(column_heights))

            if(index < quintris.col):
                quintris.left()
            elif(index > quintris.col):
                quintris.right()
            else:
                quintris.down()


###################
#### main program

(player_opt, interface_opt) = sys.argv[1:3]

try:
    if player_opt == "human":
        player = HumanPlayer()
    elif player_opt == "computer":
        player = ComputerPlayer()
    else:
        print("unknown player!")

    if interface_opt == "simple":
        quintris = SimpleQuintris()
    elif interface_opt == "animated":
        quintris = AnimatedQuintris()
    else:
        print("unknown interface!")

    quintris.start_game(player)

except EndOfGame as s:
    print("\n\n\n", s)