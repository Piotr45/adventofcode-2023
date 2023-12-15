"""Advent of code Day 15

The newly-focused parabolic reflector dish is sending all of the collected light to 
a point on the side of yet another mountain - the largest mountain on Lava Island. 
As you approach the mountain, you find that the light is being collected by
 the wall of a large facility embedded in the mountainside.

You find a door under a large sign that says "Lava Production Facility" and 
next to a smaller sign that says "Danger - Personal Protective Equipment required beyond this point".

As you step inside, you are immediately greeted by a somewhat panicked reindeer wearing goggles 
and a loose-fitting hard hat. The reindeer leads you to a shelf of goggles 
and hard hats (you quickly find some that fit) and then further into the facility. 
At one point, you pass a button with a faint snout mark and the label "PUSH FOR HELP". 
No wonder you were loaded into that trebuchet so quickly!

You pass through a final set of doors surrounded with even more warning signs 
and into what must be the room that collects all of the light from outside. 
As you admire the large assortment of lenses available to further focus the light, 
the reindeer brings you a book titled "Initialization Manual".

"Hello!", the book cheerfully begins, apparently unaware of the concerned reindeer reading over your shoulder. 
"This procedure will let you bring the Lava Production Facility online - all without burning or melting anything unintended!"

"Before you begin, please be prepared to use the Holiday ASCII String Helper algorithm (appendix 1A)."
 You turn to appendix 1A. The reindeer leans closer with interest.

--- Part Two ---

You convince the reindeer to bring you the page; the page confirms that your HASH algorithm is working.

The book goes on to describe a series of 256 boxes numbered 0 through 255. 
The boxes are arranged in a line starting from the point where light enters the facility. 
The boxes have holes that allow light to pass from one box to the next all the way down the line.

Inside each box, there are several lens slots that will keep a lens correctly positioned 
to focus light passing through the box. The side of each box has a panel 
that opens to allow you to insert or remove lenses as necessary.

Along the wall running parallel to the boxes is a large library containing lenses organized 
by focal length ranging from 1 through 9. The reindeer also brings you a small handheld label printer.

The book goes on to explain how to perform each step in the initialization sequence, 
a process it calls the Holiday ASCII String Helper Manual Arrangement Procedure, or HASHMAP for short.

Each step begins with a sequence of letters that indicate the label of the lens on which the step operates. 
The result of running the HASH algorithm on the label indicates the correct box for that step.
"""

import re

EXAMPLE = "./example.txt"
INPUT = "./input.txt"


def get_hash(
    char: str, prev_num: int = 0, multiplier: int = 17, divider: int = 256
) -> int:
    return ((prev_num + ord(char)) * multiplier) % divider


def hash_sum(filename: str) -> int:
    with open(filename, "r", encoding="utf-8") as file:
        codes = file.readline().strip().split(",")
        sum_ = 0
        for code in codes:
            prev_num = 0
            for char in code.strip():
                prev_num = get_hash(char, prev_num)
            sum_ += prev_num
        return sum_


def calc_focusing_power(boxes: list) -> int:
    _sum = 0
    for box_id, box in enumerate(boxes):
        for idx, (key, val) in enumerate(box.items()):
            _sum += (box_id + 1) * val * (idx + 1)
    return _sum


def get_focusing_power(filename: str) -> int:
    with open(filename, "r", encoding="utf-8") as file:
        codes = file.readline().strip().split(",")
        boxes = [{} for _ in range(256)]
        for code in codes:
            lens_name, sign = (
                re.findall("[a-z]+", code)[0],
                re.findall("[\-=]", code)[0],
            )
            relevant_box = 0
            for c in lens_name:
                relevant_box = get_hash(c, relevant_box)

            if sign == "-":
                if lens_name in boxes[relevant_box].keys():
                    boxes[relevant_box].pop(lens_name)
            elif sign == "=":
                focal_length = int(re.findall("\d+", code)[0])
                boxes[relevant_box][lens_name] = focal_length
        return calc_focusing_power(boxes)


def main() -> None:
    test_one = False
    test_two = False

    if hash_sum(EXAMPLE) == 1320:
        print("PASSED TEST: EXAMPLE 1")
        test_one = True

    if get_focusing_power(EXAMPLE) == 145:
        print("PASSED TEST: EXAMPLE 2")
        test_two = True

    if test_one:
        print(f"Sum of the results for Part One: {hash_sum(INPUT)}")
    if test_two:
        print(f"Focusing power for Part Two: {get_focusing_power(INPUT)}")

    return


if __name__ == "__main__":
    main()
