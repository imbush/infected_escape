import pygame

class Settings:
    def __init__(self):#initialize settings

        self.window_width = 900 #width of window
        self.window_height = 600 #height of window
        self.top_margin_height = 50 #Size of y margin
        self.bottom_margin_height = 25
        self.margin_width = 20 #Size of x margin
        self.gap_size = 5 #Space between rectangles
        self.game_running = True

        self.default_font_size = self.top_margin_height * 3/5

        self.x_num_rect = 15 #x and y number of squares in board
        self.y_num_rect = 15

        self.board_width = self.window_width - 2 * self.margin_width #pixel width of board
        self.board_height = self.window_height - (self.top_margin_height + self.bottom_margin_height)#pixel height of board

        self.box_width = (self.board_width - self.gap_size * (self.x_num_rect - 1))/self.x_num_rect #box height
        self.box_height = (self.board_height - self.gap_size * (self.y_num_rect - 1))/self.y_num_rect #box width

        self.player1_move = 4 #Infected plaer number of moves per turn
        self.player2_move = 7 #Uninfected player number of moves per turn

        self.white = (255, 255, 255) #colors used
        self.gray = (199, 199, 199) #May need to change
        self.blue = (64, 133, 198)
        self.red = (240, 79, 69)
        self.dark_blue = (20, 54, 86)

        #game colors
        self.bg_color = self.gray
        self.empty_color = self.dark_blue
        self.infected_color = self.red
        self.uninfected_color = self.blue

    def left_top_coords_of_box(self, boxx,boxy):
        '''converts board coordinates to pixel coordinates'''
        left = (boxx - 1) * (self.box_width + self.gap_size) + self.margin_width #formula for finding left of box
        top = (boxy - 1) * (self.box_height + self.gap_size) + self.top_margin_height #formula for finding top of box
        return left, top

    def get_box_at_pixel(self, x, y):
        for boxx in range (self.x_num_rect + 1):
            for boxy in range (self.y_num_rect + 1):
                left, top = self.left_top_coords_of_box(boxx, boxy)
                box_rect = pygame.Rect(left, top, self.box_width, self.box_height) #runs through all rectanglas
                if box_rect.collidepoint(x,y): #tests if box is in box_rect
                    return (boxx, boxy)#coord of box
        return (None, None) #returns none,none if no 

    def draw_board(self, board, screen): 
        '''resets screen with new board'''

        screen.fill(self.bg_color)
        for boxx in range (self.x_num_rect):
            for boxy in range (self.y_num_rect):
                left, top = self.left_top_coords_of_box(boxx + 1, boxy + 1) #I don't know why this works but it works
                if board[boxy][boxx] == 0:
                    pygame.draw.rect(screen, self.empty_color,(left, top, self.box_width, self.box_height)) #draws empty boxes
                elif board[boxy][boxx] == 1:
                    pygame.draw.rect(screen, self.infected_color,(left, top, self.box_width, self.box_height)) #draws infected boxes
                elif board[boxy][boxx] == 2:
                    pygame.draw.rect(screen, self.uninfected_color,(left, top, self.box_width, self.box_height)) 


