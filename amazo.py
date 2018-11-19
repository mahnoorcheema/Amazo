from environment import Maze
from prims_maze import generate_prims_maze_matrix
import random
import numpy as np


def build_model(width, height=None):
    # If no height supplied, make a square
    height = height if height else width
    # Create a four dimensional array where each state points
    # to a 2d array of qualities for each next state
    return np.zeros((width, height, width, height))


def train_single_epoch(state, Q, maze, gamma):
    reward_matrix = maze.get_reward_matrix()
    while state != maze.target:
        # Make a random move
        valid_next_states = maze.get_valid_next_states(state)
        next_state = random.choice(valid_next_states)

        # Determine the score of the best next move
        valid_next_next_states = maze.get_valid_next_states(next_state)
        max_q_for_next_next_states = max([Q[next_state][nns] for nns in valid_next_next_states])

        # Update quality matrix to the actual reward + the possible future reward (with discount factor)
        Q[state][next_state] = reward_matrix[next_state] + (gamma * max_q_for_next_next_states)

        # Apply move
        state = next_state


def train_for_random_start(Q, maze, gamma=0.5, minimum_change_per_epoch=0.001, minimum_epochs=42):
    epoch = 0
    amount_changed = 0
    # Todo: Replace minimum epochs with amount changed falloff
    while epoch < minimum_epochs or amount_changed > minimum_change_per_epoch:
        previous_q = Q.copy()
        # Pick a random starting location
        state = random.choice(maze.empty_spaces)
        # Train until target reached
        train_single_epoch(state, Q, maze, gamma)
        # Determine if Q is still undergoing changes
        amount_changed = np.sum(np.abs(Q - previous_q))
        print("Epoch: %d. Q modified by %f" % (epoch, amount_changed))
        epoch += 1


def train_for_all_start(Q, maze, gamma=0.5):
    # Trains Q for every possible starting position
    starting_positions = maze.empty_spaces
    for starting_position in starting_positions:
        train_single_epoch(starting_position, Q, maze, gamma)


def get_best_next_state(Q, state, valid_next_states):
    # Determine the highest Q for all valid next states
    best_next_state = None
    # Initialize the best to the worst so that all values are better
    best = -float("inf")
    for next_state in valid_next_states:
        if Q[state][next_state] > best:
            best = Q[state][next_state]
            best_next_state = next_state
    if best_next_state is None:
        raise ValueError("All options are infinitely terrible")
    return best_next_state


def solve_for_position(Q, maze, state=(0, 0)):
    maze.reset(state)
    while state != maze.target:
        valid_next_states = maze.get_valid_next_states()
        best_next_state = get_best_next_state(Q, state, valid_next_states)
        state = maze.set_state(best_next_state)
    return maze.path


def solve_all(Q, maze):
    for start in maze.empty_spaces:
        solve_for_position(Q, maze, start)


def get_direction(state, next_state):
    # Determine the transition required to go from state to next state
    x = next_state[0] - state[0]
    y = next_state[1] - state[1]

    if x == -1:
        return "left"
    elif x == 1:
        return "right"
    elif y == -1:
        return "up"
    elif y == 1:
        return "down"
    else:
        return "remain"


def get_navigation_map(Q, maze, wall=-1):
    # Show solution for every possible position in maze
    ICONS = {"up": u"▲", "right": u"►", "down": u"▼", "left": u"◄", "remain": "x", "wall": u"▢"}
    navigation_map = ""
    line = ""
    for column in range(len(maze.content)):
        for row in range(len(maze.content[column])):
            if maze.content[row, column] == wall:
                line += ICONS["wall"] + " "
            else:
                # Determine the direction of the arrow
                state = (row, column)
                valid_next_states = maze.get_valid_next_states(state)
                best_next_state = get_best_next_state(Q, state, valid_next_states)
                direction = get_direction(state, best_next_state)
                line += ICONS[direction] + " "

        navigation_map += line + "\n"
        line = ""
    return navigation_map


if __name__ == "__main__":
    input_size = int(input("Size? "))
    size = input_size if input_size else 11

    maze = Maze(generate_prims_maze_matrix(size, size))
    print(maze)
    model = build_model(maze.width, maze.height)
    train_for_random_start(model, maze)
    # test_all(model, maze)
    print(get_navigation_map(model, maze))

