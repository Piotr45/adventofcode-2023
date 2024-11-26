"""Advent of code Day 8

You're still riding a camel across Desert Island when you spot a sandstorm quickly approaching. 
When you turn to warn the Elf, she disappears before your eyes! 
To be fair, she had just finished warning you about ghosts a few minutes ago.

One of the camel's pouches is labeled "maps" - sure enough, it's full of documents 
(your puzzle input) about how to navigate the desert. At least, you're pretty sure that's what they are; 
one of the documents contains a list of left/right instructions, 
and the rest of the documents seem to describe some kind of network of labeled nodes.

It seems like you're meant to use the left/right instructions to navigate the network. 
Perhaps if you have the camel follow the same instructions, you can escape the haunted wasteland!

--- Part Two ---

The sandstorm is upon you and you aren't any closer to escaping the wasteland.
 You had the camel follow the instructions, but you've barely left your starting position. 
 It's going to take significantly more steps to escape!

What if the map isn't for people - what if the map is for ghosts? 
Are ghosts even bound by the laws of spacetime? Only one way to find out.
"""

import re
import math

EXAMPLE_1 = "./example_1.txt"
EXAMPLE_2 = "./example_2.txt"
EXAMPLE_3 = "./example_3.txt"
INPUT = "./input.txt"


def how_many_steps(filename: str, debug: bool = False) -> int:
    steps = 0
    current_node = "AAA"
    end_node = "ZZZ"
    with open(filename, "r", encoding="utf-8") as file:
        lines = file.readlines()
        instructions = lines[0].rstrip("\n")
        nodes = {}
        for line in lines[2:]:
            node_val, left, right = re.findall(r"[A-Z]+", line)
            nodes[node_val.strip("\ ")] = {"L": left, "R": right}
        while True:
            for instruction in instructions:
                steps += 1
                current_node = nodes[current_node][instruction]
                if current_node == end_node:
                    return steps
    return steps


def how_many_steps_for_ghost(filename: str, debug: bool = False) -> int:
    steps = []
    current_nodes = []
    with open(filename, "r", encoding="utf-8") as file:
        lines = file.readlines()
        instructions = lines[0].rstrip("\n")
        nodes = {}
        for line in lines[2:]:
            node_val, left, right = re.findall(r"[0-9A-Z]+", line)
            nodes[node_val.strip("\ ")] = {"L": left, "R": right}
            if node_val[-1] == "A":
                current_nodes.append(node_val)
        for node in current_nodes:
            current_node = node
            step = 0
            search = True
            while search:
                for instruction in instructions:
                    step += 1
                    current_node = nodes[current_node][instruction]
                    if current_node[-1] == "Z":
                        steps.append(step)
                        search = False
                        break

    return math.lcm(*steps)


def main() -> None:
    test_one = False
    test_two = False

    if how_many_steps(EXAMPLE_1) == 2 and how_many_steps(EXAMPLE_2) == 6:
        print("PASSED TEST: EXAMPLE 1")
        test_one = True

    if how_many_steps_for_ghost(EXAMPLE_3) == 6:
        print("PASSED TEST: EXAMPLE 2")
        test_two = True

    if test_one:
        input_total_steps = how_many_steps(INPUT)
        print(
            f"The number of steps needed to reach ZZZ for Part One: {input_total_steps}"
        )
    if test_two:
        input_total_steps = how_many_steps_for_ghost(INPUT)
        print(f"The number of steps for ghost for Part Two: {input_total_steps}")

    return


if __name__ == "__main__":
    main()
