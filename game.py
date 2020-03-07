import pygame, pyautogui, random, time


grid_size = input(f"grid size (leave blank for {20}x{15}): ")
if grid_size != "":
    grid_size = grid_size.split("x")
    grid_size[0] = int(grid_size[0])
    grid_size[1] = int(grid_size[1])
    if grid_size[0] >= 40 or grid_size[1] >= 40:
        caution = input("Carefull, at sizes like these the game will start being really slow. Are you sure you want to play with this grid size? [y/n]: ")
        if caution == "n":
            quit()
else:
    grid_size = [20, 15]

bomb_amount = input(f"amount of mines (leave blank for {int(grid_size[0]*grid_size[1]/8)}): ")
if bomb_amount != "":
    bomb_amount = int(bomb_amount)
else:
    bomb_amount = int(grid_size[0]*grid_size[1]/8)

class window():
    def __init__(self):
        global grid_size, bomb_amount
        self.grid_size = grid_size
        self.mine_amount = bomb_amount
        if grid_size[0] < 25 and grid_size[1] < 25:
            if self.grid_size[0] > self.grid_size[1]:
                self.cell_size = int(pyautogui.size()[1]/2/self.grid_size[0])
            else:
                self.cell_size = int(pyautogui.size()[1]/2/self.grid_size[1])
        else:
            if self.grid_size[0] > self.grid_size[1]:
                self.cell_size = int(pyautogui.size()[0]/2/self.grid_size[0])
            else:
                self.cell_size = int(pyautogui.size()[0]/2/self.grid_size[1])
        self.width = self.cell_size*self.grid_size[0]
        self.height = self.cell_size*self.grid_size[1]
        self.check_list = []

        self.mask = []
        self.field = []
        self.defused = []
        for x in range(self.grid_size[0]):
            self.mask.append([])
            self.field.append([])
            self.defused.append([])
            for y in range(self.grid_size[1]):
                self.mask[x].append(1)
                self.field[x].append(0)
                self.defused[x].append(0)

        for i in range(self.mine_amount):
            x = random.randint(0, len(self.field)-1)
            y = random.randint(0, len(self.field[0])-1)
            while self.field[x][y] == -1:
                x = random.randint(0, len(self.field)-1)
                y = random.randint(0, len(self.field[0])-1)
            self.field[x][y] = -1

        for x in range(self.grid_size[0]):
            for y in range(self.grid_size[1]):
                if self.field[x][y] == -1:
                    for xi in range(-1, 2):
                        for yi in range(-1, 2):
                            if x+xi > -1 and y+yi > -1:
                                try:
                                    if self.field[x+xi][y+yi] != -1:
                                        self.field[x+xi][y+yi] += 1
                                except IndexError:
                                    pass
    
    def set_mines(self, amount):

        self.mine_amount = amount

        for x in range(len(self.field)):
            for y in range(len(self.field[x])):
                self.field[x][y] = 0

        for i in range(amount):
            x = random.randint(0, len(self.field)-1)
            y = random.randint(0, len(self.field[0])-1)
            while self.field[x][y] == -1:
                x = random.randint(0, len(self.field)-1)
                y = random.randint(0, len(self.field[0])-1)
            self.field[x][y] = -1

        for x in range(self.grid_size[0]):
            for y in range(self.grid_size[1]):
                if self.field[x][y] == -1:

                    for xi in range(-1, 2):
                        for yi in range(-1, 2):
                            try:
                                if self.field[x+xi][y+yi] != -1:
                                    if x+xi > -1 and y+yi > -1:
                                        self.field[x+xi][y+yi] += 1
                            except IndexError:
                                pass
        
    def mask_remove_neighbors(self, x, y):
        for cell in self.check_list:
            if cell[0] == x and cell[1] == y:
                return
        self.check_list.append([x, y])
        for xi in range(-1, 2):
            for yi in range(-1, 2):
                try:
                    if x+xi > -1 and y+yi > -1:
                        if self.field[x+xi][y+yi] == 0:
                            self.mask[x+xi][y+yi] = 0
                            self.mask_remove_neighbors(x+xi, y+yi)
                        elif self.field[x+xi][y+yi] > 0:
                            self.mask[x+xi][y+yi] = 0
                except IndexError:
                    pass

    def check_neighbors(self, x, y, value, list_type):
        neighbors = []
        for xi in range(-1, 2):
            for yi in range(-1, 2):
                try:
                    if list_type[x+xi][y+yi] == value:
                        if x+xi > -1 and y+yi > -1:
                            neighbors.append([x+xi, y+yi])
                except IndexError:
                    pass
        return neighbors

    def check_mask(self, x, y, value):
        return self.check_neighbors(x, y, value, self.mask)

    def check_field(self, x, y, value):
        return self.check_neighbors(x, y, value, self.field)

    def check_defused(self, x, y, value):
        return self.check_neighbors(x, y, value, self.defused)
                



