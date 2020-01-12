import pygame
import time

pygame.init()

TITLE = "Sudoku Solver"
SIZE = (1000, 600)
WHITE = (255,255,255)
GRAY = (200,200,200)
BLUE = (51,204,255)
BLACK = (0,0,0)
ROWS = 9
COLS = 9
FONT = pygame.font.SysFont("arial", 40, bold=True)
NUMBER_FONT = font = pygame.font.SysFont("comicsans", 40)

BOARD1 = [
    [5, 0, 0, 1, 0, 0, 0, 9, 0],
    [0, 7, 9, 5, 6, 0, 1, 0, 2],
    [2, 3, 0, 0, 4, 0, 8, 0, 0],
    [6, 9, 0, 0, 0, 0, 0, 0, 0],
    [3, 0, 0, 2, 9, 1, 0, 0, 8],
    [0, 0, 0, 0, 0, 0, 0, 2, 4],
    [0, 0, 6, 0, 7, 0, 0, 1, 9],
    [9, 0, 3, 0, 5, 2, 7, 4, 0],
    [0, 4, 0, 0, 0, 6, 0, 0, 3]
]

BOARD3 =  [
    [8, 0, 0, 1, 0, 0, 0, 6, 0],
    [2, 9, 6, 0, 0, 5, 0, 0, 0],
    [0, 0, 4, 9, 0, 2, 0, 0, 0],
    [0, 0, 1, 0, 5, 8, 0, 0, 0],
    [6, 4, 0, 0, 0, 0, 0, 8, 9],
    [0, 0, 0, 4, 2, 0, 6, 0, 0],
    [0, 0, 0, 2, 0, 3, 5, 0, 0],
    [0, 0, 0, 5, 0, 0, 4, 9, 1],
    [0, 6, 0, 0, 0, 4, 0, 0, 3]
]

BOARD5 =  [
    [8, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 3, 6, 0, 0, 0, 0, 0],
    [0, 7, 0, 0, 9, 0, 2, 0, 0],
    [0, 5, 0, 0, 0, 7, 0, 0, 0],
    [0, 0, 0, 0, 4, 5, 7, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 3, 0],
    [0, 0, 1, 0, 0, 0, 0, 6, 8],
    [0, 0, 8, 5, 0, 0, 0, 1, 0],
    [0, 9, 0, 0, 0, 0, 4, 0, 0]
]

class Grid:
    def __init__(self, rows, cols, width, height, screen, difficulty):
        self.rows = rows
        self.cols = cols
        self.width = width
        self.height = height
        self.screen = screen
        self.difficulty = difficulty
        self.experiment = None
        if self.difficulty == 1:
            self.numbers = [[Number(BOARD1[i][j], i, j, width, height) for j in range(cols)] for i in range(rows)]
        elif self.difficulty == 3:
            self.numbers = [[Number(BOARD3[i][j], i, j, width, height) for j in range(cols)] for i in range(rows)]
        elif self.difficulty == 5:
            self.numbers = [[Number(BOARD5[i][j], i, j, width, height) for j in range(cols)] for i in range(rows)]
        self.update_experiment()

    def draw(self):
        #Draw grid
        gap = self.width / 9
        for i in range(self.rows+1):
            if i % 3 == 0 and i != 0:
                thick = 4
            else:
                thick = 1
            pygame.draw.line(self.screen, BLACK, (0, i*gap), (self.width, i*gap), thick)
            pygame.draw.line(self.screen, BLACK, (i * gap, 0), (i * gap, self.height), thick)
        
        #Draw numbers
        for i in range(self.rows):
            for j in range(self.cols):
                self.numbers[i][j].draw(self.screen)

    def solve(self):
        """
        Solves sudoku using backtracking
        """
        #Check if solved
        empty = next_cell(self.experiment)
        if not empty:
            self.finish()
            return True
        else:
            row, column = empty
        
        for i in range(1, 10):
            if check_action(self.experiment, i, (row, column)):
                self.experiment[row][column] = i
                self.numbers[row][column].set(i)
                self.numbers[row][column].change_number(self.screen, True)
                self.update_experiment()
                pygame.display.update()
                if self.difficulty == 1:
                    pygame.time.delay(90)
                elif self.difficulty == 3:
                    pygame.time.delay(10)

                if self.solve():
                    return True
                
                self.experiment[row][column] = 0
                self.numbers[row][column].set(0)
                self.update_experiment()
                self.numbers[row][column].change_number(self.screen, False)
                pygame.display.update()
                if self.difficulty == 1:
                    pygame.time.delay(90)
                elif self.difficulty == 3:
                    pygame.time.delay(10)

    def update_experiment(self):
        self.experiment = [[self.numbers[i][j].value for j in range(self.cols)] for i in range(self.rows)]

    def finish(self):
        pygame.draw.rect(self.screen, BLUE, (560, 90, 400, 60), 0)
        text1 = FONT.render("SOLVED!", 1 ,BLACK)
        text2 = FONT.render("Press DEL to go back", 1, BLACK)
        self.screen.blit(text1, (570, 100))
        self.screen.blit(text2, (570, 300))
        self.draw()
        pygame.display.update()


