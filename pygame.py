import pygame
import random

WINDOW_WIDTH = 480
WINDOW_HEIGHT = 480
BOARD_SIZE = 8
CELL_SIZE = 60

BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

def draw_board(screen):
    screen.fill(WHITE)
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if row % 2 == col % 2:
                color = GREEN
            else:
                color = BLUE
            pygame.draw.rect(screen, color, [col*CELL_SIZE, row*CELL_SIZE, CELL_SIZE, CELL_SIZE])

def draw_queens(screen, board):
    queen_image = pygame.image.load("queen.png").convert_alpha()
    for row in range(BOARD_SIZE):
        col = board[row]
        screen.blit(queen_image, [col*CELL_SIZE, row*CELL_SIZE])

def fitness(board):
    attacks = 0
    for i in range(len(board)):
        for j in range(i+1,len(board)):
            if board[i] == board[j]:
                attacks += 1
            offset = j - i
            if board[i] == board[j] - offset or board[i] == board[j] + offset:
                attacks += 1
    return attacks

def generate_board(size):
    board = [0]*size
    for i in range(size):
        board[i] = random.randint(0,size-1)
    return board

def crossover(board1,board2):
    size = len(board1)
    new_board = [0]*size
    for i in range(size):
        if i < size/2:
            new_board[i] = board1[i]
        else:
            new_board[i] = board2[i]
    return new_board

def mutate(board):
    size = len(board)
    new_board = list(board)
    new_board[random.randint(0,size-1)] = random.randint(0,size-1)
    return new_board

def evolve(population):
    new_population = []
    for i in range(len(population)):
        board1 = population[random.randint(0,len(population)-1)]
        board2 = population[random.randint(0,len(population)-1)]
        child = crossover(board1,board2)
        if random.random() < 0.1:
            child = mutate(child)
        new_population.append(child)
    return new_population

def genetic_algorithm(size,population_size,max_generations):
    population = [generate_board(size) for i in range(population_size)]
    for i in range(max_generations):
        population = sorted(population,key=lambda x:fitness(x))
        if fitness(population[0]) == 0:
            return population[0]
        population = evolve(population)
    return None

def main():
    pygame.init()
    screen = pygame.display.set_mode([WINDOW_WIDTH, WINDOW_HEIGHT])
    pygame.display.set_caption("8 Queens")

    queen_image = pygame.image.load("queen.png").convert_alpha()
    queen_image = pygame.transform.scale(queen_image, (CELL_SIZE, CELL_SIZE))

    font = pygame.font.SysFont(None, 30)

    done = False
    generation_count = 0
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        
        solution = genetic_algorithm(BOARD_SIZE,100,1000)
        if solution is not None:
            print("Solution found: ",solution)
            done = True
        
        draw_board(screen)
        draw_queens(screen, solution)
        text = font.render("Generation: "+str(generation_count), True, BLACK)
        screen.blit(text, [10, WINDOW_HEIGHT-40])
        pygame.display.flip()
        generation_count += 1

    pygame.quit()

if __name__ == "__main__":
    main()
