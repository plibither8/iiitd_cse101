import os
import time
import random

class Color:
    BLACK = '\u001b[30;1m'
    RED = '\u001b[31;1m'
    GREEN = '\u001b[32;1m'
    YELLOW = '\u001b[33;1m'
    BLUE = '\u001b[34;1m'
    MAGENTA = '\u001b[35;1m'
    CYAN = '\u001b[36;1m'
    WHITE = '\u001b[37;1m'
    RESET = '\u001b[0m'

class Player:
    directions = {
        'R': [1, 0],
        'L': [-1, 0],
        'U': [0, -1],
        'D': [0, 1]
    }

    def moveUnit(self, dir_x, dir_y):
        # check for collision with obstacle  => game end (lose)
        # check for collision with goal => game end (win)
        # check for collision with reward => energy += reward
        # check for boundary collision => wrap around and reach other end
        # decrease energy => energy -= 1
        # 
        return True

    def makeMove(self, s):
        global grid
        grid.showGrid()
        time.sleep(0.4)
        commands = [s[i:i+2] for i in range(0, len(s), 2)]

        if not commands:
            return

        active_command = commands[0]
        active_command_type, active_command_length = list(active_command)
        active_command_length = int(active_command_length)

        permitted_move_types = list(self.directions.keys())
        permitted_rotate_types = ['A', 'C']

        valid_move = False

        if active_command_type in permitted_move_types:
            if self.moveUnit(*self.directions[active_command_type]):
                valid_move = True
        elif active_command_type in permitted_rotate_types:
            if active_command_type is 'C':
                if grid.rotateClockwise(active_command_length) is not -1:
                    valid_move = True
            else:
                if grid.rotateAntiClockwise(active_command_length) is not -1:
                    valid_move = True

        if valid_move:
            active_command_length -= 1
            commands = [active_command_type + str(active_command_length)] + commands[1:]

            if active_command_length is 0:
                commands = commands[1:]

            self.makeMove(''.join(commands))

    def __init__(self, x_index, y_index, N):
        self.x = x_index
        self.y = y_index
        self.type = 1
        self.energy = 2 * N


class Goal:
    def __init__(self, x_index, y_index):
        self.x = x_index
        self.y = y_index
        self.type = 2


class Reward:
    def __init__(self, x_index, y_index):
        self.x = x_index
        self.y = y_index
        self.type = 3
        self.value = random.randint(1, 9)


class Obstacle:
    def __init__(self, x_index, y_index):
        self.x = x_index
        self.y = y_index
        self.type = 4


class Grid:
    def findCellFromCoords(self, i, j):
        all_occupied_cells = self.myObstacles + self.myRewards + [player, grid_goal]
        return next((cell for cell in all_occupied_cells if (cell.x, cell.y) == (i, j)), None)

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
        boundary_coord_list = list(filter(lambda cell: set(cell).intersection(set([0, self.N - 1])), coord_list))
        return boundary_coord_list

    def rotateClockwise(self, rotation_factor):
        player.energy -= self.N // 3
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

    def updateGrid(self):
        for i in range(self.N):
            for j in range(self.N):
                required_cell = self.findCellFromCoords(i, j)
                if required_cell:
                    self.grid[i][j] = required_cell.type if required_cell.type is not 3 else '+' + str(random.randint(1, 9))
                else:
                    self.grid[i][j] = 0


    def showGrid(self):
        cell_details = {
            0: {
                'graphic': '•',
                'color': Color.WHITE
            },
            1: {
                'graphic': '◼',
                'color': Color.BLUE
            },
            2: {
                'graphic': '🏁',
                'color': Color.GREEN
            },
            4: {
                'graphic': '#',
                'color': Color.RED
            }
        }

        os.system('clear')

        print(Color.YELLOW + 'ENERGY: ' + str(player.energy) + Color.RESET)
        print()
        for row in self.grid:
            for cell in row:
                cell_graphic = cell[1] if isinstance(cell, str) else cell_details[cell]['graphic']
                cell_color = Color.YELLOW if isinstance(cell, str) else cell_details[cell]['color']
                print("\u001b[47" + cell_color + ' ' + cell_graphic + Color.RESET, end='', flush=True)
            print()

    def __init__(self, N):
        self.N = N
        self.grid = [[0] * N for _ in range(N)]

        boundary_coords = self.getBoundryCellCoordinates()
        self.start, self.goal = random.sample(boundary_coords, 2)

        global player, grid_goal
        player = Player(*self.start, self.N)
        grid_goal = Goal(*self.goal)

        self.occupied_coords = []

        obstacles = random.sample(self.getFreeCellCoordinates(), self.N)
        self.myObstacles = list(map(lambda cell: Obstacle(*cell), obstacles))
        self.occupied_coords += obstacles

        rewards = random.sample(self.getFreeCellCoordinates(), self.N)
        self.myRewards = list(map(lambda cell: Reward(*cell), rewards))
        self.occupied_coords += rewards

        self.updateGrid()
        self.showGrid()

# take input n = input()
GRID_SIZE = 10

grid = Grid(GRID_SIZE)
player.makeMove("R4L5A2")
