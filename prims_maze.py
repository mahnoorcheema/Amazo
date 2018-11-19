import numpy as np
from random import randint as rand


def generate_prims_maze_matrix(width, height, complexity=0.75, density=0.75, wall=-1, space=0):
    # Create only odd sized mazes
    height = height + 3 if height % 2 == 0 else height + 2
    width = width + 3 if width % 2 == 0 else width + 2

    # Adjust complexity and density in accordance to maze size
    complexity = int(complexity * (5 * (height + width)))
    density = int(density * (height // 2) * (width // 2))

    maze_matrix = np.zeros((height, width), dtype=float)

    # Set the borders to be walls
    maze_matrix[0, :] = maze_matrix[-1, :] = wall
    maze_matrix[:, 0] = maze_matrix[:, -1] = wall

    for i in range(density):
        x, y = rand(0, width // 2) * 2, rand(0, height // 2) * 2
        maze_matrix[y, x] = wall
        for j in range(complexity):
            neighbours = []
            if x > 1:
                neighbours.append((y, x - 2))
            if x < width - 2:
                neighbours.append((y, x + 2))
            if y > 1:
                neighbours.append((y - 2, x))
            if y < height - 2:
                neighbours.append((y + 2, x))
            if len(neighbours):
                y_, x_ = neighbours[rand(0, len(neighbours) - 1)]
                if maze_matrix[y_, x_] == space:
                    maze_matrix[y_, x_] = wall
                    maze_matrix[y_ + (y - y_) // 2, x_ + (x - x_) // 2] = wall
                    x, y = x_, y_
    # Return the maze with the borders stripped off
    return maze_matrix[1:-1, 1:-1]


def print_maze_matrix(matrix):
    for row in matrix:
        for tile in row:
            print("_ " if tile == 0 else "[]", end="")
        print()


if __name__ == "__main__":
    for i in range(5):
        print_maze_matrix(generate_prims_maze_matrix(11, 11))
        print()
