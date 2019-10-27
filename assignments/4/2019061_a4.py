import os # Clear terminal screen
import time # Wait and print grid
import random # Generate and receive random coords

def clearScreen():
    os.system('clear' if os.name is 'posix' else 'cls')

class Color:
    RED = '\u001b[31;1m'
    GREEN = '\u001b[32;1m'
    YELLOW = '\u001b[33;1m'
    BLUE = '\u001b[34;1m'
    MAGENTA = '\u001b[35;1m'
    WHITE = '\u001b[37;1m'
    RESET = '\u001b[0m'

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

class Player:
    directions = {
        'R': [0, 1],
        'L': [0, -1],
        'U': [-1, 0],
        'D': [1, 0]
    }

    def moveUnit(self, dir_x, dir_y):
        global game_win

        new_coords = (player.x + dir_x) % grid.N, (player.y + dir_y) % grid.N
        self.x, self.y = new_coords
        self.energy -= 1

        if new_coords == grid.goal:
            game_win = True
            return

        if new_coords in grid.cellToCoordsList(grid.myObstacles):
            for i in range(len(grid.myObstacles)):
                obstacle_cell = grid.myObstacles[i]
                if new_coords == (obstacle_cell.x, obstacle_cell.y):
                    self.energy -= 4 * grid.N
                    del grid.myObstacles[i]
                    return

        if new_coords in grid.cellToCoordsList(grid.myRewards):
            for i in range(len(grid.myRewards)):
                reward_cell = grid.myRewards[i]
                if new_coords == (reward_cell.x, reward_cell.y):
                    self.energy += reward_cell.value * grid.N
                    del grid.myRewards[i]
                    return

    def makeMove(self, s):
        self.remaining_moves = s

        permitted_move_types = list(self.directions.keys())
        permitted_rotate_types = ['A', 'C']

        commands = []
        for char in s:
            if char in permitted_move_types + permitted_rotate_types:
                commands.append(char)
            else:
                commands[-1] += char

        if not commands: return True
        if game_win: return True

        active_command = commands[0]
        active_command_type, active_command_length = active_command[0], active_command[1:]
        active_command_length = int(active_command_length)

        valid_move = False

        if active_command_type in permitted_move_types and self.energy > 0:
            self.moveUnit(*self.directions[active_command_type])
            valid_move = True

        elif active_command_type in permitted_rotate_types and self.energy >= grid.N // 3:
            if active_command_type is 'C' and grid.rotateClockwise(active_command_length):
                valid_move = True

            elif active_command_type is 'A' and grid.rotateAntiClockwise(active_command_length):
                valid_move = True

        if valid_move:
            grid.updateGrid()
            grid.showGrid()
            time.sleep(0.5)

            active_command_length = active_command_length - 1 if active_command_type in permitted_move_types else 0
            commands = ([] if active_command_length is 0 else [active_command_type + str(active_command_length)]) + commands[1:]
            return self.makeMove(''.join(commands))

        return False

    def __init__(self, x_index, y_index, N):
        self.x = x_index
        self.y = y_index
        self.type = 1
        self.energy = 2 * N
        self.remaining_moves = ''

class Grid:
    def cellToCoordsList(self, cells):
        return list(map(lambda cell: (cell.x, cell.y), cells))

    def getCellCoordinates(self):
        coord_list = []
        for i in range(self.N):
            for j in range(self.N):
                coord_list.append((i, j))
        return coord_list

    def getFreeCellCoordinates(self):
        all_occupied_coords = self.cellToCoordsList(self.myObstacles + self.myRewards + [player, grid_goal])
        return list(filter(lambda coords: coords not in all_occupied_coords, self.getCellCoordinates()))

    def getBoundryCellCoordinates(self):
        coord_list = self.getCellCoordinates()
        boundary_coord_list = list(filter(lambda cell: set(cell).intersection(set([0, self.N - 1])), coord_list))
        return boundary_coord_list

    def rotateClockwise(self, rotation_factor):
        player.energy -= self.N // 3
        real_rotation_factor = rotation_factor % 4

        def new_coords(i, j):
            if real_rotation_factor is 0: return (i, j)
            if real_rotation_factor is 1: return (j, self.N - i -1)
            if real_rotation_factor is 2: return (self.N - i - 1, self.N - j - 1)
            return (self.N - j - 1, i)

        def changeCoordinates(cell):
            proposed_coords = new_coords(cell.x, cell.y)
            cell.x, cell.y = proposed_coords
            if cell.type is 4 and proposed_coords in self.cellToCoordsList([player, grid_goal]): return False
            return cell

        self.myObstacles[:] = map(changeCoordinates, self.myObstacles)
        self.myRewards[:] = map(changeCoordinates, self.myRewards)

        if False in self.myRewards + self.myObstacles:
            print(Color.RED + 'Grid cannot be rotated!' + Color.RESET)
            return False
        else:
            return True

    def rotateAntiClockwise(self, rotation_factor):
        return self.rotateClockwise(-rotation_factor)

    def updateGrid(self):
        all_occupied_cells = self.myObstacles + self.myRewards + [player, grid_goal]

        for i in range(self.N):
            for j in range(self.N):
                required_cell = next((cell for cell in all_occupied_cells if (cell.x, cell.y) == (i, j)), None)

                if required_cell:
                    self.grid[i][j] = required_cell.type if required_cell.type is not 3 else '+' + str(required_cell.value)
                else:
                    self.grid[i][j] = 0

    def showGrid(self):
        cell_details = {
            0: {
                'graphic': '•',
                'color': Color.WHITE
            },
            1: {
                'graphic': 'O',  # ◼
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

        clearScreen()
        print(Color.YELLOW + 'ENERGY: ' + str(player.energy) + Color.RESET + '\n')
        for row in self.grid:
            for cell in row:
                cell_graphic = cell[1] if isinstance(cell, str) else cell_details[cell]['graphic']
                cell_color = Color.YELLOW if isinstance(cell, str) else cell_details[cell]['color']
                print('\u001b[47' + cell_color + ' ' + cell_graphic + Color.RESET, end='', flush=True)
            print()
        print()
        if not game_win:
            print(Color.MAGENTA + player.remaining_moves + Color.RESET)

    def __init__(self, N):
        self.N = N
        self.grid = [[0] * N for _ in range(N)]
        self.myObstacles = []
        self.myRewards = []

        boundary_coords = self.getBoundryCellCoordinates()
        self.start, self.goal = random.sample(boundary_coords, 2)

        global player, grid_goal, game_win
        player = Player(*self.start, self.N)
        grid_goal = Goal(*self.goal)
        game_win = False

        obstacles = random.sample(self.getFreeCellCoordinates(), self.N)
        self.myObstacles[:] = map(lambda coords: Obstacle(*coords), obstacles)

        rewards = random.sample(self.getFreeCellCoordinates(), self.N)
        self.myRewards[:] = map(lambda coords: Reward(*coords), rewards)

        self.updateGrid()


clearScreen()
print(Color.BLUE + 'Welcome to GridWorld!' + Color.RESET + '\n')
GRID_SIZE = int(input(Color.YELLOW + 'Enter grid size: ' + Color.GREEN))
clearScreen()

grid = Grid(GRID_SIZE)
grid.showGrid()

user_move = input('\n' + Color.YELLOW + 'Enter move: ' + Color.GREEN).upper()
player.remaining_moves = user_move
final_result = player.makeMove(user_move)

grid.showGrid()

if final_result and game_win:
    print(Color.GREEN + 'YOU WON!' + Color.RESET)
else:
    print(Color.RED + 'YOU LOST!' + Color.RESET)
