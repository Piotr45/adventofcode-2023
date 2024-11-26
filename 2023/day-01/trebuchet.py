"""Advent of code Day 1

You try to ask why they can't just use a weather machine ("not powerful enough") and 
where they're even sending you ("the sky") and why your map looks mostly blank 
("you sure ask a lot of questions") and hang on did you just say the sky 
("of course, where do you think snow comes from") when you realize that the Elves are already loading you into a trebuchet
("please hold still, we need to strap you in").

As they're making the final adjustments, they discover that their calibration document
(your puzzle input) has been amended by a very young Elf who was apparently just excited to show off her art skills.
Consequently, the Elves are having trouble reading the values on the document.

The newly-improved calibration document consists of lines of text; 
each line originally contained a specific calibration value that the Elves now need to recover. 
On each line, the calibration value can be found by combining the first digit and the last digit (in that order) to form a single two-digit number.

--- Part Two ---

Your calculation isn't quite right. It looks like some of the digits 
are actually spelled out with letters: one, two, three, four, five, six, seven, eight, and nine also count as valid "digits".

Equipped with this new information, you now need to find the real first and last digit on each line.
"""

# Input files
EXAMPLE_1 = "./example_1.txt"
EXAMPLE_2 = "./example_2.txt"
INPUT = "./input.txt"

# Words
NUMBERS = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]


def decode_text_part_one(filename: str, debug: bool = False) -> int:
    calibration_sum = 0
    with open(filename, 'r', encoding='utf-8') as example:
        for line in example.readlines():
            line = line.rstrip('\n')
            digits = [char for char in line if char.isdigit()]
            code = int(digits[0] + digits[-1])
            if debug:
                print(line, code)
            calibration_sum += code
    return calibration_sum


def decode_text_part_two(filename: str, debug: bool = False) -> int:
    calibration_sum = 0
    with open(filename, 'r', encoding='utf-8') as example:
        for line in example.readlines():
            digits = []
            line = line.rstrip('\n')
            for idx, char in enumerate(line):
                if char.isdigit():
                    digits.append(char)
                for num, word_num in enumerate(NUMBERS):
                    if line[idx:].startswith(word_num):
                        digits.append(str(num + 1))
            code = int(digits[0] + digits[-1])
            if debug:
                print(line, code)
            calibration_sum += code
    return calibration_sum


def main() -> None:
    test_one = False
    test_two = False

    example_calibration = decode_text_part_one(EXAMPLE_1)
    if example_calibration == 142:
        print("PASSED TEST: EXAMPLE 1")
        test_one = True

    example_calibration = decode_text_part_two(EXAMPLE_2)
    if example_calibration == 281:
        print("PASSED TEST: EXAMPLE 2")
        test_two = True
    
    if test_one:
        input_calibration = decode_text_part_one(INPUT)
        print(f"Sum of calibration values of input for Part One: {input_calibration}")
    if test_two:
        input_calibration = decode_text_part_two(INPUT)
        print(f"Sum of calibration values of input for Part Two: {input_calibration}")
    return

if __name__ == '__main__':
    main()
