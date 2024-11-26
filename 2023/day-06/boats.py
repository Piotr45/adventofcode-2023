"""Advent of code Day 6

The ferry quickly brings you across Island Island. After asking around, 
you discover that there is indeed normally a large pile of sand somewhere near here, 
but you don't see anything besides lots of water and the small island where the ferry has docked.

As you try to figure out what to do next, you notice a poster on a wall near the ferry dock. 
"Boat races! Open to the public! Grand prize is an all-expenses-paid trip to Desert Island!" 
That must be where the sand comes from! Best of all, the boat races are starting in just a few minutes.

You manage to sign up as a competitor in the boat races just in time. 
The organizer explains that it's not really a traditional race - instead, 
you will get a fixed amount of time during which your boat has to travel as far as it can, 
and you win if your boat goes the farthest.

As part of signing up, you get a sheet of paper (your puzzle input) that lists the time allowed for each race 
and also the best distance ever recorded in that race. To guarantee you win the grand prize, 
you need to make sure you go farther in each race than the current record holder.

The organizer brings you over to the area where the boat races are held. 
The boats are much smaller than you expected - they're actually toy boats, 
each with a big button on top. Holding down the button charges the boat, 
and releasing the button allows the boat to move. 
Boats move faster if their button was held longer, 
but time spent holding the button counts against the total race time. 
You can only hold the button at the start of the race, and boats don't move until the button is released.

--- Part Two ---

As the race is about to start, you realize the piece of paper with race times and record distances you got earlier 
actually just has very bad kerning. There's really only one race - ignore the spaces between the numbers on each line.

"""


import re

EXAMPLE_1 = "./example_1.txt"
EXAMPLE_2 = "./example_2.txt"

INPUT = "./input.txt"


def calc_distance(push_button_time: int, race_time: int) -> int:
    return push_button_time * (race_time - push_button_time)


def beat_the_record(filename: str, debug: bool = False) -> int:
    time, distance = [], []
    result = 1
    with open(filename, "r", encoding="utf-8") as file:
        lines = file.readlines()
        times = list(map(int, re.findall(r"(\d+)", lines[0])))
        distances = list(map(int, re.findall(r"(\d+)", lines[1])))
    for time, distance in zip(times, distances):
        winning_races = 0
        for t in range(time + 1):
            if debug:
                print(t, time, calc_distance(t, time), distance)
            if calc_distance(t, time) > distance:
                winning_races += 1
        result *= winning_races
    return result


def beat_the_record_part_two(filename: str, debug: bool = False) -> int:
    min_time_val, max_time_val = None, None
    with open(filename, "r", encoding="utf-8") as file:
        lines = file.readlines()
        time = int("".join(re.findall(r"(\d+)", lines[0])))
        distance = int("".join(re.findall(r"(\d+)", lines[1])))
    
        for t in range(time):
            if debug:
                print("MIN", t, time, calc_distance(t, time), distance)
            if calc_distance(t, time) > distance:
                min_time_val = t
                break
        for t in range(time + 1)[::-1]:
            if debug:
                print("MAX", t, time, calc_distance(t, time), distance)
            if calc_distance(t, time) > distance:
                max_time_val = t
                break
        return max_time_val - min_time_val + 1


def main() -> None:
    test_one = False
    test_two = False

    example_ways_to_beat_record = beat_the_record(EXAMPLE_1)
    if example_ways_to_beat_record == 288:
        print("PASSED TEST: EXAMPLE 1")
        test_one = True

    example_ways_to_beat_record = beat_the_record_part_two(EXAMPLE_1)
    if example_ways_to_beat_record == 71503:
        print("PASSED TEST: EXAMPLE 2")
        test_two = True

    if test_one:
        input_ways_to_beat_record = beat_the_record(INPUT)
        print(f"Number of ways to beat the record for Part One: {input_ways_to_beat_record}")
    if test_two:
        input_ways_to_beat_record = beat_the_record_part_two(INPUT)
        print(f"Lowest location for Part Two: {input_ways_to_beat_record}")

    return


if __name__ == "__main__":
    main()
