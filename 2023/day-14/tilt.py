"""Advent of code Day 14

You reach the place where all of the mirrors were pointing: a massive parabolic reflector dish 
attached to the side of another large mountain.

The dish is made up of many small mirrors, but while the mirrors themselves are roughly 
in the shape of a parabolic reflector dish, each individual mirror seems to be pointing 
in slightly the wrong direction. If the dish is meant to focus light, 
all it's doing right now is sending it in a vague direction.

This system must be what provides the energy for the lava! If you focus the reflector dish, 
maybe you can go where it's pointing and use the light to fix the lava production.

Upon closer inspection, the individual mirrors each appear to be connected via an elaborate system of ropes 
and pulleys to a large metal platform below the dish. The platform is covered in large rocks of various shapes. 
Depending on their position, the weight of the rocks deforms the platform, 
and the shape of the platform controls which ropes move and ultimately the focus of the dish.

--- Part Two ---
The parabolic reflector dish deforms, but not in a way that focuses the beam. To do that, 
you'll need to move the rocks to the edges of the platform. Fortunately, 
a button on the side of the control panel labeled "spin cycle" attempts to do just that!

Each cycle tilts the platform four times so that the rounded rocks roll north, then west, 
then south, then east. After each tilt, the rounded rocks roll as far as they can before the platform 
tilts in the next direction. After one cycle, the platform will have finished rolling the rounded rocks 
in those four directions in that order.
"""

EXAMPLE = "./example.txt"
INPUT = "./input.txt"


def transpose(pattern) -> list:
    return [*zip(*pattern)]


def tilt_north(grid: list) -> list:
    grid_shape = (len(grid), len(grid[0]))
    for i in range(grid_shape[0]):
        for j in range(grid_shape[1]):
            move_north = i - 1
            if grid[i][j] == "O":
                while True:
                    if move_north < 0:
                        break
                    if grid[move_north][j] in "#O":
                        break
                    move_north -= 1
                if move_north + 1 == i:
                    continue
                grid[move_north + 1][j] = "O"
                grid[i][j] = "."
    return grid


def tilt_south(grid: list) -> list:
    grid_shape = (len(grid), len(grid[0]))
    for i in range(grid_shape[0])[::-1]:
        for j in range(grid_shape[1]):
            move_north = i + 1
            if grid[i][j] == "O":
                while True:
                    if move_north >= grid_shape[0]:
                        break
                    if grid[move_north][j] in "#O":
                        break
                    move_north += 1
                if move_north - 1 == i:
                    continue
                grid[move_north - 1][j] = "O"
                grid[i][j] = "."
    return grid


def tilt_west(grid: list) -> list:
    grid_shape = (len(grid), len(grid[0]))
    for i in range(grid_shape[0]):
        for j in range(grid_shape[1]):
            move_north = j - 1
            if grid[i][j] == "O":
                while True:
                    if move_north < 0:
                        break
                    if grid[i][move_north] in "#O":
                        break
                    move_north -= 1
                if move_north + 1 == j:
                    continue
                grid[i][move_north + 1] = "O"
                grid[i][j] = "."
    return grid


def tilt_east(grid: list) -> list:
    grid_shape = (len(grid), len(grid[0]))
    for i in range(grid_shape[0]):
        for j in range(grid_shape[1])[::-1]:
            move_north = j + 1
            if grid[i][j] == "O":
                while True:
                    if move_north >= grid_shape[1]:
                        break
                    if grid[i][move_north] in "#O":
                        break
                    move_north += 1
                if move_north - 1 == j:
                    continue
                grid[i][move_north - 1] = "O"
                grid[i][j] = "."
    return grid


def cycle(grid: list) -> list:
    return tilt_east(tilt_south(tilt_west(tilt_north(grid))))


def calc_load(grid: list) -> int:
    return sum([grid[i].count("O") * (len(grid) - i) for i in range(len(grid))])


def reshape_flat_grid(flattened_grid: list, grid_shape: tuple) -> list:
    return [
        flattened_grid[j * grid_shape[1] : (j + 1) * grid_shape[1]]
        for j in range(grid_shape[0])
    ]


def total_load(filename: str, num_cycles: int = 10**9, part2: bool = False) -> int:
    with open(filename, "r", encoding="utf-8") as file:
        grid = [list(line.strip()) for line in file.readlines()]
        grid_shape = (len(grid), len(grid[0]))
        if part2:
            grid_cache = {}
            for idx in range(10**9):
                grid = cycle(grid)

                flattened_grid = "".join(["".join(g) for g in grid])
                if flattened_grid in grid_cache.keys():
                    break
                grid_cache[flattened_grid] = idx

            cycles_init = grid_cache[flattened_grid] + 1
            loop_size = idx - grid_cache[flattened_grid]
            cycles_left = cycles_init + (10**9 - cycles_init) % loop_size - 1

            for flattened_grid, value in grid_cache.items():
                if value == cycles_left:
                    grid = reshape_flat_grid(flattened_grid, grid_shape)
                    break

        else:
            grid = tilt_north(grid)
        return calc_load(grid)


def main() -> None:
    test_one = False
    test_two = False

    if total_load(EXAMPLE) == 136:
        print("PASSED TEST: EXAMPLE 1")
        test_one = True

    # print(total_load(EXAMPLE, part2=True))
    if total_load(EXAMPLE, part2=True) == 64:
        print("PASSED TEST: EXAMPLE 2")
        test_two = True

    if test_one:
        print(f"Total load for Part One: {total_load(INPUT)}")
    if test_two:
        print(
            f"Total load for Part Two: {total_load(INPUT, part2=True)}"
        )

    return


if __name__ == "__main__":
    main()
