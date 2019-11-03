import os      # Clear terminal screen
import time    # Wait and print grid
import random  # Generate and receive random coords

def clear_screen():
    """Clears the terminal screen by running command depending on the OS:
     * Linux/macOS/*nix: `clear`
     * Windows: `clr`
    """
    os.system('clear' if os.name is 'posix' else 'cls')

class Color:
    """Contains ANSI color escape sequences to modify color of output text
    """
    RED       = '\u001b[31;1m'
    GREEN     = '\u001b[32;1m'
    YELLOW    = '\u001b[33;1m'
    BLUE      = '\u001b[34;1m'
    MAGENTA   = '\u001b[35;1m'
    WHITE     = '\u001b[37;1m'
    RESET     = '\u001b[0m'

class Goal:
    """Holds information regarding goal of the game.
    
    Attributes:
        x_index   : 'X' coordinate of goal in grid starting from top-left
        y_index   : 'Y' coordinate of goal in grid starting from top-left
        type      : Object type used as identifier
    """
    def __init__(self, x_index, y_index):
        self.x    = x_index
        self.y    = y_index
        self.type = 2

class Reward:
    """Holds information regarding the reward objects present in the grid.
    
    Attributes:
        x_index   : 'X' coordinate of reward in grid starting from top-left
        y_index   : 'Y' coordinate of reward in grid starting from top-left
        type      : Object type used as identifier
        value     : Random integer between 1 and 9 (inclusive) that decides the
                    strength/value of the reward and thereby increases player energy
    """
    def __init__(self, x_index, y_index):
        self.x        = x_index
        self.y        = y_index
        self.type     = 3
        self.value    = random.randint(1, 9)

class Obstacle:
    """Holds information regarding the various obstacles scattered around the grid.
    
    Attributes:
        x_index   : 'X' coordinate of obstacle in grid starting from top-left
        y_index   : 'Y' coordinate of obstacle in grid starting from top-left
        type      : Object type used as identifier
        value     : Decrease player energy by value*grid_size - used as a multiplier
    """
    def __init__(self, x_index, y_index):
        self.x        = x_index
        self.y        = y_index
        self.type     = 4
        self.value    = -4

class Visited:
    """Holds information regarding the visited cells - those cells already travered by the player.
    
    Attributes:
        x_index   : 'X' coordinate of visited cell in grid starting from top-left
        y_index   : 'Y' coordinate of visited cell in grid starting from top-left
        type      : Object type used as identifier
    """
    def __init__(self, x_index, y_index):
        self.x    = x_index
        self.y    = y_index
        self.type = 5

