"""Advent of code Day 9

You ride the camel through the sandstorm and stop where the ghost's maps told you to stop. 
The sandstorm subsequently subsides, somehow seeing you standing at an oasis!

The camel goes to get some water and you stretch your neck. 
As you look up, you discover what must be yet another giant floating island, 
this one made of metal! That must be where the parts to fix the sand machines come from.

There's even a hang glider partially buried in the sand here; 
once the sun rises and heats up the sand, you might be able to use the glider 
and the hot air to get all the way up to the metal island!

While you wait for the sun to rise, you admire the oasis hidden here in the middle of Desert Island. 
It must have a delicate ecosystem; you might as well take some ecological readings while you wait. 
Maybe you can report any environmental instabilities you find to someone so the oasis can be around for the next sandstorm-worn traveler.

--- Part Two ---

Of course, it would be nice to have even more history included in your report. 
Surely it's safe to just extrapolate backwards as well, right?

For each history, repeat the process of finding differences until the sequence of differences is entirely zero. 
Then, rather than adding a zero to the end and filling in the next values of each previous sequence,
you should instead add a zero to the beginning of your sequence of zeroes, 
then fill in new first values for each previous sequence.
"""

import re

EXAMPLE = "./example.txt"
INPUT = "./input.txt"


def extrapolate(single_history: list) -> int:
    if all(h == 0 for h in single_history):
        return 0
    return extrapolate([single_history[idx + 1] - single_history[idx] for idx in range(len(single_history) - 1)]) + single_history[-1]


def extrapolate_backwards(single_history: list) -> int:
    if all(h == 0 for h in single_history):
        return 0
    return single_history[0] - extrapolate_backwards([single_history[idx + 1] - single_history[idx] for idx in range(len(single_history) - 1)])



def extrapolate_values(filename: str, debug: bool = False) -> int:
    with open(filename, "r", encoding="utf-8") as file:
        history = [
            list(map(int, re.findall(r"[\-0-9]+", line))) for line in file.readlines()
        ]
        return sum(
            [
                extrapolate(single_history)
                for single_history in history
            ]
        )


def extrapolate_values_part_two(filename: str, debug: bool = False) -> int:
    with open(filename, "r", encoding="utf-8") as file:
        history = [
            list(map(int, re.findall(r"[\-0-9]+", line))) for line in file.readlines()
        ]
        return sum(
            [
                extrapolate_backwards(single_history)
                for single_history in history
            ]
        )


def main() -> None:
    test_one = False
    test_two = False

    if extrapolate_values(EXAMPLE) == 114:
        print("PASSED TEST: EXAMPLE 1")
        test_one = True

    if extrapolate_values_part_two(EXAMPLE) == 2:
        print("PASSED TEST: EXAMPLE 2")
        test_two = True

    if test_one:
        print(
            f"The sum of these extrapolated values for Part One is: {extrapolate_values(INPUT)}"
        )
    if test_two:
        print(f"The sum of these extrapolated values for Part Two is: {extrapolate_values_part_two(INPUT)}")

    return


if __name__ == "__main__":
    main()
