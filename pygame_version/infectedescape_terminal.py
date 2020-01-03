import copy

def create_display(game):
    game_display = copy.deepcopy(game)

    for row_number in range(1,len(game_display)-1):
        game_display[row_number][0] = row_number
        del game_display[row_number][-1]
        print (game_display[row_number])

print("Welcome to the surround game. A 2 player game. Player 1 is infected, Player 2 is not infected")

game_board_length = 0
while (not isinstance(game_board_length, int)) or game_board_length <= 0: #Variable game board length
    game_board_length = input("Please enter the game board length you would like to play on. (A valid integer value)").strip()
    
    try:
        game_board_length = int(game_board_length)
    except:
        print("That was not a valid entry. Please enter an integer.")

game_running = True 
player = 1 #players 1 start
move_number = 1
exit_pressed = False 

#Game Board setup
game = []
outer_row = []
middle_row = [3,3]
for number in range(0,game_board_length+2):#creates outer row
    outer_row.append(3)

for number in range(0,game_board_length):#creates inner row
    middle_row.insert(1,0)

game.append(outer_row)
for x in range(0,game_board_length):
    game.append(list(middle_row))
game.append(outer_row)

player = 1
move_number = 1

column_key = {} #creates column_key
alphabet = "abcdefghijklmnopqrstuvwxyz"

for entry_value in range(0, game_board_length):
    column_key[alphabet[entry_value]] = entry_value + 1

while game_running: #Main loop

    for turn_number in range(0,player):
        print("___________________________________________________________________ \n")
        
        #restarts move if not valid
        turn_valid = False
        while turn_valid == False:

            #game display
            create_display(game)
            
            print("It is player ",player,"'s move")
            next_move = input("type your move in the form 'a3'.\nWhere the letter is the column and the number is the row. (Type exit to end this program)").strip()

            if next_move == "exit": #tests for exit
                exit_pressed = True
                break

            try: #validates move and edits board
                column = column_key[next_move[0]]
                row = int(next_move[1])
                if game[row][column] == 0 and len(next_move) == 2:
                    if game[row-1][column] == player or game[row][column-1] == player or game[row+1][column] == player or game[row][column+1] == player or move_number <= 2:
                        game[row][column]=player
                        turn_valid = True
            except:
                turn_valid == False
            if turn_valid == False:
                print("That was not a valid move.\n")
                print("___________________________________________________________________ \n")

        game_running = False

        if not exit_pressed:
            for row_check in range(1, game_board_length + 1):#Tests for game end
                for column_check in range(1, game_board_length + 1):
                    if game[row_check][column_check] == 1:
                        if game[row_check-1][column_check] == 0:
                            game_running=True

                        if game[row_check+1][column_check] == 0:
                            game_running=True
                                    
                        if game[row_check][column_check-1] == 0:
                            game_running=True
                                
                        if game[row_check][column_check+1] == 0:
                            game_running=True
                        
        if game_running == False:
            break
        
        move_number += 1
    
    #switch player
    if player == 1:
        player = 2
    else:
        player = 1
    
if not exit_pressed:
    #count scores
    player_1_score = 0

    for row_count in range(1, game_board_length + 1):
        for column_count in range(1, game_board_length + 1):
            if game[row_count][column_count] == 1:
                player_1_score += 1

    create_display(game)
    print("___________________________________________________________________ \n")
    print("The game has ended.\n Player 1 expanded to ", player_1_score, " squares")