class Player:
    """Holds information regarding the player of the game.
    
    The class holds functions that make the moves, that is, changes the player position according 
    to the remaining moves, checks for collisions with other objects on the grid and thereafter
    controls the subsequent actions
    
    Args:
        x_index           : 'X' coordinate of player in grid starting from top-left
        y_index           : 'Y' coordinate of player in grid starting from top-left
        N                 : Size of the grid

    Attributes            : 
        x_index           : 'X' coordinate of player in grid starting from top-left
        y_index           : 'Y' coordinate of player in grid starting from top-left
        type              : Object type used as identifier
        energy            : Energy remaining in the player (integer)
        remaining_moves   : String of sequence of moves that are to be executed
    """
    
    # Dict holding respective move directions for the move types
    # -1, 0, 1 are adders that change the x and y index of the cell
    directions = {
        'R': [ 0,  1],
        'L': [ 0, -1],
        'U': [-1,  0],
        'D': [ 1,  0]
    }

    def move_unit(self, dir_x, dir_y):
        """Moves the player one unit towards specified direction.
        
        The method first evaluates the new coordinates of the player by adding
        the direction coords to the old coords. The new coords' modulus is taken
        with N, the grid size, so as to allow the player to wrap around the grid.
        The players coords (x/y indices) are changed subsequently.
        
        Arguments:
            dir_x   : Move unit 0, -1, 1 units in the x-axis
            dir_y   : Move unit 0, -1, 1 units in the y-axis
        """
        # Make this a global variable to be accessed outside this method
        global game_win

        old_coords = self.x, self.y

        # 1. Take mod(N) to wrap around
        # 2. Assign new coords to the player coords
        # 3. Reduce player energy by 1
        new_coords = (self.x + dir_x) % grid.N, (self.y + dir_y) % grid.N
        self.x, self.y = new_coords
        self.energy -= 1

        # Add the old coordinates of the cell in list of visited cells, an attribute
        # of the Grid class, only if it is not present beforehand
        if old_coords not in grid.cell_to_coords_list(grid.visited_cells):
            # Create Visited object and append to list
            grid.visited_cells.append(Visited(*old_coords))

        # If the new evaluated coordinates are those of game's goal, then make player win
        # and return fast
        if new_coords == grid.goal:
            game_win = True
            return

        def check_collision(cell_list):
            """Checks whether player's new coords are colliding with obstacles or rewards.

            Arguments:
                cell_list: List of cell objects (not coords) that are to be checked
            """
            # Finds _next_ index in cell_list of which the cell has identical coords as the new player coords
            # Otherwise, it returns -1
            cell_index = next((i for i, coords in enumerate(grid.cell_to_coords_list(cell_list)) if coords == new_coords), -1)

            # Collision detected:
            # ===================
            # 1. Get cell which is colliding with the player
            # 2. Increase/decrease player energy according to the cell value
            # 3. Delete the colliding cell from the list, the player has "eaten" it
            # 4. Return fast otherwise IndexError
            if cell_index is not -1:
                current_cell = cell_list[cell_index]
                self.energy += current_cell.value * grid.N
                del cell_list[cell_index]
                return

        # Check for collisions with both obstacles and rewards
        check_collision(grid.myObstacles)
        check_collision(grid.myRewards)

    def makeMove(self, s):
        """Main move handling function, decides player/grid movements/changes.
        
        This is a recursive function that makes player/grid movements/changes and then
        changes/reduces the move string by 1, either reducing the command_length by 1 or
        removing the active command if length is 0. This function is called again
        with the new move string.
        
        Permitted moves:
            R: Right
            L: Left
            D: Down
            U: Up
            C: Clockwise rotate
            A: Anti-clockwise rotate

        Base case:
            There are no more commands/moves left or the player has won.
        
        Arguments:
            s: The _remaining moves_ string, sequence of moves
        
        Returns: Boolean - Game state and whether valid move has been made
        """
        # Permitted move types, or the alphabets that are allowed in the move string
        permitted_move_types    = list(self.directions.keys())  # [R, D, U, L] the possible direction moves
        permitted_rotate_types  = ['A', 'C']                    # [A, C] The possible/allowed rotate moves

        # Build a list of commands, where each element is of the form: "<move_type><move_length>"
        # where <move_type> is the move letter (R, D, A, ...), and <move_length> is a number containing
        # the number of such commands to make
        #
        # Loop over the string and evaluate each character:
        #   * If <move_type> add it as a new element in the list
        #   * If <move_length> add it to the last commands string
        commands = []
        for char in s:
            if char in permitted_move_types + permitted_rotate_types:
                commands.append(char)
            else:
                commands[-1] += char

        # Base cases:
        # ===========
        # 1. If there are no commands/moves left
        # 2. If the player has already won the game in the previous move
        if not commands: return True
        if game_win: return True

        # The current, active, first command to execute from the list
        # and the type, length of it
        active_command  = commands[0]
        active_command_type = active_command[0]
        active_command_length = int(active_command[1:])

        # Initially set valid_move as False
        valid_move = False

        # If the active command is of move type and the player energy is greater than zero
        if active_command_type in permitted_move_types and self.energy > 0:
            # Make the move!
            self.move_unit(*self.directions[active_command_type])
            valid_move = True 

        # If the active command is of rotate type and the energye is greater
        # than that required for a rotation
        elif active_command_type in permitted_rotate_types and self.energy >= grid.N // 3:
            # If the active command was "Clockwise rotation" and was successfully completed
            if active_command_type is 'C' and grid.rotateClockwise(active_command_length):
                valid_move = True

            # If the active command was "Ant-clockwise rotation" and was successfully completed
            elif active_command_type is 'A' and grid.rotateAntiClockwise(active_command_length):
                valid_move = True

        # If the move made was valid, then:
        # 1. Update the game grid with the new positions of the various cells
        # 2. Print the updated grid to the console
        # 3. Wait (sleep) for half a second (0.5s) before making the next move
        # 4. Update command length and active command list
        # 5. Update remaining_commands string
        # 6. Return status of and make the next move using the updated remaining_commands string
        if valid_move:
            grid.update_grid()
            grid.showGrid()
            time.sleep(0.5)

            active_command_length = active_command_length - 1 if active_command_type in permitted_move_types else 0
            commands = ([] if active_command_length is 0 else [active_command_type + str(active_command_length)]) + commands[1:]

            self.remaining_moves = ''.join(commands)
            return self.makeMove(self.remaining_moves)

        # Otherwise, of course, return False indicating invalid move
        return False

    def __init__(self, x_index, y_index, N):
        self.x                  = x_index
        self.y                  = y_index
        self.type               = 1
        self.energy             = 2 * N  # Initial energy points should be twice the grid size
        self.remaining_moves    = ''

