"""Advent of code Day 4

The gondola takes you up. Strangely, though, the ground doesn't seem to be coming with you; 
you're not climbing a mountain. As the circle of Snow Island recedes below you, 
an entire new landmass suddenly appears above you! 
The gondola carries you to the surface of the new island and lurches into the station.

As you exit the gondola, the first thing you notice is that the air here is much warmer than it was on Snow Island. 
It's also quite humid. Is this where the water source is?

The next thing you notice is an Elf sitting on the floor across the station in what seems to be a pile of colorful square cards.

"Oh! Hello!" The Elf excitedly runs over to you. 
"How may I be of service?" You ask about water sources.

"I'm not sure; I just operate the gondola lift. 
That does sound like something we'd have, though - this is Island Island, after all! I bet the gardener would know. 
He's on a different island, though - er, the small kind surrounded by water, not the floating kind. 
We really need to come up with a better naming scheme. Tell you what: if you can help me with something quick, 
I'll let you borrow my boat and you can go visit the gardener. 
I got all these scratchcards as a gift, but I can't figure out what I've won."

The Elf leads you over to the pile of colorful cards. There, you discover dozens of scratchcards, 
all with their opaque covering already scratched off. Picking one up, it looks like each card has two lists of numbers 
separated by a vertical bar (|): a list of winning numbers and then a list of numbers you have. 
You organize the information into a table (your puzzle input).

As far as the Elf has been able to figure out, you have to figure out which of the numbers you have appear in the list of winning numbers. 
The first match makes the card worth one point and each match after the first doubles the point value of that card.

--- Part Two ---
Just as you're about to report your findings to the Elf, one of you realizes that 
the rules have actually been printed on the back of every card this whole time.

There's no such thing as "points". Instead, scratchcards only cause you to 
win more scratchcards equal to the number of winning numbers you have.

Specifically, you win copies of the scratchcards below the winning card equal to the number of matches. 
So, if card 10 were to have 5 matching numbers, you would win one copy each of cards 11, 12, 13, 14, and 15.

Copies of scratchcards are scored like normal scratchcards and have the same card number as the card they copied. 
So, if you win a copy of card 10 and it has 5 matching numbers, 
it would then win a copy of the same cards that the original card 10 won: cards 11, 12, 13, 14, and 15. 
This process repeats until none of the copies cause you to win any more cards. 
(Cards will never make you copy a card past the end of the table.)
"""

import re

EXAMPLE_1 = "./example_1.txt"

INPUT = "./input.txt"


def preprocess_input(line: str) -> tuple[int, list, list]:
    line = line.strip()
    card_id, cards = line.split(':')
    card_id = int(card_id.lstrip('Card '))
    winning_numbers, my_numbers = cards.split('|')
    winning_numbers = list(map(int, re.findall(r"(\d+)", winning_numbers)))
    my_numbers = list(map(int, re.findall(r"(\d+)", my_numbers)))
    return card_id, winning_numbers, my_numbers


def how_many_points(filename: str) -> int:
    sum_of_points = 0
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        for line in lines:
            points = 0
            card_id, winning_numbers, my_numbers = preprocess_input(line)
            for num in my_numbers:
                if num in winning_numbers:
                    if points == 0:
                        points = 1
                    else:
                        points *= 2
            sum_of_points += points
    return sum_of_points


def how_many_scratchcards(filename: str) -> int:
    card_quantities = {}
    last_card_id = 0
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        for line in lines:
            card_id, winning_numbers, my_numbers = preprocess_input(line)
            last_card_id = card_id
            if card_id not in list(card_quantities.keys()):
                card_quantities[card_id] = 1
            else:
                card_quantities[card_id] += 1
            for i in range(card_quantities[card_id]):
                new_card_id = card_id + 1
                for num in my_numbers:
                    if num in winning_numbers:
                        if new_card_id not in list(card_quantities.keys()):
                            card_quantities[new_card_id] = 1
                        else:
                            card_quantities[new_card_id] += 1
                        new_card_id += 1
    return sum([val for key, val in card_quantities.items() if key <= last_card_id])



def main() -> None:
    test_one = False
    test_two = False

    example_points = how_many_points(EXAMPLE_1)
    if example_points == 13:
        print("PASSED TEST: EXAMPLE 1")
        test_one = True

    example_num_cards = how_many_scratchcards(EXAMPLE_1)
    if example_num_cards == 30:
        print("PASSED TEST: EXAMPLE 2")
        test_two = True

    if test_one:
        input_points = how_many_points(INPUT)
        print(f"Sum of all points from scratchcards for Part One: {input_points}")
    if test_two:
        input_gear_ratio = how_many_scratchcards(INPUT)
        print(f"Sum of all scratchcards for Part Two: {input_gear_ratio}")
    
    return


if __name__ == '__main__':
    main()
