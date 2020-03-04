import pygame, pyautogui, random, time


class window():
    def __init__(self):
        self.width = int(pyautogui.size()[0]/2/2)
        self.height = int(pyautogui.size()[1]/2)
        self.grid_size = [10, 10]
        self.cell_x = int(self.width/self.grid_size[0])
        self.cell_y = int(self.height/self.grid_size[1])
        self.mine_amount = int(self.grid_size[0]*self.grid_size[1]/8)
        self.check_list = []

        self.mask = []
        self.field = []
        for x in range(self.grid_size[0]):
            self.mask.append([])
            self.field.append([])
            for y in range(self.grid_size[1]):
                self.mask[x].append(1)
                self.field[x].append(0)

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
                    try:
                        if self.field[x-1][y] != -1 and x > 0:
                            self.field[x-1][y] += 1
                    except IndexError:
                        pass
                    try:
                        if self.field[x+1][y] != -1:
                            self.field[x+1][y] += 1
                    except IndexError:
                        pass
                    try:
                        if self.field[x][y+1] != -1:
                            self.field[x][y+1] += 1
                    except IndexError:
                        pass
                    try:
                        if self.field[x][y-1] != -1 and y > 0:
                            self.field[x][y-1] += 1
                    except IndexError:
                        pass
                    try:
                        if self.field[x-1][y+1] != -1 and x > 0:
                            self.field[x-1][y+1] += 1
                    except IndexError:
                        pass
                    try:
                        if self.field[x-1][y-1] != -1:
                            if x > 0 and y > 0:
                                self.field[x-1][y-1] += 1
                    except IndexError:
                        pass
                    try:
                        if self.field[x+1][y+1] != -1:
                            self.field[x+1][y+1] += 1
                    except IndexError:
                        pass
                    try:
                        if self.field[x+1][y-1] != -1 and y > 0:
                            self.field[x+1][y-1] += 1
                    except IndexError:
                        pass

    def mask_check_neighbors(self, x, y):
        for cell in self.check_list:
            if cell[0] == x and cell[1] == y:
                return
        
        self.check_list.append([x, y])
        try:
            if self.field[x-1][y] == 0 and x > 0:
                self.mask[x-1][y] = 0
                self.mask_check_neighbors(x-1, y)
            elif self.field[x-1][y] > 0 and x > 0:
                self.mask[x-1][y] = 0
        except IndexError:
            pass
        try:
            if self.field[x+1][y] == 0:
                self.mask[x+1][y] = 0
                self.mask_check_neighbors(x+1, y)
            elif self.field[x+1][y] > 0:
                self.mask[x+1][y] = 0
        except IndexError:
            pass
        try:
            if self.field[x][y+1] == 0:
                self.mask[x][y+1] = 0
                self.mask_check_neighbors(x, y+1)
            elif self.field[x][y+1] > 0:
                self.mask[x][y+1] = 0
        except IndexError:
            pass
        try:
            if self.field[x][y-1] == 0 and y > 0:
                self.mask[x][y-1] = 0
                self.mask_check_neighbors(x, y-1)
            elif self.field[x][y-1] > 0 and y > 0:
                self.mask[x][y-1] = 0
        except IndexError:
            pass
        try:
            if self.field[x-1][y+1] == 0 and x > 0:
                self.mask[x-1][y+1] = 0
                self.mask_check_neighbors(x-1, y+1)
            elif self.field[x-1][y+1] > 0 and x > 0:
                self.mask[x-1][y+1] = 0
        except IndexError:
            pass
        try:
            if x > 0 and y > 0:
                if self.field[x-1][y-1] == 0:
                    self.mask[x-1][y-1] = 0
                    self.mask_check_neighbors(x-1, y-1)
                elif self.field[x-1][y-1] > 0:
                    self.mask[x-1][y-1] = 0
        except IndexError:
            pass
        try:
            if self.field[x+1][y+1] == 0:
                self.mask[x+1][y+1] = 0
                self.mask_check_neighbors(x+1, y+1)
            elif self.field[x+1][y+1] > 0:
                self.mask[x+1][y+1] = 0
        except IndexError:
            pass
        try:
            if self.field[x+1][y-1] == 0 and y > 0:
                self.mask[x+1][y-1] = 0
                self.mask_check_neighbors(x+1, y-1)
            elif self.field[x+1][y-1] > 0 and y > 0:
                self.mask[x+1][y-1] = 0
        except IndexError:
            pass
                



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
 
# Set the width and height of the screen [width, height]
size = (minesweeper.width, minesweeper.height)
screen = pygame.display.set_mode(size)
 
pygame.display.set_caption("minesweeper")
 
