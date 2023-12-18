"""Advent of code Day 19

Thanks to your efforts, the machine parts factory is one of the first factories up 
and running since the lavafall came back. However, to catch up with the large backlog of parts requests, 
the factory will also need a large supply of lava for a while; 
the Elves have already started creating a large lagoon nearby for this purpose.

However, they aren't sure the lagoon will be big enough; 
they've asked you to take a look at the dig plan (your puzzle input).

--- Part Two ---

The Elves were right to be concerned; the planned lagoon would be much too small.

After a few minutes, someone realizes what happened; someone swapped the color 
and instruction parameters when producing the dig plan. 
They don't have time to fix the bug; one of them asks if you can extract the correct instructions from the hexadecimal codes.
"""

import numpy as np
from shapely import Polygon

EXAMPLE = "./example.txt"
INPUT = "./input.txt"


def get_area(instructions: list) -> np.ndarray:
    max_size = sum([int(v) for _, v, _ in instructions])
    cp = (max_size // 2, max_size // 2)
    points = [cp]
    for move, val, color in instructions:
        val = int(val)
        if move == 'R':
            cp = (cp[0], cp[1] + val)
        elif move == 'L':
            cp = (cp[0], cp[1] - val)
        elif move == 'U':
            cp = (cp[0] - val, cp[1])
        elif move == 'D':
            cp = (cp[0] + val, cp[1])
        points.append(cp)

    shape = Polygon(points)
    return round(shape.buffer(.5, cap_style='square', join_style='mitre').area)


def get_area_part_two(instructions: list) -> np.ndarray:
    max_size = sum([int(v) for _, v, _ in instructions])
    cp = (max_size // 2, max_size // 2)
    points = [cp]
    for _, _, color in instructions:
        distance = int(color[2:-2], base=16)
        direction = color[-2]
        if direction == '0':
            cp = (cp[0], cp[1] + distance)
        elif direction == '2':
            cp = (cp[0], cp[1] - distance)
        elif direction == '3':
            cp = (cp[0] - distance, cp[1])
        elif direction == '1':
            cp = (cp[0] + distance, cp[1])
        points.append(cp)

    shape = Polygon(points)
    return round(shape.buffer(.5, cap_style='square', join_style='mitre').area)


def calc_cubic_meters(filename: str, part2: bool = False) -> int:
    with open(filename, "r", encoding="utf-8") as file:
        instructions = [line.strip().split() for line in file.readlines()]
        if part2:
            return get_area_part_two(instructions)
        else:
            return get_area(instructions)
        

def main() -> None:
    test_one = False
    test_two = False

    if calc_cubic_meters(EXAMPLE) == 62:
        print("PASSED TEST: EXAMPLE 1")
        test_one = True

    if calc_cubic_meters(EXAMPLE, part2=True) == 952408144115:
        print("PASSED TEST: EXAMPLE 2")
        test_two = True

    if test_one:
        print(f"Cubic meters of lava for Part One: {calc_cubic_meters(INPUT)}")

    if test_two:
        print(
            f"Cubic meters of lava for Part Two: {calc_cubic_meters(INPUT, part2=True)}"
        )
    return


if __name__ == "__main__":
    main()
