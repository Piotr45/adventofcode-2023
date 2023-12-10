"""Advent of code Day 10

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


def find_area_enclosed_by_pies(distance_map: list) -> int:
    # dummy way to fill all -1 outside
    filling = True
    while filling:
        filling = False
        for ridx in range(len(distance_map)):
            for cidx in range(len(distance_map[0])):
                if distance_map[ridx][cidx] == -1:
                    if (ridx + 1) >= len(distance_map) or (ridx - 1) < 0:
                        distance_map[ridx][cidx] = "O"
                        filling = True
                    if (cidx + 1) >= len(distance_map[0]) or (cidx - 1) < 0:
                        distance_map[ridx][cidx] = "O"
                        filling = True
                    try:
                        if (
                            distance_map[ridx - 1][cidx] == "O"
                            or distance_map[ridx + 1][cidx] == "O"
                            or distance_map[ridx][cidx - 1] == "O"
                            or distance_map[ridx][cidx + 1] == "O"
                            or distance_map[ridx + 1][cidx + 1] == "O"
                            or distance_map[ridx - 1][cidx + 1] == "O"
                            or distance_map[ridx + 1][cidx - 1] == "O"
                            or distance_map[ridx - 1][cidx - 1] == "O"
                            or distance_map[ridx + 1][cidx] == "O"
                            or distance_map[ridx - 1][cidx] == "O"
                        ):
                            distance_map[ridx][cidx] = "O"
                            filling = True
                    except IndexError:
                        pass
    return


def pipe_maze_part_two(filename: str, debug: bool = False) -> int:
    with open(filename, "r", encoding="utf-8") as file:
        lines = [line.strip() for line in file.readlines()]
        if debug:
            for line in lines:
                print(line.strip())
        distance_map = [[-1 for _ in row] for row in lines]
        connection_map, start_point = create_maze_schematic(lines)
        fill_distance_map(connection_map, start_point, distance_map)
        find_area_enclosed_by_pies(distance_map)
        result = sum([dst.count(-1) for dst in distance_map])

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
        and pipe_maze_part_two(EXAMPLE_4, True) == 8
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
