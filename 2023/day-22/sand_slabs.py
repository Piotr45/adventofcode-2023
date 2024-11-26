"""Advent of code Day 22

Enough sand has fallen; it can finally filter water for Snow Island.

Well, almost.

The sand has been falling as large compacted bricks of sand, 
piling up to form an impressive stack here near the edge of Island Island. 
In order to make use of the sand to filter water, 
some of the bricks will need to be broken apart - nay, disintegrated - back into freely flowing sand.

The stack is tall enough that you'll have to be careful about choosing which bricks to disintegrate; 
if you disintegrate the wrong brick, large portions of the stack could topple, which sounds pretty dangerous.

The Elves responsible for water filtering operations took a snapshot of the bricks 
while they were still falling (your puzzle input) which should let you work out which bricks are safe to disintegrate.

--- Part Two ---

Disintegrating bricks one at a time isn't going to be fast enough. 
While it might sound dangerous, what you really need is a chain reaction.

You'll need to figure out the best brick to disintegrate. 
For each brick, determine how many other bricks would fall if that brick were disintegrated.
"""

import re

from collections import defaultdict


EXAMPLE = "./example.txt"
INPUT = "./input.txt"


def calc_dropped_brick(tallest: defaultdict, brick: list):
    top = max(
        tallest[(x, y)]
        for x in range(brick[0], brick[3] + 1)
        for y in range(brick[1], brick[4] + 1)
    )
    dz = max(brick[2] - top - 1, 0)
    return (brick[0], brick[1], brick[2] - dz, brick[3], brick[4], brick[5] - dz)


def drop_bricks(tower: list):
    tallest = defaultdict(int)
    new_tower = []
    num_falls = 0
    for brick in tower:
        new_brick = calc_dropped_brick(tallest, brick)
        if new_brick[2] != brick[2]:
            num_falls += 1
        new_tower.append(new_brick)
        for x in range(brick[0], brick[3] + 1):
            for y in range(brick[1], brick[4] + 1):
                tallest[(x, y)] = new_brick[5]
    return num_falls, new_tower


def how_may_bricks(filename: str, part2: bool = False) -> int:
    with open(filename, "r", encoding="utf-8") as file:
        bricks = sorted(
            [
                list(map(int, re.findall("\d+", line.strip())))
                for line in file.readlines()
            ],
            key=lambda b: b[2],
        )

        _, fallen_bricks = drop_bricks(bricks)
        part_one_result, part_two_result = 0, 0

        for i in range(len(fallen_bricks)):
            removed = fallen_bricks[:i] + fallen_bricks[i + 1 :]
            falls, _ = drop_bricks(removed)
            if not falls:
                part_one_result += 1
            else:
                part_two_result += falls

        if part2:
            return part_two_result
        else:
            return part_one_result


def main() -> None:
    test_one = False
    test_two = True

    if how_may_bricks(EXAMPLE) == 5:
        print("PASSED TEST: EXAMPLE 1")
        test_one = True

    if test_one:
        print(
            f"How many bricks could be safely chosen as the one to get disintegrated?: {how_may_bricks(INPUT)}"
        )

    if test_two:
        print(
            f"What is the sum of the number of other bricks that would fall?: {how_may_bricks(INPUT, part2=True)}"
        )
    return


if __name__ == "__main__":
    main()
