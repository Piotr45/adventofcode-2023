"""Advent of code Day 13

With your help, the hot springs team locates an appropriate spring which 
launches you neatly and precisely up to the edge of Lava Island.

There's just one problem: you don't see any lava.

You do see a lot of ash and igneous rock; there are even what look like gray mountains scattered around.
After a while, you make your way to a nearby cluster of mountains only to discover that the valley 
between them is completely full of large mirrors. Most of the mirrors seem to be aligned in a consistent way; 
perhaps you should head in that direction?

As you move through the valley of mirrors, you find that several of them 
have fallen from the large metal frames keeping them in place. The mirrors are extremely flat and shiny, 
and many of the fallen mirrors have lodged into the ash at strange angles. Because the terrain is all one color, 
it's hard to tell where it's safe to walk or where you're about to run into a mirror.

You note down the patterns of ash (.) and rocks (#) that you see as you walk (your puzzle input); 
perhaps by carefully analyzing these patterns, you can figure out where the mirrors are!

--- Part Two ---

You resume walking through the valley of mirrors and - SMACK! - run directly into one. 
Hopefully nobody was watching, because that must have been pretty embarrassing.

Upon closer inspection, you discover that every mirror has exactly one smudge: 
exactly one . or # should be the opposite type.

In each pattern, you'll need to locate and fix the smudge that causes a different reflection line to be valid.
(The old reflection line won't necessarily continue being valid after the smudge is fixed.)
"""

EXAMPLE = "./example.txt"
INPUT = "./input.txt"


def transpose(pattern) -> list:
    return [*zip(*pattern)]


def split_left_right(pattern: list, idx: int) -> tuple[list, list]:
    left, right = pattern[:idx][::-1], pattern[idx:]
    length = min(len(left), len(right))
    return left[:length], right[:length]


def find_reflection(pattern: list) -> int:
    for idx in range(1, len(pattern)):
        left, right = split_left_right(pattern, idx)
        if left == right:
            return idx
    return 0


def differ_by_one_char(str1: str, str2: str) -> bool:
    return (
        True
        if sum([0 if s1 == s2 else 1 for s1, s2 in zip(str1, str2)]) == 1
        else False
    )


def find_reflection_part_two(pattern: list) -> int:
    for idx in range(1, len(pattern)):
        left, right = split_left_right(pattern, idx)
        differ_by_one = [differ_by_one_char(l, r) for l, r in zip(left, right)]
        are_equal = [l == r for l, r in zip(left, right)]
        if (
            differ_by_one.count(True) == 1
            and are_equal.count(True) == len(are_equal) - 1
        ):
            return idx
    return 0


def calc_mirrors(pattern: list, part2: bool = False) -> int:
    if part2:
        return find_reflection_part_two(pattern) * 100 + find_reflection_part_two(
            transpose(pattern)
        )
    return find_reflection(pattern) * 100 + find_reflection(transpose(pattern))


def number_of_mirrors(filename: str, part2: bool = False) -> int:
    with open(filename, "r", encoding="utf-8") as file:
        res = 0
        lines = file.readlines()
        pattern = []
        for line in lines:
            if line == "\n":
                mirrors = calc_mirrors(pattern, part2)
                res += mirrors
                pattern = []
                continue
            pattern.append(line.strip())
        if pattern != []:
            mirrors = calc_mirrors(pattern, part2)
            res += mirrors
        return res


def main() -> None:
    test_one = False
    test_two = False

    if number_of_mirrors(EXAMPLE) == 405:
        print("PASSED TEST: EXAMPLE 1")
        test_one = True

    if number_of_mirrors(EXAMPLE, part2=True) == 400:
        print("PASSED TEST: EXAMPLE 2")
        test_two = True

    if test_one:
        print(
            f"Reflection line in each pattern for Part One: {number_of_mirrors(INPUT)}"
        )
    if test_two:
        print(
            f"New reflection line in each pattern for Part Two: {number_of_mirrors(INPUT, part2=True)}"
        )

    return


if __name__ == "__main__":
    main()
