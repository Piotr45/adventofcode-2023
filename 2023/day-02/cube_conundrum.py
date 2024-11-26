"""Advent of code Day 2

You're launched high into the atmosphere! The apex of your trajectory just barely reaches
the surface of a large island floating in the sky. You gently land in a fluffy pile of leaves. 
It's quite cold, but you don't see much snow. An Elf runs over to greet you.

The Elf explains that you've arrived at Snow Island and apologizes for the lack of snow. 
He'll be happy to explain the situation, but it's a bit of a walk, so you have some time. 
They don't get many visitors up here; would you like to play a game in the meantime?

As you walk, the Elf shows you a small bag and some cubes which are either red, green, or blue. 
Each time you play this game, he will hide a secret number of cubes of each color in the bag, 
and your goal is to figure out information about the number of cubes.

To get information, once a bag has been loaded with cubes, 
the Elf will reach into the bag, grab a handful of random cubes, show them to you, 
and then put them back in the bag. He'll do this a few times per game.

You play several games and record the information from each game (your puzzle input). 
Each game is listed with its ID number (like the 11 in Game 11: ...) followed by a semicolon-separated 
list of subsets of cubes that were revealed from the bag (like 3 red, 5 green, 4 blue).

The Elf would first like to know which games would have been possible if the bag contained only 12 red cubes, 13 green cubes, and 14 blue cubes?

--- Part Two ---

The Elf says they've stopped producing snow because they aren't getting any water! 
He isn't sure why the water stopped; however, he can show you how to get to 
the water source to check it out for yourself. It's just up ahead!

As you continue your walk, the Elf poses a second question: in each game you played, 
what is the fewest number of cubes of each color that could have been in the bag to make the game possible?
"""

RED = 12
GREEN = 13
BLUE = 14

EXAMPLE = "./example_1.txt"

INPUT = "./input.txt"


def is_game_possible(cube_color: str, num_cubes: int) -> bool:
    if cube_color == "red" and num_cubes <= RED:
        return True
    elif cube_color == "green" and num_cubes <= GREEN:
        return True
    elif cube_color == "blue" and num_cubes <= BLUE:
        return True
    return False

def find_min_val_fo_cubes(cube_collection: dict, debug: bool = False) -> int:
    power = 1
    for cube_color, collection in cube_collection.items():
        power *= max(collection)
        if debug:
            print(f"Min val of cubes for color {cube_color} is {max(collection)}")
    return power


def all_elf_lies(filename: str, debug: bool = False) -> int:
    possible_games_sum = 0
    with open(filename, 'r', encoding="utf-8") as file:
        lines = file.readlines()
        for line in lines:
            line = line.rstrip("\n")
            game, subsets = line.split(':')
            subsets = subsets.split(';')
            game_id = game.lstrip("Game ")
            # Single game
            possible = True
            for subset in subsets:
                cubes = [cubes.strip().split(' ') for cubes in subset.split(',')]
                for num_cubes, cube_color in cubes:
                    if not is_game_possible(cube_color, int(num_cubes)):
                        possible = False
            if possible:
                if debug:
                    print(f"Game {game_id} should be possible.")
                possible_games_sum += int(game_id)

    return possible_games_sum


def all_elf_lies_part_two(filename: str, debug: bool = False) -> int:
    possible_cubes_sum = 0
    with open(filename, 'r', encoding="utf-8") as file:
        lines = file.readlines()
        for line in lines:
            line = line.rstrip("\n")
            game, subsets = line.split(':')
            subsets = subsets.split(';')
            game_id = game.lstrip("Game ")
            # Single game
            cube_collection = {"red": [], "green": [], "blue": []}
            for subset in subsets:
                cubes = [cubes.strip().split(' ') for cubes in subset.split(',')]
                for num_cubes, cube_color in cubes:
                    cube_collection[cube_color].append(int(num_cubes))
            
            power = find_min_val_fo_cubes(cube_collection, debug)
            possible_cubes_sum += power

    return possible_cubes_sum


def main() -> None:
    test_one = False
    test_two = False

    possible_games_sum = all_elf_lies(EXAMPLE)
    if possible_games_sum == 8:
        print("PASSED TEST: EXAMPLE 1")
        test_one = True

    possible_games_sum = all_elf_lies_part_two(EXAMPLE)
    if possible_games_sum == 2286:
        print("PASSED TEST: EXAMPLE 2")
        test_two = True
    
    if test_one:
        input_possible_games_sum = all_elf_lies(INPUT)
        print(f"Sum of possible games of input for Part One: {input_possible_games_sum}")
    if test_two:
        input_possible_cubes_sum = all_elf_lies_part_two(INPUT)
        print(f"Sum of power of cubes of an input for Part Two: {input_possible_cubes_sum}")
    return


if __name__ == '__main__':
    main()
