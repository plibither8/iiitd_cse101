import os # Clear terminal screen
import time # Wait and print grid
import random # Generate and receive random coords

def clear_screen():
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
        self.value = -4

class Visited:
    def __init__(self, x_index, y_index):
        self.x = x_index
        self.y = y_index
        self.type = 5

class Player:
    directions = {
        'R': [0, 1],
        'L': [0, -1],
        'U': [-1, 0],
        'D': [1, 0]
    }

    def move_unit(self, dir_x, dir_y):
        global game_win

        old_coords = self.x, self.y
        new_coords = (self.x + dir_x) % grid.N, (self.y + dir_y) % grid.N
        self.x, self.y = new_coords
        self.energy -= 1

        if old_coords not in grid.cell_to_coords_list(grid.visited_cells):
            grid.visited_cells.append(Visited(*old_coords))

        if new_coords == grid.goal:
            game_win = True
            return

        def check_collision(cell_list):
            cell_index = next((i for i, coords in enumerate(grid.cell_to_coords_list(cell_list)) if coords == new_coords), -1)
            if cell_index is not -1:
                current_cell = cell_list[cell_index]
                self.energy += current_cell.value * grid.N
                del cell_list[cell_index]
                return

        check_collision(grid.myObstacles)
        check_collision(grid.myRewards)

    def makeMove(self, s):
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
        active_command_type, active_command_length = active_command[0], int(active_command[1:])

        valid_move = False

        if active_command_type in permitted_move_types and self.energy > 0:
            self.move_unit(*self.directions[active_command_type])
            valid_move = True

        elif active_command_type in permitted_rotate_types and self.energy >= grid.N // 3:
            if active_command_type is 'C' and grid.rotateClockwise(active_command_length):
                valid_move = True

            elif active_command_type is 'A' and grid.rotateAntiClockwise(active_command_length):
                valid_move = True

        if valid_move:
            grid.update_grid()
            grid.showGrid()
            time.sleep(0.5)

            active_command_length = active_command_length - 1 if active_command_type in permitted_move_types else 0
            commands = ([] if active_command_length is 0 else [active_command_type + str(active_command_length)]) + commands[1:]

            self.remaining_moves = ''.join(commands)
            return self.makeMove(self.remaining_moves)

        return False

    def __init__(self, x_index, y_index, N):
        self.x = x_index
        self.y = y_index
        self.type = 1
        self.energy = 2 * N
        self.remaining_moves = ''

class Grid:
    def cell_to_coords_list(self, cells):
        return list(map(lambda cell: (cell.x, cell.y), cells))

    def get_cell_coordinates(self):
        coords_list = []
        for i in range(self.N):
            for j in range(self.N):
                coords_list.append((i, j))
        return coords_list

    def get_free_cell_coordinates(self):
        all_occupied_coords = self.cell_to_coords_list(self.myObstacles + self.myRewards + [player, grid_goal])
        return list(filter(lambda coords: coords not in all_occupied_coords, self.get_cell_coordinates()))

    def get_boundry_cell_coordinates(self):
        coords_list = self.get_cell_coordinates()
        boundary_coords_list = list(filter(lambda cell: set(cell).intersection(set([0, self.N - 1])), coords_list))
        return boundary_coords_list

    def rotateClockwise(self, rotation_factor):
        real_rotation_factor = rotation_factor % 4

        def new_coords(i, j):
            if real_rotation_factor is 0: return (i, j)
            if real_rotation_factor is 1: return (j, self.N - i -1)
            if real_rotation_factor is 2: return (self.N - i - 1, self.N - j - 1)
            return (self.N - j - 1, i)

        def change_coordinates(cell):
            proposed_coords = new_coords(cell.x, cell.y)
            cell.x, cell.y = proposed_coords
            if cell.type is 4 and proposed_coords in self.cell_to_coords_list([player, grid_goal]): return False
            return cell

        self.myObstacles[:] = map(change_coordinates, self.myObstacles)
        self.myRewards[:] = map(change_coordinates, self.myRewards)
        self.visited_cells[:] = map(change_coordinates, self.visited_cells)

        if False in self.myRewards + self.myObstacles:
            print(Color.RED + 'Grid cannot be rotated!' + Color.RESET)
            return False
        else:
            player.energy -= self.N // 3
            return True

    def rotateAntiClockwise(self, rotation_factor):
        return self.rotateClockwise(-rotation_factor)

    def update_grid(self):
        all_occupied_cells = [player, grid_goal] + self.myObstacles + self.myRewards + self.visited_cells

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
                'graphic': 'O',
                'color': Color.BLUE
            },
            2: {
                'graphic': '@',
                'color': Color.GREEN
            },
            4: {
                'graphic': '#',
                'color': Color.RED
            },
            5: {
                'graphic': 'X',
                'color': Color.WHITE
            }
        }

        clear_screen()
        print(Color.YELLOW + 'ENERGY: ' + str(player.energy) + Color.RESET + '\n')

        for row in self.grid:
            for cell in row:
                is_reward_cell = isinstance(cell, str)
                cell_graphic = cell[1] if is_reward_cell else cell_details[cell]['graphic']
                cell_color = Color.YELLOW if is_reward_cell else cell_details[cell]['color']

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
        self.visited_cells = []

        boundary_coords = self.get_boundry_cell_coordinates()
        self.start, self.goal = random.sample(boundary_coords, 2)

        global player, grid_goal, game_win
        player = Player(*self.start, self.N)
        grid_goal = Goal(*self.goal)
        game_win = False

        obstacles = random.sample(self.get_free_cell_coordinates(), self.N)
        self.myObstacles[:] = map(lambda coords: Obstacle(*coords), obstacles)

        rewards = random.sample(self.get_free_cell_coordinates(), self.N)
        self.myRewards[:] = map(lambda coords: Reward(*coords), rewards)

        self.update_grid()


clear_screen()
print(Color.BLUE + 'Welcome to GridWorld!' + Color.RESET + '\n')
GRID_SIZE = int(input(Color.YELLOW + 'Enter grid size: ' + Color.GREEN))
clear_screen()

grid = Grid(GRID_SIZE)
grid.showGrid()

player.remaining_moves = input('\n' + Color.YELLOW + 'Enter move: ' + Color.GREEN).upper()
final_result = player.makeMove(player.remaining_moves)

grid.showGrid()

if final_result and game_win:
    print(Color.GREEN + 'YOU WON!' + Color.RESET)
else:
    print(Color.RED + 'YOU LOST!' + Color.RESET)
