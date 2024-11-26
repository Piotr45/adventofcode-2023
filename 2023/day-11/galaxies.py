"""Advent of code Day 11

You continue following signs for "Hot Springs" and eventually come across an observatory. 
The Elf within turns out to be a researcher studying cosmic expansion using the giant telescope here.

He doesn't know anything about the missing machine parts; he's only visiting for this research project. 
However, he confirms that the hot springs are the next-closest area likely to have people; 
he'll even take you straight there once he's done with today's observation analysis.

Maybe you can help him with the analysis to speed things up?

The researcher has collected a bunch of data and compiled the data into a single giant image (your puzzle input). 
The image includes empty space (.) and galaxies (#).

The researcher is trying to figure out the sum of the lengths of the shortest path between every pair of galaxies. 
However, there's a catch: the universe expanded in the time it took the light 
from those galaxies to reach the observatory.

Due to something involving gravitational effects, only some space expands. 
In fact, the result is that any rows or columns that contain no galaxies should all actually be twice as big.

--- Part Two ---

The galaxies are much older (and thus much farther apart) than the researcher initially estimated.

Now, instead of the expansion you did before, make each empty row or column one million times larger. 
That is, each empty row should be replaced with 1000000 empty rows, 
and each empty column should be replaced with 1000000 empty columns.
"""

EXAMPLE = "./example.txt"
INPUT = "./input.txt"


class Galaxy:
    def __init__(self, name: int, position: tuple[int, int]) -> None:
        self.name: int = name
        self.position: tuple = position
        self.distances_to_other_galaxies: dict = {}


def find_galaxies(space: list) -> list[Galaxy]:
    galaxies = []
    galaxy_name = 1
    for ridx, row in enumerate(space):
        for cidx, col in enumerate(row):
            if col == "#":
                galaxies.append(Galaxy(galaxy_name, (ridx, cidx)))
                galaxy_name += 1
    return galaxies


def expand_space(space: list, galaxies: list) -> list[Galaxy]:
    empty_rows = [
        x
        for x in range(len(space))
        if x not in [galaxy.position[0] for galaxy in galaxies]
    ]
    empty_cols = [
        y
        for y in range(len(space[0]))
        if y not in [galaxy.position[1] for galaxy in galaxies]
    ]
    inserted = 0
    for empty_row_idx in empty_rows:
        space.insert(empty_row_idx + inserted, "." * len(space[0]))
        inserted += 1
    inserted = 0
    for empty_col_idx in empty_cols:
        for i in range(len(space)):
            temp = [s for s in space[i]]
            temp.insert(empty_col_idx + inserted, ".")
            space[i] = "".join(temp)
        inserted += 1


def expand_space_part_two(space: list, galaxies: list) -> list[Galaxy]:
    empty_rows = [
        x
        for x in range(len(space))
        if x not in [galaxy.position[0] for galaxy in galaxies]
    ]
    empty_cols = [
        y
        for y in range(len(space[0]))
        if y not in [galaxy.position[1] for galaxy in galaxies]
    ]
    return empty_rows, empty_cols


def find_shortest_paths_between_each_galaxy(galaxies: list) -> dict:
    res = 0
    for i in range(len(galaxies)):
        src_galaxy = galaxies[i]
        for j in range(i + 1, len(galaxies)):
            dst_galaxy = galaxies[j]
            steps = abs(src_galaxy.position[0] - dst_galaxy.position[0]) + abs(
                src_galaxy.position[1] - dst_galaxy.position[1]
            )
            res += steps
    return res


def find_shortest_paths_between_each_galaxy_part_two(
    galaxies: list, empty_rows: list, empty_cols: list
) -> dict:
    res = 0
    for i in range(len(galaxies)):
        src_galaxy = galaxies[i]
        for j in range(i + 1, len(galaxies)):
            dst_galaxy = galaxies[j]
            lbr, rbr = min(src_galaxy.position[0], dst_galaxy.position[0]), max(
                src_galaxy.position[0], dst_galaxy.position[0]
            )
            lbc, rbc = min(src_galaxy.position[1], dst_galaxy.position[1]), max(
                src_galaxy.position[1], dst_galaxy.position[1]
            )
            bonus_steps = sum([10**6 - 1 for r in empty_rows if lbr < r < rbr]) + sum(
                [10**6 - 1 for c in empty_cols if lbc < c < rbc]
            )
            steps = (
                abs(src_galaxy.position[0] - dst_galaxy.position[0])
                + abs(src_galaxy.position[1] - dst_galaxy.position[1])
                + bonus_steps
            )
            res += steps
    return res


def galaxies_shortest_path(filename: str, debug: bool = False) -> int:
    with open(filename, "r", encoding="utf-8") as file:
        space = [line.strip() for line in file.readlines()]
        galaxies = find_galaxies(space)
        expand_space(space, galaxies)
        galaxies = find_galaxies(space)
        distances_to_other_galaxies = find_shortest_paths_between_each_galaxy(galaxies)
        return distances_to_other_galaxies


def galaxies_shortest_path_part_two(filename: str, debug: bool = False) -> int:
    with open(filename, "r", encoding="utf-8") as file:
        space = [line.strip() for line in file.readlines()]
        galaxies = find_galaxies(space)
        empty_rows, empty_cols = expand_space_part_two(space, galaxies)
        distances_to_other_galaxies = find_shortest_paths_between_each_galaxy_part_two(
            galaxies, empty_rows, empty_cols
        )
        print(distances_to_other_galaxies)
        return distances_to_other_galaxies


def main() -> None:
    test_one = False
    test_two = False

    if galaxies_shortest_path(EXAMPLE, True) == 374:
        print("PASSED TEST: EXAMPLE 1")
        test_one = True

    if galaxies_shortest_path_part_two(EXAMPLE) == 82000210:
        print("PASSED TEST: EXAMPLE 2")
        test_two = True

    if test_one:
        print(
            f"Sum of the lengths in shortest path for Part One: {galaxies_shortest_path(INPUT)}"
        )
    if test_two:
        print(
            f"Sum of the lengths in shortest path for Part Two: {galaxies_shortest_path_part_two(INPUT)}"
        )

    return


if __name__ == "__main__":
    main()
