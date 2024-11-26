"""Advent of code Day 16

With the beam of light completely focused somewhere, 
the reindeer leads you deeper still into the Lava Production Facility. 
At some point, you realize that the steel facility walls have been replaced with cave, 
and the doorways are just cave, and the floor is cave, and you're pretty sure this is actually just a giant cave.

Finally, as you approach what must be the heart of the mountain, 
you see a bright light in a cavern up ahead. There, you discover that the beam of light you so 
carefully focused is emerging from the cavern wall closest to the facility and 
pouring all of its energy into a contraption on the opposite side.

Upon closer inspection, the contraption appears to be a flat, 
two-dimensional square grid containing empty space (.), mirrors (/ and \), and splitters (| and -).

The contraption is aligned so that most of the beam bounces around the grid, 
but each tile on the grid converts some of the beam's light into heat to melt the rock in the cavern.

--- Part Two ---

As you try to work out what might be wrong, 
the reindeer tugs on your shirt and leads you to a nearby control panel. 
There, a collection of buttons lets you align the contraption so that 
the beam enters from any edge tile and heading away from that edge. 
(You can choose either of two directions for the beam if it starts on a corner; for instance, 
if the beam starts in the bottom-right corner, it can start heading either left or upward.)

So, the beam could start on any tile in the top row (heading downward), 
any tile in the bottom row (heading upward), any tile in the leftmost column (heading right), 
or any tile in the rightmost column (heading left). 
To produce lava, you need to find the configuration that energizes as many tiles as possible.
"""

EXAMPLE = "./example.txt"
INPUT = "./input.txt"


def count_energized_tiles(position: int, direction: int):
    global complex_grid
    to_visit = set([(position, direction)])
    visited = set()
    while to_visit:
        new_position, new_direction = to_visit.pop()
        while not (new_position, new_direction) in visited:
            visited.add((new_position, new_direction))
            new_position += new_direction
            if complex_grid.get(new_position) == "-":
                new_direction = 1
                to_visit.add((new_position, -new_direction))
            if complex_grid.get(new_position) == "|":
                new_direction = 1j
                to_visit.add((new_position, -new_direction))
            if complex_grid.get(new_position) == "/":
                new_direction = -complex(new_direction.imag, new_direction.real)
            if complex_grid.get(new_position) == "\\":
                new_direction = complex(new_direction.imag, new_direction.real)
            if complex_grid.get(new_position) is None:
                break
    return len(set(x for x, _ in visited)) - 1


def light_beam(filename: str, part2: bool = False) -> int:
    with open(filename, "r", encoding="utf-8") as file:
        global complex_grid
        grid = [line.strip() for line in file.readlines()]
        complex_grid = {
            i + j * 1j: col for j, row in enumerate(grid) for i, col in enumerate(row)
        }

        if part2:
            collection_of_positions = zip(
                *[
                    (posistion - direction, direction)
                    for posistion in complex_grid
                    for direction in (1, 1j, -1, -1j)
                    if posistion - direction not in complex_grid
                ]
            )
            return max(map(count_energized_tiles, *collection_of_positions))
        else:
            return count_energized_tiles(-1, 1)


def main() -> None:
    test_one = False
    test_two = False

    if light_beam(EXAMPLE) == 46:
        print("PASSED TEST: EXAMPLE 1")
        test_one = True

    if light_beam(EXAMPLE, part2=True) == 51:
        print("PASSED TEST: EXAMPLE 2")
        test_two = True

    if test_one:
        print(f"Energized tiles for Part One are equal: {light_beam(INPUT)}")

    if test_two:
        print(
            f"Energized tiles for Part Two are equal: {light_beam(INPUT, part2=True)}"
        )
    return


if __name__ == "__main__":
    main()
