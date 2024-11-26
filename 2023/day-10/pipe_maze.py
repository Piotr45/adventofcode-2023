"""Advent of code Day 10

You use the hang glider to ride the hot air from Desert Island all the way up to the floating metal island.
 This island is surprisingly cold and there definitely aren't any thermals to glide on, 
 so you leave your hang glider behind.

You wander around for a while, but you don't find any people or animals. 
However, you do occasionally find signposts labeled "Hot Springs" pointing in a seemingly consistent direction;
 maybe you can find someone at the hot springs and ask them where the desert-machine parts are made.

The landscape here is alien; even the flowers and trees are made of metal. 
As you stop to admire some metal grass, you notice something metallic scurry away in your peripheral vision 
and jump into a big pipe! It didn't look like any animal you've ever seen; if you want a better look, 
you'll need to get ahead of it.

Scanning the area, you discover that the entire field you're standing on is densely packed with pipes; 
it was hard to tell at first because they're the same metallic silver color as the "ground". 
You make a quick sketch of all of the surface pipes you can see (your puzzle input).

--- Part Two ---

You quickly reach the farthest point of the loop, but the animal never emerges. 
Maybe its nest is within the area enclosed by the loop?

"""

import re
from matplotlib.path import Path
from scipy.spatial import ConvexHull

EXAMPLE_1 = "./example_1.txt"
EXAMPLE_2 = "./example_2.txt"
EXAMPLE_3 = "./example_3.txt"
EXAMPLE_4 = "./example_4.txt"
EXAMPLE_5 = "./example_5.txt"
INPUT = "./input.txt"


CONNECTIONS = {
    "|": ((-1, 0), (1, 0)),  # North and South
    "-": ((0, -1), (0, 1)),  # West and East
    "L": ((-1, 0), (0, 1)),  # North and East
    "J": ((-1, 0), (0, -1)),  # North and West
    "7": ((1, 0), (0, -1)),  # South and West
    "F": ((1, 0), (0, 1)),  # South and East
    ".": [],
    "S": ((0, 1), (0, -1), (1, 0), (-1, 0)),  # All directions (max 2 connections)
}


def create_maze_schematic(lines: list) -> tuple[dict, tuple]:
    coords = [(r, c) for c in range(len(lines[0])) for r in range(len(lines))]
    connection_map = {coord: [] for coord in coords}
    start_point = None
    for ridx, row in enumerate(lines):
        for cidx, col in enumerate(row):
            if col == "S":
                start_point = (ridx, cidx)
            elif col == ".":
                continue
            for (x, y) in CONNECTIONS[col]:
                try:
                    for (x2, y2) in CONNECTIONS[lines[ridx + x][cidx + y]]:
                        if -x2 == x and -y2 == y:
                            connection_map[(ridx, cidx)].append((ridx + x, cidx + y))

                except IndexError:
                    continue
    return connection_map, start_point


def fill_distance_map(
    connection_map: dict, starting_point: tuple, distance_map: list
) -> None:
    curr_nodes = connection_map[starting_point]
    distance_map[starting_point[0]][starting_point[1]] = 0
    counter = 1
    prev_nodes = [starting_point, starting_point]
    while True:
        if curr_nodes[0] == curr_nodes[1]:
            distance_map[curr_nodes[0][0]][curr_nodes[0][1]] = counter
            break
        for node_id, curr_node in enumerate(curr_nodes):
            for next_node in connection_map[curr_node]:
                if next_node != prev_nodes[node_id] and next_node != starting_point:
                    prev_nodes[node_id] = curr_node
                    distance_map[curr_node[0]][curr_node[1]] = counter
                    curr_nodes[node_id] = next_node
                    break
        counter += 1


def pipe_maze(filename: str, debug: bool = False) -> int:
    with open(filename, "r", encoding="utf-8") as file:
        lines = [line.strip() for line in file.readlines()]
        distance_map = [[-1 for _ in row] for row in lines]
        connection_map, start_point = create_maze_schematic(lines)
        fill_distance_map(connection_map, start_point, distance_map)
        if debug:
            for dst in distance_map:
                print("".join(["." if d == -1 else str(d) for d in dst]))
    return max([max(dst) for dst in distance_map])


def create_path(connection_map: dict, starting_point: tuple) -> list:
    path = [starting_point]
    prev_node = starting_point
    current_node = connection_map[starting_point][1]
    while True:
        path.append(current_node)
        if prev_node == connection_map[current_node][0]:
            prev_node = current_node
            current_node = connection_map[current_node][1]
        else:
            prev_node = current_node
            current_node = connection_map[current_node][0]
        if current_node == starting_point:
            break
    return path


def pipe_maze_part_two(filename: str, debug: bool = False) -> int:
    with open(filename, "r", encoding="utf-8") as file:
        lines = [line.strip() for line in file.readlines()]
        grid = (len(lines), len(lines[0]))
        distance_map = [[-1 for _ in row] for row in lines]
        connection_map, start_point = create_maze_schematic(lines)
        path = create_path(connection_map, start_point)
        result = 0
        p = Path(path)
        for x in range(grid[0]):
            for y in range(grid[1]):
                if (x, y) in path:
                    continue
                if p.contains_point((x, y)):
                    distance_map[x][y] = "I"
                    result += 1
        if debug:
            for dst in distance_map:
                print(" ".join(["." if d == -1 else str(d) for d in dst]))
    return result


def main() -> None:
    test_one = False
    test_two = False

    if pipe_maze(EXAMPLE_1) == 4 and pipe_maze(EXAMPLE_2) == 8:
        print("PASSED TEST: EXAMPLE 1")
        test_one = True

    if (
        pipe_maze_part_two(EXAMPLE_3) == 4
        and pipe_maze_part_two(EXAMPLE_4) == 8
        and pipe_maze_part_two(EXAMPLE_5) == 10
    ):
        print("PASSED TEST: EXAMPLE 2")
        test_two = True

    if test_one:
        print(f"The distance for farthest point for Part One is: {pipe_maze(INPUT)}")
    if test_two:
        print(
            f"The number of enclosed tiles for Part Two is: {pipe_maze_part_two(INPUT)}"
        )

    return


if __name__ == "__main__":
    main()