class Number:
    def __init__(self, value, row, col, width, height):
        self.value = value
        self.row = row
        self.col = col
        self.width = width
        self.height = height

    def set(self, value):
        self.value = value
    
    def draw(self, screen):
        cell_size = self.width / 9
        x = self.col * cell_size
        y = self.row * cell_size

        if self.value != 0:
            text = NUMBER_FONT.render(str(self.value), 1, BLACK)
            screen.blit(text, (x + (cell_size/2 - text.get_width()/2), y + (cell_size/2 - text.get_height()/2)))
    
    def change_number(self, screen, color):
        cell_size = self.width / 9
        x = self.col * cell_size
        y = self.row * cell_size

        pygame.draw.rect(screen, GRAY, (x, y, cell_size, cell_size), 0)
        text = NUMBER_FONT.render(str(self.value), 1, BLACK)
        screen.blit(text, (x + (cell_size/2 - text.get_width()/2), y + (cell_size/2 - text.get_height()/2)))
        if color:
            pygame.draw.rect(screen, (0, 255, 0), (x, y, cell_size, cell_size), 3)
        else:
            pygame.draw.rect(screen, (255, 0, 0), (x, y, cell_size, cell_size), 3)

def print_start_screen(screen):
    screen.fill(BLUE)
    pygame.draw.rect(screen, (255, 153, 51), (220, 50, 590, 450), 10)
    arial_40 = pygame.font.SysFont("arial", 40, bold=True)
    arial_20 = pygame.font.SysFont("arial", 20, bold=True)
    guide1 = FONT.render("Choose sudoku by pressing", 1, BLACK)
    guide2 = FONT.render("one of the keys listed below", 1, BLACK)
    simple = arial_40.render("(1) Simple", 1, BLACK)
    medium = arial_40.render("(3) Medium", 1, BLACK)
    hard = arial_40.render("(5) Hard*", 1, BLACK)
    info = arial_20.render("*Number five is titled to be the worlds hardest sudoku. Solving might take a while.", 1, BLACK)
    screen.blit(guide1, (250, 80))
    screen.blit(guide2, (250, 120))
    screen.blit(simple, (250, 300))
    screen.blit(medium, (250, 360))
    screen.blit(hard, (250, 420))
    screen.blit(info, (10, 550))
    pygame.display.update()

def update_screen(screen, board):
    text = FONT.render("Press SPACE to start!", 1, BLACK)
    screen.blit(text, (570, 100))
    board.draw()

def next_cell(board):
    """
    Return next empty spot on the board (row, col)
    """
    for i in range(ROWS):
        for j in range(COLS):
            if board[i][j] == 0:
                return (i, j)

    return None

def check_action(board, number, position):
    """
    Return True of False if the attempted move is valid or not
    """
    row_pos = position[0]
    column_pos = position[1]

    for i in range(ROWS):
        if board[row_pos][i] == number and column_pos != i:
            return False

    for i in range(COLS):
        if board[i][column_pos] == number and row_pos != i:
            return False

    #Corner position of current cell
    cell_x = column_pos // 3
    cell_y = row_pos // 3

    for i in range(cell_y*3, cell_y*3 + 3):
        for j in range(cell_x * 3, cell_x*3 + 3):
            if board[i][j] == number and (i,j) != position:
                return False

    return True


def main():
    start_screen = True
    finished = False
    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption(TITLE)
    key = 1
    sudoku = Grid(9, 9, 540, 540, screen, key)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    key = 1
                    start_screen = False
                if event.key == pygame.K_3:
                    key = 3
                    start_screen = False
                if event.key == pygame.K_5:
                    key = 5
                    start_screen = False
                if event.key == pygame.K_SPACE and start_screen == False:
                    pygame.draw.rect(screen, BLUE, (560, 90, 440, 60), 0)
                    text = FONT.render("Solving...", 1, BLACK)
                    screen.blit(text, (570, 100))
                    sudoku.solve()
                    finished = True
                if event.key == pygame.K_DELETE:
                    start_screen = True
                    finished = False

        if start_screen:
            print_start_screen(screen)
        elif not finished:
            sudoku = Grid(9, 9, 540, 540, screen, key)
            screen.fill(BLUE)
            pygame.draw.rect(screen, GRAY, (0, 0, 540, 540), 0)
            update_screen(screen, sudoku)
            pygame.display.update()

main()
pygame.quit()