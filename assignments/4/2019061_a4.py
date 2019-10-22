import os
import time
import random

class Player:
    def makeMove(self, s):
        pass

    def __init__(self, x_index, y_index, N):
        self.x = x_index
        self.y = y_index
        self.energy = 2 * N


class Goal:
    def __init__(self, x_index, y_index):
        self.x = x_index
        self.y = y_index


class Reward:
    def __init__(self, x_index, y_index):
        self.x = x_index
        self.y = y_index
        self.value = random.randint(1, 9)


class Obstacle:
    def __init__(self, x_index, y_index):
        self.x = x_index
        self.y = y_index


class Grid:
    def getCellCoordinates(self):
        coord_list = []
        for i in range(self.N):
            for j in range(self.N):
                coord_list.append((i, j))
        return coord_list

    def getFreeCellCoordinates(self):
        extended_occupied_coords = self.occupied_coords + [(player.x, player.y), self.goal]
        return list(filter(lambda coord: coord not in extended_occupied_coords, self.getCellCoordinates()))

    def getBoundryCellCoordinates(self):
        coord_list = self.getCellCoordinates()
        boundry_coord_list = list(filter(lambda cell: set(cell).intersection(set([0, self.N - 1])), coord_list))
        return boundry_coord_list

    def rotateClockwise(self, rotation_factor):
        real_rotation_factor = rotation_factor % 4

        if real_rotation_factor is 0:
            pass  # Don't do anything

        elif real_rotation_factor is 1:
            for k in range(len(self.occupied_coords)):
                i, j = self.occupied_coords[k]
                proposed_cell = (j, self.N - i)
                if proposed_cell is (player.x, player.y): return -1
                self.occupied_coords[k] = proposed_cell

        elif real_rotation_factor is 2:
            for k in range(len(self.occupied_coords)):
                i, j = self.occupied_coords[k]
                proposed_cell = (self.N - i, self.N - j)
                if proposed_cell is (player.x, player.y): return -1
                self.occupied_coords[k] = proposed_cell

        else:
            for k in range(len(self.occupied_coords)):
                i, j = self.occupied_coords[k]
                proposed_cell = (self.N - j, i)
                if proposed_cell is (player.x, player.y): return -1
                self.occupied_coords[k] = proposed_cell

        return 0

    def rotateAntiClockwise(self, rotation_factor):
        return self.rotateClockwise(-rotation_factor)

    def showGrid(self):
        pass

    def __init__(self, N):
        self.N = N
        self.grid = [[ None ] * N] * N

        boundry_coords = self.getBoundryCellCoordinates()
        self.start, self.goal = random.sample(boundry_coords, 2)

        global player
        player = Player(*self.start, self.N)

        self.occupied_coords = []

        obstacles = random.sample(self.getFreeCellCoordinates(), self.N)
        self.myObstacles = list(map(lambda cell: Obstacle(*cell), obstacles))
        self.occupied_coords += obstacles

        rewards = random.sample(self.getFreeCellCoordinates(), self.N)
        self.myRewards = list(map(lambda cell: Reward(*cell), rewards))
        self.occupied_coords += rewards


# take input n = input()
GRID_SIZE = 10

grid = Grid(GRID_SIZE)