class Grid:
    """Main Grid class that holds all information regarding the game.
    
    Attributes:
        N             : Integer - The grid size
        grid          : Two-dimensional list containing object positions
        myObstacles   : List of obstacle objects
        myRewards     : List of reward objects
        visited_cells : List of visited cell objects
        start         : Start cell
        goal          : Goal cell

    Arguments:
        N: The grid size
    """
    def cell_to_coords_list(self, cells):
        """Returns list of coordinates of the cells in the cell list.
        """
        return list(map(lambda cell: (cell.x, cell.y), cells))

    def get_cell_coordinates(self):
        """Returns list of all (i, j) combinations
        """
        coords_list = []
        for i in range(self.N):
            for j in range(self.N):
                coords_list.append((i, j))
        return coords_list

    def get_free_cell_coordinates(self):
        """Returns list of coordinates of all unoccupied, free cells in the grid.
        """
        all_occupied_coords = self.cell_to_coords_list(self.myObstacles + self.myRewards + [player, grid_goal])
        return list(filter(lambda coords: coords not in all_occupied_coords, self.get_cell_coordinates()))

    def get_boundary_cell_coordinates(self):
        """Returns list of coordinates of all boundary cells.
        """
        coords_list = self.get_cell_coordinates()
        # The filter function here checks whether the cell coords contains 0 or N-1
        boundary_coords_list = list(filter(lambda coords: set(coords).intersection(set([0, self.N - 1])), coords_list))
        return boundary_coords_list

    def rotateClockwise(self, rotation_factor):
        """Method that performs the rotation of grid.
        
        Returns: Boolean - whether grid rotation was possible or not
        """
        # Because rotation 'n' times is same as rotation 'n%4' times
        # if the rotations are done at 90 degrees
        real_rotation_factor = rotation_factor % 4

        def new_coords(i, j):
            """Returns new coordinates of the cell depending on rotation factor.
            """
            if real_rotation_factor is 0: return (i, j)
            if real_rotation_factor is 1: return (j, self.N - i -1)
            if real_rotation_factor is 2: return (self.N - i - 1, self.N - j - 1)
            return (self.N - j - 1, i)

        def change_coordinates(cell):
            """Returns cell with new rotated coordinates of False indicating invalid rotation.
            """
            # 1. Get the new, proposed coordinates
            # 2. Check whether the cell is an obstacle and it collides with player/goal position - return False
            proposed_coords = new_coords(cell.x, cell.y)
            if cell.type is 4 and proposed_coords in self.cell_to_coords_list([player, grid_goal]):
                return False

            # 3. If the above condition is false, return the cell itself with updated coords
            cell.x, cell.y = proposed_coords
            return cell

        # Update obstacle and reward cell list with rotated coords
        self.myObstacles[:] = map(change_coordinates, self.myObstacles)
        self.myRewards[:] = map(change_coordinates, self.myRewards)

        # If there is a False in the cell list, that means there was an invalid rotation
        # and thus print the error, return False and exit
        if False in self.myRewards + self.myObstacles:
            print(Color.RED + 'Grid cannot be rotated!' + Color.RESET)
            return False

        # Otherwise, decrease the player energy since this was a valid move and return True
        else:
            player.energy -= self.N // 3
            return True

    def rotateAntiClockwise(self, rotation_factor):
        """Rotate anticlocwise using the rotateClockwise function by passing
        the negative of the rotation factor to it.
        
        Returns: Boolean - whether grid rotation was possible or not
        """
        return self.rotateClockwise(-rotation_factor)

    def update_grid(self):
        """Updates the game grid with updated occupied cell positions after every command.
        """
        # List of all occupied/visited cells
        all_occupied_cells = [player, grid_goal] + self.myObstacles + self.myRewards + self.visited_cells

        # For every coordinate on the board, check whether it is occupied by any one of the above
        # cells by comparing coordinates and x, y indices. If no cell is found, add 0 to that position
        # in the grid indicating an empty cell
        # If a cell is found, add the cell-type to the position in the grid if
        # the cell is not of "reward" type. If it is of reward type,
        # add its value with a 'plus' in front of it
        for coords in self.get_cell_coordinates():
            i, j = coords
            required_cell = next((cell for cell in all_occupied_cells if (cell.x, cell.y) == coords), None)

            if required_cell:
                self.grid[i][j] = required_cell.type if required_cell.type is not 3 else '+' + str(required_cell.value)
            else:
                self.grid[i][j] = 0

    def showGrid(self):
        """Print gameboard graphics to the terminal
        """
        # Cell graphic and color depending on the cell type
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

        # Clear screen before printing new board
        clear_screen()

        # Print player energy
        print(Color.YELLOW + 'ENERGY: ' + str(player.energy) + Color.RESET + '\n')

        # Loop through each coordinate in the grid and print according to
        # the cell_details graphics and color. Exceptions are made at "reward" type cell
        # where the reward value is printed
        for row in self.grid:
            for cell in row:
                is_reward_cell = isinstance(cell, str)
                cell_graphic = cell[1] if is_reward_cell else cell_details[cell]['graphic']
                cell_color = Color.YELLOW if is_reward_cell else cell_details[cell]['color']

                print('\u001b[47' + cell_color + ' ' + cell_graphic + Color.RESET, end='', flush=True)
            print()
        print()

        # Print the remaining_moves string
        if not game_win:
            print(Color.MAGENTA + player.remaining_moves + Color.RESET)

    def __init__(self, N):
        self.N              = N
        self.grid           = [[0] * N for _ in range(N)] # 2 dimensional N*N grid with all elements as 0
        self.myObstacles    = []
        self.myRewards      = []
        self.visited_cells  = []

        # Get all the boundary coordinates in the grid and randomly select
        # two from them that shall be the start and goal coordinates
        boundary_coords = self.get_boundary_cell_coordinates()
        self.start, self.goal = random.sample(boundary_coords, 2)

        # Initiating basic class objects of Player and Goal, and
        # making game_win False.
        # Give these variables global scope so that they can be
        # accessed from outside this function body too
        global player, grid_goal, game_win
        player    = Player(*self.start, self.N)
        grid_goal = Goal(*self.goal)
        game_win  = False

        # The following is done on myObstacles and myRewards
        # Get all the presently free coordinates in the grid and randomly select 'N' coordinate pairs from it
        # Create a list of cell objects with those N coordinates and assign it to the list
        obstacles = random.sample(self.get_free_cell_coordinates(), self.N)
        rewards = random.sample(self.get_free_cell_coordinates(), self.N)

        self.myObstacles[:] = map(lambda coords: Obstacle(*coords), obstacles)
        self.myRewards[:] = map(lambda coords: Reward(*coords), rewards)

        # Update the game grid with these new positions
        self.update_grid()

# 1. Clear the terminal screen
# 2. Print welcome text
# 3. Get user input from grid size
# 4. Once input received, clear the screen again
clear_screen()
print(Color.BLUE + 'Welcome to GridWorld!' + Color.RESET + '\n')
GRID_SIZE = int(input(Color.YELLOW + 'Enter grid size: ' + Color.GREEN))
clear_screen()

# 5. Iniate the Grid object instance with the user-input Grid size
# 6. Print grid graphics
grid = Grid(GRID_SIZE)
grid.showGrid()

# 7. Get user input for move sequence string
# 8. Make the move and store move validity
player.remaining_moves = input('\n' + Color.YELLOW + 'Enter move: ' + Color.GREEN).upper()
final_result = player.makeMove(player.remaining_moves)

# 9. Print the final grid
grid.showGrid()

# 10. Print winning text if player has won and moves have been valid,
#     otherwise, print losing text
if final_result and game_win:
    print(Color.GREEN + 'YOU WON!' + Color.RESET)
else:
    print(Color.RED + 'YOU LOST!' + Color.RESET)
