SPACE = 0
TARGET_REWARD = 1

class Maze:
    def __init__(self, maze_matrix):
        self.width, self.height = maze_matrix.shape
        self.content = maze_matrix
        # Store a list of empty positions
        self.empty_spaces = []
        for row in range(len(self.content)):
            for cell in range(len(self.content[row])):
                if self.content[row][cell] == SPACE:
                    self.empty_spaces.append((row, cell))
        # Set the initial position to the top left
        self.state = (0, 0)
        # Set the initial target to the bottom right
        self.target = (self.width - 1, self.height - 1)
        # Ensure the empty spaces does not contain the target
        if self.target in self.empty_spaces:
            self.empty_spaces.remove(self.target)
        # The path can optionally be used to track the state history
        self.path = [self.state]

    def get_valid_next_states(self, state=None):
        # If state is not provided use local
        state = state if state else self.state
        x, y = state
        # Create a list containing all the neighbor states
        # Unless they are out of bounds or a wall
        valid_next_states = []
        # Left
        if x - 1 >= 0 and self.content[x - 1, y] == SPACE:
            valid_next_states.append((x - 1, y))
        # Right
        if x + 1 < self.width and self.content[x + 1, y] == SPACE:
            valid_next_states.append((x + 1, y))
        # Up
        if y - 1 >= 0 and self.content[x, y - 1] == SPACE:
            valid_next_states.append((x, y - 1))
        # Down
        if y + 1 < self.height and self.content[x, y + 1] == SPACE:
            valid_next_states.append((x, y + 1))

        return valid_next_states

    def set_state(self, state):
        self.state = state
        self.path.append(state)
        return self.state

    def reset(self, initial_state=(0, 0), target=None):
        self.state = initial_state
        self.path = [self.state]
        # If a new target is provided remove it from the empty spaces
        # And re-add the old target to the empty spaces
        if target:
            self.empty_spaces.append(self.target)
            self.target = target
            self.empty_spaces.remove(self.target)

    def get_reward_matrix(self):
        rewards = self.content.copy()
        rewards[self.target] = TARGET_REWARD
        return rewards

    def __repr__(self):
        grid = ""
        line = ""
        for column in range(len(self.content)):
            for row in range(len(self.content[column])):
                if (row, column) in self.path:
                    line += "O "
                elif self.content[row][column] == SPACE:
                    line += "_ "
                else:
                    line += "[]"
            grid += line + "\n"
            line = ""
        return grid


if __name__ == "__main__":
    import prims_maze
    maze_matrix = prims_maze.generate_prims_maze_matrix(5, 5)
    maze = Maze(maze_matrix)
    print(maze.get_reward_matrix())
    print(maze.empty_spaces)
    print(maze)
