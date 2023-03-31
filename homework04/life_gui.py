import pygame
from life import GameOfLife
from pygame.locals import *
from ui import UI


class GUI(UI):
    def __init__(self, life: GameOfLife, cell_size: int = 10, speed: int = 10) -> None:
        super().__init__(life)
        self.cell_size = cell_size
        self.speed = speed
        self.width = cell_size * self.life.cols
        self.height = cell_size * self.life.rows
        self.screen_size = (self.width, self.height)
        self.screen = pygame.display.set_mode(self.screen_size)

    def draw_lines(self) -> None:
        """Отрисовать сетку"""
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def draw_grid(self) -> None:
        """
        Отрисовка списка клеток с закрашиванием их в соответствующе цвета.
        """
        grid = self.grid
        for y in range(self.height):
            for x in range(self.width):
                if grid[y][x] == 0:
                    pygame.draw.rect(
                        self.screen,
                        pygame.Color("white"),
                        (self.cell_size * x, self.cell_size * y, self.cell_size, self.cell_size),
                    )
                else:
                    pygame.draw.rect(
                        self.screen,
                        pygame.Color("green"),
                        (self.cell_size * x, self.cell_size * y, self.cell_size, self.cell_size),
                    )

    def change_status(self) -> None:
        x, y = pygame.mouse.get_pos()
        row = y // self.cell_size
        col = x // self.cell_size
        self.grid[row][col] = (self.grid[row][col] + 1) % 2

    def run(self) -> None:
        """Запустить игру"""
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))
        self.grid = self.life.curr_generation
        running = True
        pause = False


if __name__ == "__main__":
    life = GameOfLife((20, 30), True, max_generations=200)
    gui = GUI(life, 15, 15)
    gui.run()
