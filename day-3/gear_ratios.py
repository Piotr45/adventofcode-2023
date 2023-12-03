"""Advent of code Day 3

You and the Elf eventually reach a gondola lift station; 
he says the gondola lift will take you up to the water source, 
but this is as far as he can bring you. You go inside.

It doesn't take long to find the gondolas, 
but there seems to be a problem: they're not moving.

"Aaah!"

You turn around to see a slightly-greasy Elf with a wrench and a look of surprise. 
"Sorry, I wasn't expecting anyone! The gondola lift isn't working right now; 
it'll still be a while before I can fix it." You offer to help.

The engineer explains that an engine part seems to be missing from the engine, 
but nobody can figure out which one. If you can add up all the part numbers in the engine schematic, 
it should be easy to work out which part is missing.

The engine schematic (your puzzle input) consists of a visual representation of the engine. 
There are lots of numbers and symbols you don't really understand, 
but apparently any number adjacent to a symbol, even diagonally, 
is a "part number" and should be included in your sum. (Periods (.) do not count as a symbol.)

--- Part Two ---
The engineer finds the missing part and installs it in the engine! 
As the engine springs to life, you jump in the closest gondola, 
finally ready to ascend to the water source.

You don't seem to be going very fast, though. Maybe something is still wrong?
Fortunately, the gondola has a phone labeled "help", so you pick it up and the engineer answers.

Before you can explain the situation, she suggests that you look out the window. 
There stands the engineer, holding a phone in one hand and waving with the other. 
You're going so slowly that you haven't even left the station. You exit the gondola.

The missing part wasn't the only issue - one of the gears in the engine is wrong.
A gear is any * symbol that is adjacent to exactly two part numbers. 
Its gear ratio is the result of multiplying those two numbers together.

This time, you need to find the gear ratio of every gear and add them all up 
so that the engineer can figure out which gear needs to be replaced.
"""

import re

# Input files
EXAMPLE_1 = "./example_1.txt"
INPUT = "./input.txt"


def get_matrix(schematic: list) -> bool:
    matrix = []
    for row, line in enumerate(schematic):
        for col, c in enumerate(line[::]):
            if not c.isdigit() and c != "." and c != "\n":
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        if i == 0 and j == 0:
                            continue
                        matrix.append((row + i, col + j))
    return matrix


def get_sum_of_parts(filename: str) -> int:
    sum_of_prats = 0
    with open(filename, "r", encoding="utf-8") as file:
        schematic = file.readlines()
        matrix = get_matrix(schematic)
        for row, line in enumerate(schematic):
            nums = re.findall(r"(\d+)", line)
            lf = 0
            for num in nums:
                idx = line.find(num, lf)
                lf = idx + len(num)
                for col in range(idx, idx + len(num)):
                    if (row, col) in matrix:
                        sum_of_prats += int(num)
                        break
    return sum_of_prats


def get_gear_ratios(filename: str) -> int:
    possible_gears = {}
    gear_idxs = []
    with open(filename, "r", encoding="utf-8") as file:
        schematic = file.readlines()
        matrix = get_matrix(schematic)
        for row, line in enumerate(schematic):
            nums = re.findall(r"(\d+)", line)
            lf = 0
            for num in nums:
                idx = line.find(num, lf)
                lf = idx + len(num)
                for col in range(idx, idx + len(num)):
                    if ((row, col)) in matrix:
                        gear_idx = int(matrix.index((row, col)) / 8)
                        if gear_idx in list(possible_gears.keys()):
                            possible_gears[gear_idx] *= int(num)
                            gear_idxs.append(gear_idx)
                        else:
                            possible_gears[gear_idx] = int(num)
                        break
    return sum([possible_gears[i] for i in list(set(gear_idxs))])


def main() -> None:
    test_one = False
    test_two = False

    example_sum = get_sum_of_parts(EXAMPLE_1)
    if example_sum == 4361:
        print("PASSED TEST: EXAMPLE 1")
        test_one = True

    example_gear_ratios = get_gear_ratios(EXAMPLE_1)
    if example_gear_ratios == 467835:
        print("PASSED TEST: EXAMPLE 2")
        test_two = True

    if test_one:
        input_sum = get_sum_of_parts(INPUT)
        print(f"Sum of all adjacent numbers for Part One: {input_sum}")
    if test_two:
        input_gear_ratio = get_gear_ratios(INPUT)
        print(f"Sum of gear ratios for Part Two: {input_gear_ratio}")
    return


if __name__ == "__main__":
    main()
