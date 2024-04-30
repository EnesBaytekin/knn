import pygame
from pygame.locals import *

from knn import KNN, get_data

# Ekran boyutu ve renk tanımları
WIDTH, HEIGHT = 400, 400
BACKGROUND_COLOR = (255, 255, 255)
LINE_COLOR = (0, 0, 0)
GRID_SIZE = 4
CELL_SIZE = WIDTH // GRID_SIZE

# Sınıf etiketleri
class_labels = ["T Shape", "Square Block", "L Shape", "Line Block", "S Shape"]

# Grid oluşturma
grid = [[192 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

X, Y = get_data()

def main():
    global selected_color
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Image Editor")
    clock = pygame.time.Clock()

    dragging_slider = False
    slider_x = 50
    selected_color = 0
    left_color = 0

    drawing = False

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return

            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:  # Sol tuşa basıldığında
                    x, y = event.pos
                    if 10 <= x <= 230 and 10 <= y <= 30:
                        slider_x = max(10, min(x-10, 210))
                        selected_color = int((slider_x - 10) / 200 * 255)
                        left_color = selected_color
                        dragging_slider = True
                        drawing = False
                    elif 0 <= x <= WIDTH and 0 <= y <= HEIGHT:
                        drawing = True
                        row = y // CELL_SIZE
                        col = x // CELL_SIZE
                        grid[row][col] = selected_color
                if event.button == 3:  # Sağ tuşa basıldığında
                    drawing = True
                    row = y // CELL_SIZE
                    col = x // CELL_SIZE
                    grid[row][col] = 192
                    selected_color = 192

            if event.type == MOUSEBUTTONUP:
                if event.button == 1:  # Sol tuş bırakıldığında
                    dragging_slider = False
                    drawing = False
                if event.button == 3:  # Sağ tuş bırakıldığında
                    selected_color = left_color
                    dragging_slider = False
                    drawing = False

            if event.type == MOUSEMOTION:
                x, y = event.pos
                if dragging_slider:
                    slider_x = max(10, min(x-10, 210))
                    selected_color = int((slider_x - 10) / 200 * 255)
                    left_color = selected_color
                if drawing:
                    row = min(max(y, 0), HEIGHT-1) // CELL_SIZE
                    col = min(max(x, 0), WIDTH-1) // CELL_SIZE
                    grid[row][col] = selected_color

            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    # Resmi tahmin etme
                    input_data = []
                    for i in range(4):
                        input_data.extend(grid[i])
                    predicted_class = predict_single_sample(input_data)
                    # class_name = class_labels[predicted_class]
                    class_name = predicted_class
                    pygame.display.set_caption(class_name)

        screen.fill(BACKGROUND_COLOR)
        draw_grid(screen)
        draw_slider(screen, slider_x)
        pygame.display.flip()
        clock.tick(60)

def draw_grid(screen):
    # Satırları çizme
    for row in range(GRID_SIZE + 1):
        pygame.draw.line(screen, LINE_COLOR, (0, row * CELL_SIZE), (WIDTH, row * CELL_SIZE))

    # Sütunları çizme
    for col in range(GRID_SIZE + 1):
        pygame.draw.line(screen, LINE_COLOR, (col * CELL_SIZE, 0), (col * CELL_SIZE, HEIGHT))

    # Hücreleri boyama
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            cell_color = (grid[row][col], grid[row][col], grid[row][col])
            pygame.draw.rect(screen, cell_color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def draw_slider(screen, x):
    pygame.draw.rect(screen, LINE_COLOR, (20, 12, 200, 16))
    pygame.draw.rect(screen, (0, 0, 0), (x, 10, 20, 20))
    pygame.draw.rect(screen, (192, 192, 192), (x+1, 11, 18, 18))

def predict_single_sample(input_data):
    # Veriyi gerekli şekle dönüştürme

    # Veriyi tahmin etme
    prediction = KNN(X, Y, input_data, k=5)
    

    return prediction

if __name__ == "__main__":
    main()
