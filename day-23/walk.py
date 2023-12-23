"""Advent of code Day 23

The Elves resume water filtering operations! Clean water starts flowing over the edge of Island Island.

They offer to help you go over the edge of Island Island, too! 
Just hold on tight to one end of this impossibly long rope and they'll lower you down a safe distance 
from the massive waterfall you just created.

As you finally reach Snow Island, you see that the water isn't really reaching the ground: 
it's being absorbed by the air itself. It looks like you'll finally have a little downtime while 
the moisture builds up to snow-producing levels. Snow Island is pretty scenic, even without any snow; 
why not take a walk?

--- Part Two ---

As you reach the trailhead, you realize that the ground isn't as slippery as you expected; 
you'll have no problem climbing up the steep slopes.

Now, treat all slopes as if they were normal paths (.). 
You still want to make sure you have the most scenic hike possible, 
so continue to ensure that you never step onto the same tile twice. What is the longest hike you can take?
"""

from collections import deque


EXAMPLE = "./example.txt"
INPUT = "./input.txt"


DIRECTIONS = ((0, 1), (1, 0), (0, -1), (-1, 0))
DIRECTION_MAP = {"v": (1, 0), "^": (-1, 0), ">": (0, 1), "<": (0, -1)}


def get_neighbors(hiking_map: dict, position: tuple, part2: bool = False):
    if not part2:
        if hiking_map[position] in DIRECTION_MAP.keys():
            yield position[0] + DIRECTION_MAP[hiking_map[position]][0], position[
                1
            ] + DIRECTION_MAP[hiking_map[position]][1]
            return

    for direction in ((0, -1), (1, 0), (-1, 0), (0, 1)):
        new_position = position[0] + direction[0], position[1] + direction[1]
        if new_position not in hiking_map or hiking_map[new_position] == "#":
            continue

        yield new_position


def find_the_longest_path(hiking_map: dict, start: tuple, end: tuple):
    to_check = deque([(*start, set())])
    length = dict()
    length[start] = 0

    while to_check:
        row_index, column_index, path = to_check.pop()

        if (row_index, column_index) == end:
            continue

        for new_point in get_neighbors(hiking_map, (row_index, column_index)):
            new_length = length[row_index, column_index] + 1

            if new_point in path:
                continue
            if new_point not in length or new_length > length[new_point]:
                length[new_point] = new_length

                new_path = path.copy()
                new_path.add(new_point)

                to_check.appendleft((*new_point, new_path))

    return length[end]


def find_the_longest_path_part_two(graph, start: tuple, end: tuple):
    to_visit = deque([(start, 0, set())])
    length = dict()
    length[start] = 0
    path_sizes = []

    while to_visit:
        point, size, path = to_visit.pop()
        if point == end:
            path_sizes.append(size)
            continue

        s = path.copy()
        s.add(point)

        for new_point in graph[point].keys():
            if new_point in path:
                continue

            to_visit.appendleft((new_point, size + graph[point][new_point], s))

    return max(path_sizes)


def bfs(hiking_map: dict, start: tuple, end: tuple, crossings: list):
    to_visit = deque([start])
    length = dict()
    length[start] = 0

    while to_visit:
        column_index, row_index = to_visit.pop()

        if (column_index, row_index) == end:
            return length[end]
        if (column_index, row_index) != start and (
            column_index,
            row_index,
        ) in crossings:
            continue

        for new_position in get_neighbors(hiking_map, (column_index, row_index), True):
            new_length = length[column_index, row_index] + 1

            if new_position not in length or new_length < length[new_position]:
                length[new_position] = new_length
                to_visit.appendleft(new_position)


def create_graph(hiking_map: dict, start: tuple, end: tuple) -> dict:
    crossings = [start, end]
    graph = {start: {}, end: {}}

    for p in hiking_map:
        s = list(get_neighbors(hiking_map, p))
        if len(s) > 2:
            crossings.append(p)
            graph[p] = {}

    for k in graph:
        for c in crossings:
            if c == k:
                continue
            if c in graph[k]:
                continue
            size = bfs(hiking_map, k, c, crossings)
            if size != None:
                graph[k][c] = size
                graph[c][k] = size
    return graph


def calc_hikes(filename: str, part2: bool = False) -> int:
    with open(filename, "r", encoding="utf-8") as file:
        hiking_map = [line.strip() for line in file.readlines()]
        start = (0, 1)
        end = (len(hiking_map) - 1, len(hiking_map[0]) - 2)

        hiking_map = {
            (x, y): v
            for x, r in enumerate(hiking_map)
            for y, v in enumerate(r)
            if v != "#"
        }

        if part2:
            graph = create_graph(hiking_map, start, end)
            return find_the_longest_path_part_two(graph, start, end)
        else:
            return find_the_longest_path(hiking_map, start, end)


def main() -> None:
    test_one = False
    test_two = False

    if calc_hikes(EXAMPLE) == 94:
        print("PASSED TEST: EXAMPLE 1")
        test_one = True

    if calc_hikes(EXAMPLE, part2=True) == 154:
        print("PASSED TEST: EXAMPLE 2")
        test_two = True

    if test_one:
        print(f"How many steps long is the longest hike?: {calc_hikes(INPUT)}")

    if test_two:
        print(
            f"How many steps long is the longest hike?: {calc_hikes(INPUT, part2=True)}"
        )
    return


if __name__ == "__main__":
    main()