# Loop until the user clicks the close button.
done = False
lost = False
won = False
pressed = False
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
        mouse_x = int(mouse[0]/minesweeper.cell_x) # getting mouse grid x postion
        mouse_y = int(mouse[1]/minesweeper.cell_y) # getting mouse grid y postion
        button = pygame.mouse.get_pressed() # getting mouse buttons' state

        if button[0]: # if left mouse button is pressed, remove mask at mouse grid position
            for x in range(len(minesweeper.mask)):
                for y in range(len(minesweeper.mask[x])):
                    if x == mouse_x and y == mouse_y:
                        if minesweeper.mask[x][y] != 10:
                            minesweeper.mask[x][y] = 0
                            if minesweeper.field[x][y] == 0:
                                minesweeper.mask_check_neighbors(x,y)
                            elif minesweeper.field[x][y] == -1:
                                lost = True
        elif button[2] and not pressed:
            pressed = True
            for x in range(len(minesweeper.mask)):
                for y in range(len(minesweeper.mask[x])):
                    if x == mouse_x and y == mouse_y:
                        if minesweeper.mask[x][y] == 1:
                            minesweeper.mask[x][y] = 10
                        elif minesweeper.mask[x][y] == 10:
                            minesweeper.mask[x][y] = 1
        
        if not button[2]:
            pressed = False


        # checking for win conditions
        count = 0
        for x in range(len(minesweeper.mask)):
            for y in range(len(minesweeper.mask[x])):
                if minesweeper.field[x][y] == -1 and minesweeper.mask[x][y] == 10:
                    count += 1
        if count == minesweeper.mine_amount:
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
                pygame.draw.rect(screen,MINE,[x*minesweeper.cell_x,y*minesweeper.cell_y,minesweeper.cell_x,minesweeper.cell_y],0)
            elif minesweeper.field[x][y] > 0:
                # Select the font to use, size, bold, italics
                if minesweeper.cell_x < minesweeper.cell_y:
                    font = pygame.font.SysFont('Calibri', minesweeper.cell_x, True, False)
                else:
                    font = pygame.font.SysFont('Calibri', minesweeper.cell_y, True, False)
 
                # Render the text. "True" means anti-aliased text.
                # Black is the color. This creates an image of the
                # letters, but does not put it on the screen
                text = font.render(str(minesweeper.field[x][y]), True, BLACK)
 
                # Put the image of the text on the screen at 250x250
                screen.blit(text, [x*minesweeper.cell_x+minesweeper.cell_x/5, y*minesweeper.cell_y+minesweeper.cell_y/5])

    # mask
    for x in range(len(minesweeper.mask)):
        for y in range(len(minesweeper.mask[x])):
            if minesweeper.mask[x][y] == 1:
                pygame.draw.rect(screen,MASK,[x*minesweeper.cell_x,y*minesweeper.cell_y,minesweeper.cell_x,minesweeper.cell_y],0)
            elif minesweeper.mask[x][y] == 10:
                pygame.draw.rect(screen,MASK,[x*minesweeper.cell_x,y*minesweeper.cell_y,minesweeper.cell_x,minesweeper.cell_y],0)
                # Select the font to use, size, bold, italics
                if minesweeper.cell_x < minesweeper.cell_y:
                    font = pygame.font.SysFont('Calibri', minesweeper.cell_x, True, False)
                else:
                    font = pygame.font.SysFont('Calibri', minesweeper.cell_y, True, False)
 
                # Render the text. "True" means anti-aliased text.
                # Black is the color. This creates an image of the
                # letters, but does not put it on the screen
                text = font.render("!", True, BLACK)
 
                # Put the image of the text on the screen at 250x250
                screen.blit(text, [x*minesweeper.cell_x+minesweeper.cell_x/5, y*minesweeper.cell_y+minesweeper.cell_y/5])

    # grid
    for x in range(minesweeper.grid_size[0]+1):
        pygame.draw.line(screen, WHITE, [x*minesweeper.cell_x, 0], [x*minesweeper.cell_x, minesweeper.height], int(minesweeper.cell_x/10))
    for y in range(minesweeper.grid_size[1]+1):
        pygame.draw.line(screen, WHITE, [0, y*minesweeper.cell_y], [minesweeper.width, y*minesweeper.cell_y], int(minesweeper.cell_y/10))

    # won
    if won or lost:
        # Select the font to use, size, bold, italics
        if minesweeper.cell_x < minesweeper.cell_y:
            font = pygame.font.SysFont('Calibri', minesweeper.cell_x, True, False)
        else:
            font = pygame.font.SysFont('Calibri', minesweeper.cell_y, True, False)

        # Render the text. "True" means anti-aliased text.
        # Black is the color. This creates an image of the
        # letters, but does not put it on the screen
        if won:
            text = font.render("you won!", True, GREEN)
        else:
            text = font.render("you lost!", True, RED)

        # Put the image of the text on the screen at 250x250
        screen.blit(text, [minesweeper.width/2-minesweeper.cell_x, minesweeper.height/2-minesweeper.cell_y])
 
    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 
    # --- Limit to 60 frames per second
    clock.tick(60)
 
# Close the window and quit.
pygame.quit()