minesweeper = window()
 
# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BG = (222, 222, 222)
MINE = (255, 0, 0)
MASK = (180, 180, 180)
 
pygame.init()

bomb_img = pygame.transform.scale(pygame.image.load("bomb.png"), (minesweeper.cell_size, minesweeper.cell_size))
bombed_img = pygame.transform.scale(pygame.image.load("bombed.png"), (minesweeper.cell_size, minesweeper.cell_size))
flag_img = pygame.transform.scale(pygame.image.load("flag.png"), (minesweeper.cell_size, minesweeper.cell_size))
flagged_img = pygame.transform.scale(pygame.image.load("flaged_bomb.png"), (minesweeper.cell_size, minesweeper.cell_size))
flag_temp_img = pygame.transform.scale(pygame.image.load("flag_temp.png"), (minesweeper.cell_size, minesweeper.cell_size))
 
# Set the width and height of the screen [width, height]
size = (minesweeper.width, minesweeper.height)
screen = pygame.display.set_mode(size)
 
pygame.display.set_caption("Minesweeper")
 
# Loop until the user clicks the close button.
done = False
lost = False
won = False
r_pressed = False
l_pressed = False
pre_mouse_x = 0
pre_mouse_y = 0
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
 
# -------- Main Program Loop -----------
while not done:
    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                del minesweeper
                minesweeper = window()
                won = False
                lost = False
 
    # --- Game logic should go here
    if won == False and lost == False:
        mouse = pygame.mouse.get_pos() # getting mpouse position
        mouse_x = int(mouse[0]/minesweeper.cell_size) # getting mouse grid x postion
        mouse_y = int(mouse[1]/minesweeper.cell_size) # getting mouse grid y postion
        button = pygame.mouse.get_pressed() # getting mouse buttons' state

        if l_pressed and button[0] == 0:
            l_pressed = False
            for x in range(len(minesweeper.mask)):
                for y in range(len(minesweeper.mask[x])):
                    if x == mouse_x and y == mouse_y:
                        if minesweeper.defused[x][y] == 0:
                            if minesweeper.field[x][y] == 0:
                                minesweeper.mask_remove_neighbors(x,y)
                            elif minesweeper.field[x][y] == -1: # lost
                                minesweeper.field[x][y] = -2
                                minesweeper.mask[x][y] = 0
                                for x in range(len(minesweeper.mask)):
                                    for y in range(len(minesweeper.mask[x])):
                                        if minesweeper.field[x][y] == -1:
                                            minesweeper.mask[x][y] = 0
                                lost = True
                            elif minesweeper.field[x][y] > 0 and minesweeper.mask[x][y] == 0:
                                bombs = minesweeper.check_defused(x, y, 1)
                                real_bombs = minesweeper.check_field(x, y, -1)
                                all_defused = True

                                if len(bombs) == len(real_bombs):
                                    count = 0
                                    for bomb in range(len(bombs)):
                                        if bombs[bomb][0] != real_bombs[bomb][0] or bombs[bomb][1] != real_bombs[bomb][1]:
                                            all_defused = False
                                else:
                                    all_defused = False

                                if all_defused:
                                    empty = minesweeper.check_field(x, y, 0)
                                    for cell in empty:
                                        minesweeper.mask_remove_neighbors(cell[0], cell[1])
                                    others = []
                                    for i in range(0, 9):
                                        others.append(minesweeper.check_field(x, y, i))
                                    for accumulation in others:
                                        for cell in accumulation:
                                            minesweeper.mask[cell[0]][cell[1]] = 0
                                elif len(bombs) == len(real_bombs):
                                    for x in range(len(minesweeper.mask)):
                                        for y in range(len(minesweeper.mask[x])):
                                            if minesweeper.field[x][y] == -1:
                                                minesweeper.mask[x][y] = 0
                                    lost = True
                            minesweeper.mask[x][y] = 0

        if button[0]: # if left mouse button is r_pressed, remove mask at mouse grid position
            l_pressed = True
            
        elif button[2] and not r_pressed:
            r_pressed = True
            for x in range(len(minesweeper.mask)):
                for y in range(len(minesweeper.mask[x])):
                    if x == mouse_x and y == mouse_y:
                        if minesweeper.mask[x][y] == 1:
                            if minesweeper.defused[x][y] == 0:
                                minesweeper.defused[x][y] = 1
                            elif minesweeper.defused[x][y] == 1:
                                minesweeper.defused[x][y] = 2
                            elif minesweeper.defused[x][y] == 2:
                                minesweeper.defused[x][y] = 0
        
        if not button[2]:
            r_pressed = False


        # checking for win conditions
        count = 0
        for x in range(len(minesweeper.mask)):
            for y in range(len(minesweeper.mask[x])):
                if minesweeper.field[x][y] == -1 and minesweeper.defused[x][y] == 1:
                    count += 1
        if count == minesweeper.mine_amount: # won
            for x in range(len(minesweeper.mask)):
                for y in range(len(minesweeper.mask[x])):
                    if minesweeper.field[x][y] > -1 and minesweeper.mask[x][y] == 1:
                        minesweeper.mask[x][y] = 0
            won = True

            
        pre_mouse_x = mouse_x
        pre_mouse_y = mouse_y
    # --- Screen-clearing code goes here
 
    # Here, we clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.
 
    # If you want a background image, replace this clear with blit'ing the
    # background image.
    screen.fill(BG)
 
    # --- Drawing code should go here

    # field
    for x in range(len(minesweeper.field)):
        for y in range(len(minesweeper.field[x])):
            if minesweeper.field[x][y] == -1:
                screen.blit(bomb_img, (x*minesweeper.cell_size, y*minesweeper.cell_size))
                #pygame.draw.rect(screen,MINE,[x*minesweeper.cell_size,y*minesweeper.cell_size,minesweeper.cell_size,minesweeper.cell_size],0)
            elif minesweeper.field[x][y] == -2:
                screen.blit(bombed_img, (x*minesweeper.cell_size, y*minesweeper.cell_size))
            elif minesweeper.field[x][y] > 0:
                # Select the font to use, size, bold, italics
                if minesweeper.cell_size < minesweeper.cell_size:
                    font = pygame.font.SysFont('Calibri', minesweeper.cell_size, True, False)
                else:
                    font = pygame.font.SysFont('Calibri', minesweeper.cell_size, True, False)
 
                # Render the text. "True" means anti-aliased text.
                # Black is the color. This creates an image of the
                # letters, but does not put it on the screen
                text = font.render(str(minesweeper.field[x][y]), True, BLACK)
 
                # Put the image of the text on the screen at 250x250
                screen.blit(text, [x*minesweeper.cell_size+minesweeper.cell_size/5, y*minesweeper.cell_size+minesweeper.cell_size/5])

    # mask
    for x in range(len(minesweeper.mask)):
        for y in range(len(minesweeper.mask[x])):
            if minesweeper.mask[x][y] == 1:
                pygame.draw.rect(screen,MASK,[x*minesweeper.cell_size,y*minesweeper.cell_size,minesweeper.cell_size,minesweeper.cell_size],0)

    # defused
    for x in range(len(minesweeper.mask)):
        for y in range(len(minesweeper.mask[x])):
            if minesweeper.defused[x][y] == 1:
                if won or lost:
                    screen.blit(flagged_img, (x*minesweeper.cell_size, y*minesweeper.cell_size))
                else:
                    screen.blit(flag_img, (x*minesweeper.cell_size, y*minesweeper.cell_size))
            elif minesweeper.defused[x][y] == 2:
                if won == False and lost == False:
                    screen.blit(flag_temp_img, (x*minesweeper.cell_size, y*minesweeper.cell_size))
                '''# Select the font to use, size, bold, italics
                if minesweeper.cell_size < minesweeper.cell_size:
                    font = pygame.font.SysFont('Calibri', minesweeper.cell_size, True, False)
                else:
                    font = pygame.font.SysFont('Calibri', minesweeper.cell_size, True, False)
 
                # Render the text. "True" means anti-aliased text.
                # Black is the color. This creates an image of the
                # letters, but does not put it on the screen
                text = font.render("!", True, BLACK)
 
                # Put the image of the text on the screen at 250x250
                screen.blit(text, [x*minesweeper.cell_size+minesweeper.cell_size/5, y*minesweeper.cell_size+minesweeper.cell_size/5])'''

    # grid
    for x in range(minesweeper.grid_size[0]+1):
        pygame.draw.line(screen, WHITE, [x*minesweeper.cell_size, 0], [x*minesweeper.cell_size, minesweeper.height], int(minesweeper.cell_size/10))
    for y in range(minesweeper.grid_size[1]+1):
        pygame.draw.line(screen, WHITE, [0, y*minesweeper.cell_size], [minesweeper.width, y*minesweeper.cell_size], int(minesweeper.cell_size/10))

    # won
    if won or lost:
        # Select the font to use, size, bold, italics
        if minesweeper.cell_size < minesweeper.cell_size:
            font = pygame.font.SysFont('Calibri', minesweeper.cell_size, True, False)
        else:
            font = pygame.font.SysFont('Calibri', minesweeper.cell_size, True, False)

        # Render the text. "True" means anti-aliased text.
        # Black is the color. This creates an image of the
        # letters, but does not put it on the screen
        if won:
            text = font.render("you won!", True, GREEN)
        else:
            text = font.render("you lost!", True, RED)

        # Put the image of the text on the screen at 250x250
        screen.blit(text, [minesweeper.width/2-minesweeper.cell_size, minesweeper.height/2-minesweeper.cell_size])
 
    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 
    # --- Limit to 60 frames per second
    clock.tick(60)
 
# Close the window and quit.
pygame.quit()