class game_array:
    def __init__(self,array_x_length, array_y_length):
        board_setup = []

        self.array_x_length = array_x_length
        self.array_y_length = array_y_length

        #board
        outer_row = []
        middle_row = [3,3]
        for number in range(0,array_x_length + 2):#creates outer row
            outer_row.append(3)

        for number in range(0,array_x_length):#creates inner row
            middle_row.insert(1,0)

        board_setup.append(outer_row)
        for x in range(0,array_y_length):
            board_setup.append(list(middle_row))
        board_setup.append(outer_row)

        self.board = board_setup

    def change_rect_status(self, status, boxx, boxy): 
        '''changes the value in an entry in self.board'''

        self.board[boxy][boxx] = status

    def return_board(self): 
        '''returns board without the frame of 3s'''

        new_board = []
        for row_check in range(1, self.array_y_length + 1):
            new_row = list.copy(self.board[row_check])
            del new_row[0]
            del new_row[self.array_x_length]
            new_board.append(new_row)

        return new_board

    def check_move_valid(self, player, valid_boxx, valid_boxy, move_count, player1_move): 
        '''validates a move'''
    
        if self.board[valid_boxy][valid_boxx] == 0:
            if self.board[valid_boxy-1][valid_boxx] == player: #checks box below
                return True
            elif self.board[valid_boxy][valid_boxx-1] == player: #checks box to the left
                return True
            elif self.board[valid_boxy+1][valid_boxx] == player: #checks box above
                return True
            elif self.board[valid_boxy][valid_boxx+1] == player: #checks box to the right
                return True
            elif move_count == 1 or move_count == player1_move + 1: #validates inf's first move or noninf's first move
                return True
        return False

    def check_game_running(self): 
        '''Sees if game is running, returns 0 if running,
        returns 1 = player 1 cannot expand, returns 2 = player 2 cannot expand'''

        inf_surrounded = True #default sets game ended
        noninf_surrounded = True #default sets game ended
        noninf_first_move = True #default sets no noninf on the board

        for row_check in range(1, self.array_y_length + 1): #Checks playable rows
            for column_check in range(1, self.array_x_length + 1): #checks playable columns

                entry = self.board[row_check][column_check] #stores current entry as a variable
                
                if entry == 1: #tests entry value
                    if self.board[row_check-1][column_check] == 0: #checks adjacent entries
                        inf_surrounded = False

                    elif self.board[row_check+1][column_check] == 0:
                        inf_surrounded = False
                                        
                    elif self.board[row_check][column_check-1] == 0:
                        inf_surrounded = False
                                    
                    elif self.board[row_check][column_check+1] == 0:
                        inf_surrounded = False

                elif entry == 2: #tests entry value

                    noninf_first_move = False# if there are 2's on the screen, it is not 2's first move

                    if self.board[row_check-1][column_check] == 0: #checks adjacent entries
                        noninf_surrounded = False

                    elif self.board[row_check+1][column_check] == 0:
                        noninf_surrounded = False                                            
                    
                    elif self.board[row_check][column_check-1] == 0:
                        noninf_surrounded = False
                                        
                    elif self.board[row_check][column_check+1] == 0:
                        noninf_surrounded = False

        if noninf_first_move: #if it is player 2's first move, game continues
            return 0

        elif inf_surrounded: # if inf surrounded return 1, ends game
            return 1

        elif noninf_surrounded: # if noninfected surrounded return 2, ends game
            return 2

        else: 
            return 0 #else, continue game
    def fill_all(self, player):
        '''Used at the end of the game if the noninfected player becomes surrounded to convert all remaining 0s to 1s'''
        for row_check in range(1, self.array_y_length + 1): #Checks playable rows
            for column_check in range(1, self.array_x_length + 1): #checks playable columns
                if self.board[row_check][column_check] == 0:
                    self.board[row_check][column_check] = player #if 0 converts to 1

    def count_score(self, player): 
        '''counts score'''
        score = 0
        for row_check in range(1, self.array_y_length + 1): #checks all rows
            for column_check in range(1, self.array_x_length + 1): #checks all columns
                if self.board[row_check][column_check] == player:
                    score +=  1
        return score

class text: #used for all text boxes
    def __init__(self, characters, text_size, color, screen, font = "freesansbold.ttf"):
        self.characters = characters
        self.text_size = round(text_size)
        self.color = color
        self.screen = screen
        self.font = font

    def right_display_rectangle(self, x_right, y_cent):
        '''creates and displays text on screen'''
        
        font = pygame.font.Font(self.font, self.text_size) #creates a font object
        
        text_object = font.render(self.characters, True, self.color) #creates a text surface object

        rectangle = text_object.get_rect()

        #sets coordinates of rectangle based off of left side and height center
        rectangle.right = x_right
        rectangle.centery = y_cent

        self.screen.blit(text_object, rectangle)

    def left_display_rectangle(self, x_left, y_cent):
        '''creates and displays text on screen'''
        
        font = pygame.font.Font(self.font, self.text_size) #creates a font object
        
        text_object = font.render(self.characters, True, self.color) #creates a text surface object

        rectangle = text_object.get_rect()

        #sets coordinates of rectangle based off of left side and height center
        rectangle.left = x_left
        rectangle.centery = y_cent

        self.screen.blit(text_object, rectangle)


    def right_return_rectangle(self,x_right,y_cent):
        font = pygame.font.Font(self.font, self.text_size) #creates a font object
        
        text_object = font.render(self.characters, True, self.color) #creates a text surface object

        rectangle = text_object.get_rect()

        #sets coordinates of rectangle based off of left side and height center
        rectangle.right = x_right
        rectangle.centery = y_cent

        return rectangle

    def left_return_rectangle(self,x_left,y_cent):
        font = pygame.font.Font(self.font, self.text_size) #creates a font object
        
        text_object = font.render(self.characters, True, self.color) #creates a text surface object

        rectangle = text_object.get_rect()

        #sets coordinates of rectangle based off of left side and height center
        rectangle.left = x_left
        rectangle.centery = y_cent

        return rectangle