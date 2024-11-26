"""Advent of code Day 12

You finally reach the hot springs! You can see steam rising from secluded areas attached to the primary,
 ornate building.

As you turn to enter, the researcher stops you. 
"Wait - I thought you were looking for the hot springs, weren't you?" 
You indicate that this definitely looks like hot springs to you.

"Oh, sorry, common mistake! This is actually the onsen! The hot springs are next door."

You look in the direction the researcher is pointing and suddenly notice the massive 
metal helixes towering overhead. "This way!"

It only takes you a few more steps to reach the main gate of the massive 
fenced-off area containing the springs. You go through the gate and into a small administrative building.

"Hello! What brings you to the hot springs today? Sorry they're not very hot right now; 
we're having a lava shortage at the moment." You ask about the missing machine parts for Desert Island.

"Oh, all of Gear Island is currently offline! Nothing is being manufactured at the moment, 
not until we get more lava to heat our forges. And our springs.
 The springs aren't very springy unless they're hot!"

"Say, could you go up and see why the lava stopped flowing? 
The springs are too cold for normal operation, 
but we should be able to find one springy enough to launch you up there!"

There's just one problem - many of the springs have fallen into disrepair, 
so they're not actually sure which springs would even be safe to use! Worse yet, 
their condition records of which springs are damaged (your puzzle input) are also damaged! 
You'll need to help them repair the damaged records.

--- Part Two ---

As you look out at the field of springs, you feel like there are way more springs than the condition records list. 
When you examine the records, you discover that they were actually folded up this whole time!

To unfold the records, on each row, replace the list of spring conditions with five copies of itself (separated by ?) 
and replace the list of contiguous groups of damaged springs with five copies of itself (separated by ,).
"""

import re

from functools import cache

EXAMPLE = "./example.txt"
INPUT = "./input.txt"


@cache
def calculate_arrangements(springs: str, broken_states: tuple[int]) -> int:
    result = 0

    if not springs:
        return len(broken_states) == 0
    if not broken_states:
        return "#" not in springs
    if springs[0] in "." or springs[0] == "?":
        result += calculate_arrangements(springs[1:], broken_states)
    if (
        (springs[0] == "#" or springs[0] == "?")
        and broken_states[0] <= len(springs)
        and "." not in springs[: broken_states[0]]
        and (broken_states[0] == len(springs) or springs[broken_states[0]] != "#")
    ):
        result += calculate_arrangements(
            springs[broken_states[0] + 1 :], broken_states[1:]
        )

    return result


def number_of_possible_arrangements(filename: str, debug: bool = False) -> int:
    with open(filename, "r", encoding="utf-8") as file:
        res = 0
        lines = file.readlines()
        for line in lines:
            springs, broken_states = line.strip().split(" ")
            broken_states = tuple(map(int, re.findall(r"\d+", broken_states)))
            res += calculate_arrangements(springs, broken_states)
        return res


def number_of_possible_arrangements_part_two(filename: str, debug: bool = False) -> int:
    with open(filename, "r", encoding="utf-8") as file:
        res = 0
        lines = file.readlines()
        for line in lines:
            springs, broken_states = line.strip().split(" ")
            broken_states = tuple(map(int, re.findall(r"\d+", broken_states)))
            broken_states = (broken_states) * 5
            springs = "?".join([springs] * 5)
            res += calculate_arrangements(springs, broken_states)
        return res


def main() -> None:
    test_one = False
    test_two = False

    if number_of_possible_arrangements(EXAMPLE) == 21:
        print("PASSED TEST: EXAMPLE 1")
        test_one = True

    if number_of_possible_arrangements_part_two(EXAMPLE) == 525152:
        print("PASSED TEST: EXAMPLE 2")
        test_two = True

    if test_one:
        print(
            f"Number of possible arrangements for Part One: {number_of_possible_arrangements(INPUT)}"
        )
    if test_two:
        print(
            f"Number of possible arrangements for Part Two: {number_of_possible_arrangements_part_two(INPUT)}"
        )

    return


if __name__ == "__main__":
    main()
