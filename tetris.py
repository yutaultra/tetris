import pygame
import random

# 定数の定義
SCREEN_WIDTH, SCREEN_HEIGHT = 400, 600
GAME_WIDTH, GAME_HEIGHT = 300, 600
GRID_SIZE = 30
GRID_WIDTH, GRID_HEIGHT = GAME_WIDTH // GRID_SIZE, GAME_HEIGHT // GRID_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

SHAPES = [
    [[1, 1, 1, 1]], # I
    [[1, 1, 1],
     [0, 1, 0]],   # T
    [[1, 1],
     [1, 1]],      # O
    [[1, 1, 0],
     [0, 1, 1]],   # S
    [[0, 1, 1],
     [1, 1, 0]],   # Z
    [[1, 1, 1],
     [1, 0, 0]],   # L
    [[1, 1, 1],
     [0, 0, 1]]    # J
]

class Tetris:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Tetris")
        self.clock = pygame.time.Clock()
        self.grid = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]
        self.running = True
        self.current_piece = self.new_piece()
        self.next_piece = self.new_piece()
        self.current_piece_color = RED
        self.x, self.y = GRID_WIDTH // 2, 0
        self.last_fall_time = pygame.time.get_ticks()  # ピースが最後に落ちた時間
        self.fall_interval = 1000  # 1秒 (1000ミリ秒)
        self.score = 0

    def draw_3d_block(self, color, x_offset, y_offset):
        lighter_color = tuple(min(c + 50, 255) for c in color)
        darker_color = tuple(max(c - 50, 0) for c in color)

        pygame.draw.rect(self.screen, lighter_color, (x_offset, y_offset, GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(self.screen, darker_color, (x_offset + 2, y_offset + 2, GRID_SIZE - 4, GRID_SIZE - 4))
        pygame.draw.rect(self.screen, BLACK, (x_offset, y_offset, GRID_SIZE, GRID_SIZE), 2)

    def draw_text_with_shadow(self, text, font_name, color, x, y, shadow_offset=2):
        shadow_color = (0, 0, 0)
        font = pygame.font.SysFont(font_name, 24, bold=True)
        shadow_text = font.render(text, True, shadow_color)
        self.screen.blit(shadow_text, (x + shadow_offset, y + shadow_offset))
        text_surface = font.render(text, True, color)
        self.screen.blit(text_surface, (x, y))

    def draw_grid(self):
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                pygame.draw.rect(self.screen, BLACK, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
                if self.grid[y][x]:
                    self.draw_3d_block(self.grid[y][x], x * GRID_SIZE, y * GRID_SIZE)

    def draw_piece(self, piece, x_offset, y_offset, color):
        if piece:
            for dy, row in enumerate(piece):
                for dx, cell in enumerate(row):
                    if cell:
                        self.draw_3d_block(color, x_offset + dx * GRID_SIZE, y_offset + dy * GRID_SIZE)

    def draw_score(self):
        self.draw_text_with_shadow(f'Score: {self.score}', 'Arial', WHITE, GAME_WIDTH + 10, 20)

    def draw_next_piece(self):
        self.draw_text_with_shadow('Next:', 'Arial', WHITE, GAME_WIDTH + 10, 60)
        self.draw_piece(self.next_piece, GAME_WIDTH + 10, 90, RED)

    def draw_game_over(self):
        self.draw_text_with_shadow('Game Over', 'Arial', RED, SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 30)

    def new_piece(self):
        shape = random.choice(SHAPES)
        color = random.choice([RED, BLUE, GREEN, CYAN, MAGENTA, YELLOW, ORANGE])
        self.current_piece_color = color
        return shape

    def move_piece(self, dx, dy):
        self.x += dx
        self.y += dy
        if self.check_collision():
            self.x -= dx
            self.y -= dy
            return False
        return True

    def rotate_piece(self):
        if self.current_piece:
            original_piece = self.current_piece
            self.current_piece = [list(row) for row in zip(*self.current_piece[::-1])]
            if self.check_collision():
                self.current_piece = original_piece

    def check_collision(self):
        for dy, row in enumerate(self.current_piece):
            for dx, cell in enumerate(row):
                if cell:
                    x_pos = self.x + dx
                    y_pos = self.y + dy
                    if x_pos < 0 or x_pos >= GRID_WIDTH or y_pos >= GRID_HEIGHT or self.grid[y_pos][x_pos]:
                        return True
        return False

    def merge_piece(self):
        for dy, row in enumerate(self.current_piece):
            for dx, cell in enumerate(row):
                if cell:
                    self.grid[self.y + dy][self.x + dx] = self.current_piece_color

    def remove_lines(self):
        lines_to_remove = [i for i, row in enumerate(self.grid) if all(row)]
        for line in lines_to_remove:
            for _ in range(5):  # 点滅アニメーション
                pygame.draw.rect(self.screen, BLACK, (0, line * GRID_SIZE, GAME_WIDTH, GRID_SIZE))
                pygame.display.flip()
                pygame.time.wait(100)
                pygame.draw.rect(self.screen, WHITE, (0, line * GRID_SIZE, GAME_WIDTH, GRID_SIZE))
                pygame.display.flip()
                pygame.time.wait(100)
            self.grid.pop(line)
            self.grid.insert(0, [0] * GRID_WIDTH)
        self.score += len(lines_to_remove)

    def run(self):
        while self.running:
            current_time = pygame.time.get_ticks()
            self.screen.fill(BLACK)
            self.draw_grid()
            self.draw_piece(self.current_piece, self.x * GRID_SIZE, self.y * GRID_SIZE, self.current_piece_color)
            self.draw_score()
            self.draw_next_piece()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.move_piece(-1, 0)
                    elif event.key == pygame.K_RIGHT:
                        self.move_piece(1, 0)
                    elif event.key == pygame.K_DOWN:
                        self.move_piece(0, 1)
                    elif event.key == pygame.K_UP:
                        self.rotate_piece()

            if current_time - self.last_fall_time >= self.fall_interval:
                self.last_fall_time = current_time
                if not self.move_piece(0, 1):
                    self.merge_piece()
                    self.remove_lines()
                    self.current_piece = self.next_piece
                    self.next_piece = self.new_piece()
                    self.x, self.y = GRID_WIDTH // 2, 0
                    if self.check_collision():
                        self.draw_game_over()
                        pygame.display.flip()
                        pygame.time.wait(3000)  # 3秒間ゲームオーバー画面を表示
                        self.running = False

            pygame.display.flip()
            self.clock.tick(60)  # 60 FPSに設定

        pygame.quit()

if __name__ == "__main__":
    Tetris().run()
