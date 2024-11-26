"""Advent of code Day 17

The lava starts flowing rapidly once the Lava Production Facility is operational. 
As you leave, the reindeer offers you a parachute, allowing you to quickly reach Gear Island.

As you descend, your bird's-eye view of Gear Island reveals why you had trouble finding anyone on your way up: 
half of Gear Island is empty, but the half below you is a giant factory city!

You land near the gradually-filling pool of lava at the base of your new lavafall. 
Lavaducts will eventually carry the lava throughout the city, but to make use of it immediately, 
Elves are loading it into large crucibles on wheels.

The crucibles are top-heavy and pushed by hand. Unfortunately, 
the crucibles become very difficult to steer at high speeds, 
and so it can be hard to go in a straight line for very long.

To get Desert Island the machine parts it needs as soon as possible, 
you'll need to find the best way to get the crucible from the lava pool to the machine parts factory. 
To do this, you need to minimize heat loss while choosing a route that doesn't require the crucible to go in a straight line for too long.

Fortunately, the Elves here have a map (your puzzle input) that uses traffic patterns, 
ambient temperature, and hundreds of other parameters to calculate exactly how much heat loss can be expected 
for a crucible entering any particular city block.

--- Part Two ---

The crucibles of lava simply aren't large enough to provide an adequate supply of lava to the machine parts factory. 
Instead, the Elves are going to upgrade to ultra crucibles.

Ultra crucibles are even more difficult to steer than normal crucibles. 
Not only do they have trouble going in a straight line, but they also have trouble turning!

Once an ultra crucible starts moving in a direction, 
it needs to move a minimum of four blocks in that direction before it can turn 
(or even before it can stop at the end). However, it will eventually start to get wobbly: 
an ultra crucible can move a maximum of ten consecutive blocks without turning.
"""

from heapq import heappush, heappop

EXAMPLE = "./example.txt"
INPUT = "./input.txt"


DIRECTIONS = ((0, 1), (1, 0), (0, -1), (-1, 0))


def find_shortest_path(grid: dir, min_steps: int, max_steps: int, grid_end: tuple) -> int:
    to_visit = [(0, 0, (0, 0), (0, 1)), (0, 0, (0, 0), (1, 0))] # you can go right or down from point (0, 0)
    visited = set()
    moves = 0

    while to_visit:
        cost, m, position, direction = heappop(to_visit)

        if position == grid_end:
            return cost
        if (position, direction) in visited:
            continue
        visited.add((position, direction))
        
        for new_direction in DIRECTIONS:
            if new_direction == direction: # cant go further in this direction
                continue
            if -new_direction[0] == direction[0] and -new_direction[1] == direction[1]: # dont go back
                continue
            for step in range(min_steps, max_steps + 1):
                new_position = (position[0] + new_direction[0] * step, position[1] + new_direction[1] * step)
                if new_position in grid.keys():
                    v = sum([grid[(position[0] + new_direction[0] * j, position[1] + new_direction[1] * j)] for j in range(1, step + 1)])
                    heappush(to_visit, (cost+v, (moves:=moves+1), new_position, new_direction))


def calc_cost(filename: str, part2: bool = False) -> int:
    with open(filename, "r", encoding="utf-8") as file:
        grid = [line.strip() for line in file.readlines()]
        grid_end = (len(grid) - 1, len(grid[0])- 1)
        grid_costs = {(x, y): int(v) for x, r in enumerate(grid) for y, v in enumerate(r)}
        if part2:
            return find_shortest_path(grid_costs, 4, 10, grid_end)
        else:
            return find_shortest_path(grid_costs, 1, 3, grid_end)


def main() -> None:
    test_one = False
    test_two = False

    if calc_cost(EXAMPLE) == 102:
        print("PASSED TEST: EXAMPLE 1")
        test_one = True

    if calc_cost(EXAMPLE, part2=True) == 94:
        print("PASSED TEST: EXAMPLE 2")
        test_two = True

    if test_one:
        print(f"The least heat loss for Part One: {calc_cost(INPUT)}")

    if test_two:
        print(
            f"The least heat loss for Part Two: {calc_cost(INPUT, part2=True)}"
        )
    return


if __name__ == "__main__":
    main()
