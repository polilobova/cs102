import pathlib
import random
import typing as tp
from copy import deepcopy

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self,
        size: tp.Tuple[int, int],
        randomize: bool = True,
        max_generations: tp.Optional[float] = float("inf"),
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

    def create_grid(self, randomize: bool = False) -> Grid:
        if randomize:
            grid = [[random.randint(0, 1) for i in range(self.rows)] for j in range(self.cols)]
        else:
            grid = [[0 for i in range(self.rows)] for j in range(self.cols)]
        return grid

    def get_neighbours(self, cell: Cell) -> Cells:
        cells = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                y = cell[0] + i
                x = cell[1] + j
                if i == 0 and j == 0:
                    continue
                elif (-1 < y < self.rows) and (-1 < x < self.cols):
                    cells.append(self.curr_generation[y][x])
        return cells

    def get_next_generation(self) -> Grid:
        new_grid = deepcopy(self.curr_generation)
        for row in range(self.rows):
            for col in range(self.cols):
                cell = (row, col)
                alive_neighbours = sum(self.get_neighbours(cell))
                if alive_neighbours in (2, 3) and self.curr_generation[row][col] == 1:
                    new_grid[row][col] = 1
                elif alive_neighbours == 3 and self.curr_generation[row][col] == 0:
                    new_grid[row][col] = 1
                else:
                    new_grid[row][col] = 0
        return new_grid

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        self.prev_generation = deepcopy(self.curr_generation)
        self.curr_generation = self.get_next_generation()
        self.generations += 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        if self.max_generations is not None:
            return float(self.generations) >= self.max_generations
        return False

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        grid = self.curr_generation
        flag = True
        for y in range(len(grid)):
            for x in range(len(grid[0])):
                if grid[y][x] == 1:
                    flag = False
                    break
        if flag:
            return False
        return grid != self.prev_generation

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        """
        Прочитать состояние клеток из указанного файла.
        """
        f = open(filename)
        lines = f.readlines()
        grid = list()
        width, height = 0, 0
        for line in lines:
            to_append = list(map(int, list(line.strip())))
            height += 1
            if width == 0:
                width = len(to_append)
            grid.append(to_append)
        new_grid = GameOfLife((height, width))
        new_grid.curr_generation = grid
        return new_grid

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        with open(filename, "w") as f:
            for i in range(len(self.curr_generation)):
                print("".join(map(str, self.curr_generation[i])), end="\n", file=f)
