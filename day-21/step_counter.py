"""Advent of code Day 21

You manage to catch the airship right as it's dropping someone else off on their all-expenses-paid trip to Desert Island!
It even helpfully drops you off near the gardener and his massive farm.

"You got the sand flowing again! Great work! 
Now we just need to wait until we have enough sand to filter the water for Snow Island and we'll have snow again in no time."

While you wait, one of the Elves that works with the gardener heard how good you are at solving problems and would like your help. 
He needs to get his steps in for the day, and so he'd like to know which garden plots he can reach with exactly his remaining 64 steps.

--- Part Two ---

The Elf seems confused by your answer until he realizes his mistake: 
he was reading from a list of his favorite numbers that are both perfect squares and perfect cubes, not his step counter.

The actual number of steps he needs to get today is exactly 26501365.

He also points out that the garden plots and rocks are set up so that the map repeats infinitely in every direction.
"""

from collections import deque
from math import ceil
import numpy as np

EXAMPLE = "./example.txt"
INPUT = "./input.txt"

DIRECTIONS = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # Up Right Down Left


def grid_search(grid: list, start_point: tuple, total_steps: int = 64) -> int:
    queue = deque()
    queue.append(start_point)

    for step in range(1, total_steps + 1):
        processing_queue = deque()
        visited = set()

        while len(queue):
            x, y = queue.popleft()
            for direction in DIRECTIONS:
                new_x, new_y = (x + direction[0], y + direction[1])
                if (
                    new_x < 0
                    or new_x >= len(grid)
                    or new_y < 0
                    or new_y >= len(grid[0])
                ):
                    continue
                if grid[new_x][new_y] != "#":
                    if (new_x, new_y) not in visited:
                        visited.add((new_x, new_y))
                        processing_queue.append((new_x, new_y))
        queue = processing_queue
        if step == total_steps:
            return len(visited)


def grid_search_part_two(grid: list, start_point: tuple, total_steps: int = 64) -> int:
    queue = deque()
    queue.append(start_point)

    for step in range(1, total_steps + 1):
        processing_queue = deque()
        visited = set()

        while len(queue):
            x, y = queue.popleft()
            for direction in DIRECTIONS:
                new_x, new_y = (x + direction[0], y + direction[1])
                new_x_ref, new_y_ref = (new_x % len(grid), new_y % len(grid[0]))
                if grid[new_x_ref][new_y_ref] != "#":
                    if (new_x, new_y) not in visited:
                        visited.add((new_x, new_y))
                        processing_queue.append((new_x, new_y))
        queue = processing_queue
        if step == total_steps:
            return len(visited)


def how_many_garden_plots(
    filename: str, total_steps: int = 64, part2: bool = False
) -> int:
    with open(filename, "r", encoding="utf-8") as file:
        grid = [line.strip() for line in file.readlines()]
        start_point = [
            (x, y)
            for y in range(len(grid[0]))
            for x in range(len(grid))
            if grid[x][y] == "S"
        ][0]

        if part2:
            num_steps = total_steps % len(grid)
            bfs1 = grid_search_part_two(grid, start_point, num_steps)
            bfs2 = grid_search_part_two(grid, start_point, num_steps + len(grid))
            bfs3 = grid_search_part_two(grid, start_point, num_steps + len(grid) * 2)
            poly = np.polyfit([i for i in range(3)], [bfs1, bfs2, bfs3], 2)
            target = (total_steps - (total_steps % len(grid))) // len(grid)
            return ceil(poly[0] * target**2 + poly[1] * target + poly[2])
        else:
            return grid_search(grid, start_point, total_steps)


def main() -> None:
    test_one = False
    test_two = True

    if how_many_garden_plots(EXAMPLE, 6) == 16:
        print("PASSED TEST: EXAMPLE 1")
        test_one = True

    if test_one:
        print(
            f"How many garden plots could the Elf reach in exactly 64 steps?: {how_many_garden_plots(INPUT)}"
        )

    if test_two:
        print(
            f"How many garden plots could the Elf reach in exactly 26501365 steps?: {how_many_garden_plots(INPUT, 26501365, part2=True)}"
        )
    return


if __name__ == "__main__":
    main()
