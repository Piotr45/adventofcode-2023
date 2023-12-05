"""Advent of code Day 5

You take the boat and find the gardener right where you were told he would be: 
managing a giant "garden" that looks more to you like a farm.

"A water source? Island Island is the water source!" 
You point out that Snow Island isn't receiving any water.

"Oh, we had to stop the water because we ran out of sand to filter it with! 
Can't make snow with dirty water. Don't worry, I'm sure we'll get more sand soon; 
we only turned off the water a few days... weeks... oh no."
His face sinks into a look of horrified realization.

"I've been so busy making sure everyone here has food that I completely forgot to check why we stopped getting more sand! 
There's a ferry leaving soon that is headed over in that direction - it's much faster than your boat. 
Could you please go check it out?"

You barely have time to agree to this request when he brings up another. 
"While you wait for the ferry, maybe you can help us with our food production problem. 
The latest Island Island Almanac just arrived and we're having trouble making sense of it."

The almanac (your puzzle input) lists all of the seeds that need to be planted.
It also lists what type of soil to use with each kind of seed, 
what type of fertilizer to use with each kind of soil, 
what type of water to use with each kind of fertilizer, 
and so on. Every type of seed, soil, fertilizer and so on is identified with a number, 
but numbers are reused by each category - that is, soil 123 and fertilizer 123 aren't necessarily related to each other.

--- Part Two ---

Everyone will starve if you only plant such a small number of seeds. 
Re-reading the almanac, it looks like the seeds: line actually describes ranges of seed numbers.

The values on the initial seeds: line come in pairs. Within each pair, 
the first value is the start of the range and the second value is the length of the range. 
So, in the first line of the example above:

seeds: 79 14 55 13
This line describes two ranges of seed numbers to be planted in the garden. 
The first range starts with seed number 79 and contains 14 values: 79, 80, ..., 91, 92. 
The second range starts with seed number 55 and contains 13 values: 55, 56, ..., 66, 67.

Now, rather than considering four seed numbers, you need to consider a total of 27 seed numbers.

In the above example, the lowest location number can be obtained from seed number 82, 
which corresponds to soil 84, fertilizer 84, water 84, light 77, temperature 45, humidity 46, 
and location 46. So, the lowest location number is 46.

Consider all of the initial seed numbers listed in the ranges on the first line of the almanac. 
What is the lowest location number that corresponds to any of the initial seed numbers?
"""

import re

EXAMPLE_1 = "./example_1.txt"

INPUT = "./input.txt"


def create_map(dst: list[int], src: list[int], length: list[int]) -> list:
    _map = []
    for d, s, l in zip(dst, src, length):
        min_src = s
        max_src = s + l - 1
        min_dst = d
        max_dst = d + l - 1
        _map.append([min_dst, max_dst, min_src, max_src])
    return _map


def map_seeds(seeds: list, seed_map: dict) -> list:
    res = [None for _ in range(len(seeds))]
    for i, seed in enumerate(seeds):
        beetween_value = [
            min_src <= seed <= max_src
            for min_dst, max_dst, min_src, max_src in seed_map
        ]
        if beetween_value.count(True):
            min_dst, max_dst, min_src, max_src = seed_map[beetween_value.index(True)]
            conversion = min_src - min_dst
            res[i] = seed - conversion
        else:
            res[i] = seed
    return res


def find_lowest_location(filename: str, debug: bool = False) -> int:
    current_map = 0
    seeds = None
    dst, src, length = [], [], []
    with open(filename, "r", encoding="utf-8") as file:
        lines = file.readlines()
        for i, line in enumerate(lines):
            if i == 0:
                seeds = list(map(int, re.findall(r"(\d+)", line.lstrip("seeds: "))))
                continue
            elif i == 1:
                continue
            nums = list(map(int, re.findall(r"(\d+)", line)))
            if len(nums):
                dst.append(nums[0])
                src.append(nums[1])
                length.append(nums[2])
            # print(nums, dst, src, length)
            if len(nums) == 0 and len(dst) != 0:
                if debug:
                    print(f"Processing map {current_map}")
                    current_map += 1
                seed_map = create_map(dst, src, length)
                seeds = map_seeds(seeds, seed_map)
                dst, src, length = [], [], []
    if len(nums) != 0 and len(dst) != 0:
        if debug:
            print(f"Processing map {current_map}")
            current_map += 1
        seed_map = create_map(dst, src, length)
        seeds = map_seeds(seeds, seed_map)
    return min(seeds)


def find_lowest_location_part_two(filename: str, debug: bool = False) -> int:
    current_map = 0
    seeds = None
    dst, src, length = [], [], []
    with open(filename, "r", encoding="utf-8") as file:
        lines = file.readlines()
        for i, line in enumerate(lines):
            if i == 0:
                seeds_org = list(map(int, re.findall(r"(\d+)", line.lstrip("seeds: "))))
                seeds = []
                for j in range(0, len(seeds_org), 2):
                    # print(j, seeds_org[j+1])
                    seeds += [seeds_org[j] + k for k in range(seeds_org[j+1])]
                    print(seeds, len(seeds))
                continue
            elif i == 1:
                continue
            nums = list(map(int, re.findall(r"(\d+)", line)))
            if len(nums):
                dst.append(nums[0])
                src.append(nums[1])
                length.append(nums[2])
            # print(nums, dst, src, length)
            if len(nums) == 0 and len(dst) != 0:
                if debug:
                    print(f"Processing map {current_map}")
                    current_map += 1
                seed_map = create_map(dst, src, length)
                seeds = map_seeds(seeds, seed_map)
                dst, src, length = [], [], []
    if len(nums) != 0 and len(dst) != 0:
        if debug:
            print(f"Processing map {current_map}")
            current_map += 1
        seed_map = create_map(dst, src, length)
        seeds = map_seeds(seeds, seed_map)
    return min(seeds)

    return


def main() -> None:
    test_one = False
    test_two = False

    example_location = find_lowest_location(EXAMPLE_1)
    if example_location == 35:
        print("PASSED TEST: EXAMPLE 1")
        test_one = True

    example_location = find_lowest_location_part_two(EXAMPLE_1)
    if example_location == 46:
        print("PASSED TEST: EXAMPLE 2")
        test_two = True

    if test_one:
        input_location = find_lowest_location(INPUT)
        print(f"Lowest location for Part One: {input_location}")
    if test_two:
        input_location = find_lowest_location_part_two(INPUT)
        print(f"Lowest location for Part Two: {input_location}")

    return


if __name__ == "__main__":
    main()
