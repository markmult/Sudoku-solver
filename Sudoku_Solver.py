import pygame
import time

pygame.init()

TITLE = "Sudoku Solver"
SIZE = (1000, 600)
WHITE = (255,255,255)
BLUE = (51,204,255)
BLACK = (0,0,0)
ROWS = 9
COLS = 9
ARIAL_40 = pygame.font.SysFont("arial", 40, bold=True)
ARIAL_20 = pygame.font.SysFont("arial", 20, bold=True)
NUMBER_FONT = pygame.font.SysFont("comicsans", 40)

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
        if self.value != 0:
            cell_size = self.width / COLS
            cell_x = self.col * cell_size
            cell_y = self.row * cell_size
            text = NUMBER_FONT.render(str(self.value), 1, WHITE)

            text_pos_x = cell_x + (cell_size/2 - text.get_width()/2)
            text_pos_y = cell_y + (cell_size/2 - text.get_height()/2)
            screen.blit(text, (text_pos_x, text_pos_y))
        
    def change_number(self, screen, color):
        cell_size = self.width / COLS
        cell_x = self.col * cell_size
        cell_y = self.row * cell_size
        pygame.draw.rect(screen, BLACK, (cell_x, cell_y, cell_size, cell_size), 0)
        text = NUMBER_FONT.render(str(self.value), 1, WHITE)

        text_pos_x = cell_x + (cell_size/2 - text.get_width()/2)
        text_pos_y = cell_y + (cell_size/2 - text.get_height()/2)
        screen.blit(text, (text_pos_x, text_pos_y))

        if color:
            pygame.draw.rect(screen, (0, 255, 0), (cell_x, cell_y, cell_size, cell_size), 3)
        else:
            pygame.draw.rect(screen, (255, 0, 0), (cell_x, cell_y, cell_size, cell_size), 3)


class Grid:
    def __init__(self, rows, cols, width, height, screen, difficulty):
        self.iterations = 0
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

    def draw_board(self):
        """
        Draws grid and numbers to screen
        """
        cell_size = self.width / ROWS
        for i in range(self.rows+1):
            if i % 3 == 0:
                line_thickness = 4
            else:
                line_thickness = 1
            pygame.draw.line(self.screen, WHITE, (0, i*cell_size), (self.width, i*cell_size), line_thickness)
            pygame.draw.line(self.screen, WHITE, (i*cell_size, 0), (i*cell_size, self.height), line_thickness)
        
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
            self.iterations += 1

        #Try numbers from 1 to 9
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
        arial_30 = pygame.font.SysFont("arial", 30, bold=True)
        text1 = ARIAL_40.render("SOLVED!", 1 ,BLACK)
        text2 = arial_30.render(str(self.iterations) + " iterations", 1, BLACK)
        text3 = arial_30.render("Press DEL to go back", 1, BLACK)
        self.screen.blit(text1, (570, 100))
        self.screen.blit(text2, (570, 180))
        self.screen.blit(text3, (570, 400))
        self.draw_board()
        pygame.display.update()


def print_start_screen(screen):
    screen.fill(BLUE)
    pygame.draw.rect(screen, (255, 153, 51), (220, 50, 590, 450), 10)
    guide1 = ARIAL_40.render("Choose sudoku by pressing", 1, BLACK)
    guide2 = ARIAL_40.render("one of the keys listed below", 1, BLACK)
    simple = ARIAL_40.render("(1) Simple", 1, BLACK)
    medium = ARIAL_40.render("(3) Medium", 1, BLACK)
    hard = ARIAL_40.render("(5) Hard*", 1, BLACK)
    info = ARIAL_20.render("*Number five is titled to be the worlds hardest sudoku. Solving might take a while.", 1, BLACK)
    screen.blit(guide1, (250, 80))
    screen.blit(guide2, (250, 120))
    screen.blit(simple, (250, 300))
    screen.blit(medium, (250, 360))
    screen.blit(hard, (250, 420))
    screen.blit(info, (10, 550))
    pygame.display.update()

def update_screen(screen, board):
    text = ARIAL_40.render("Press SPACE to start!", 1, BLACK)
    screen.blit(text, (570, 100))
    board.draw_board()

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
    
    #Check if there is same number in current row or column
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
                    text = ARIAL_40.render("Solving...", 1, BLACK)
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
            pygame.draw.rect(screen, BLACK, (0, 0, 540, 540), 0)
            update_screen(screen, sudoku)
            pygame.display.update()

main()
pygame.quit()