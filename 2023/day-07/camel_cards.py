"""Advent of code Day 7

Your all-expenses-paid trip turns out to be a one-way, five-minute ride in an airship. 
(At least it's a cool airship!) It drops you off at the edge of a vast desert and descends back to Island Island.

"Did you bring the parts?"

You turn around to see an Elf completely covered in white clothing, wearing goggles, and riding a large camel.

"Did you bring the parts?" she asks again, louder this time. 
You aren't sure what parts she's looking for; you're here to figure out why the sand stopped.

"The parts! For the sand, yes! Come with me; I will show you." She beckons you onto the camel.

After riding a bit across the sands of Desert Island, you can see what look like very large rocks covering half of the horizon. 
The Elf explains that the rocks are all along the part of Desert Island that is directly above Island Island, 
making it hard to even get there. Normally, they use big machines to move the rocks and filter the sand, 
but the machines have broken down because Desert Island recently stopped receiving the parts they need to fix the machines.

You've already assumed it'll be your job to figure out why the parts stopped when she asks if you can help. 
You agree automatically.

Because the journey will take a few days, she offers to teach you the game of Camel Cards. 
Camel Cards is sort of similar to poker except it's designed to be easier to play while riding a camel.

In Camel Cards, you get a list of hands, and your goal is to order them based on the strength of each hand. 
A hand consists of five cards labeled one of A, K, Q, J, T, 9, 8, 7, 6, 5, 4, 3, or 2. 
The relative strength of each card follows this order, where A is the highest and 2 is the lowest.

Every hand is exactly one type. From strongest to weakest, they are:

Five of a kind, where all five cards have the same label: AAAAA
Four of a kind, where four cards have the same label and one card has a different label: AA8AA
Full house, where three cards have the same label, and the remaining two cards share a different label: 23332
Three of a kind, where three cards have the same label, and the remaining two cards are each different from any other card in the hand: TTT98
Two pair, where two cards share one label, two other cards share a second label, and the remaining card has a third label: 23432
One pair, where two cards share one label, and the other three cards have a different label from the pair and each other: A23A4
High card, where all cards' labels are distinct: 23456
Hands are primarily ordered based on type; for example, every full house is stronger than any three of a kind.

If two hands have the same type, a second ordering rule takes effect. Start by comparing the first card in each hand. If these cards are different, the hand with the stronger first card is considered stronger. If the first card in each hand have the same label, however, then move on to considering the second card in each hand. If they differ, the hand with the higher second card wins; otherwise, continue with the third card in each hand, then the fourth, then the fifth.

So, 33332 and 2AAAA are both four of a kind hands, but 33332 is stronger because its first card is stronger. Similarly, 77888 and 77788 are both a full house, but 77888 is stronger because its third card is stronger (and both hands have the same first and second card).

Find the rank of every hand in your set. What are the total winnings?

--- Part Two ---

To make things a little more interesting, the Elf introduces one additional rule. Now, 
J cards are jokers - wildcards that can act like whatever card would make the hand the strongest type possible.

To balance this, J cards are now the weakest individual cards, weaker even than 2. 
The other cards stay in the same order: A, K, Q, T, 9, 8, 7, 6, 5, 4, 3, 2, J.

J cards can pretend to be whatever card is best for the purpose of determining hand type; for example, 
QJJQ2 is now considered four of a kind. However, for the purpose of breaking ties between two hands of the same type, 
J is always treated as J, not the card it's pretending to be: JKKK2 is weaker than QQQQ2 because J is weaker than Q.

Using the new joker rule, find the rank of every hand in your set. What are the new total winnings?
"""

EXAMPLE = "./example.txt"

INPUT = "./input.txt"


def get_strength_of_hand(hand: str) -> tuple:
    card_counts = [hand.count(card) for card in set(hand)]
    if 5 in card_counts:
        return 6  # Five of a kind
    if 4 in card_counts:
        return 5  # Four of a kind
    if 3 in card_counts:
        if 2 in card_counts:
            return 4  # Full House
        else:
            return 3  # Three of a kind
    if card_counts.count(2) == 2:
        return 2  # Two pair
    if card_counts.count(2) == 1:
        return 1  # One pair
    return 0  # High card


def get_possible_hand(hand: str, hand_strength: int) -> tuple[str, int]:
    best_hand = hand
    best_strength = hand_strength
    for card in "23456789TQKA":
        possible_hand = hand
        possible_strength = get_strength_of_hand(possible_hand.replace("J", card))
        if possible_strength > best_strength:
            best_strength = possible_strength
            best_hand = possible_hand
    return best_hand, best_strength


def total_winnings(filename: str, debug: bool = False) -> int:
    ranking = []
    with open(filename, "r", encoding="utf-8") as file:
        lines = file.readlines()
        for line in lines:
            hand, bid = line.strip().split(" ")
            hand_strength = get_strength_of_hand(hand.strip())
            cards_strengths = ["23456789TJQKA".index(card) for card in hand]
            ranking.append((cards_strengths, hand_strength, int(bid)))

        ranking = sorted(ranking, key=lambda x: (x[1], x[0]))

        return sum((i + 1) * rank[-1] for i, rank in enumerate(ranking))


def total_winnings_part_two(filename: str, debug: bool = False) -> int:
    ranking = []
    with open(filename, "r", encoding="utf-8") as file:
        lines = file.readlines()
        for line in lines:
            hand, bid = line.strip().split(" ")
            hand_strength = get_strength_of_hand(hand.strip())
            if "J" in hand:
                hand, hand_strength = get_possible_hand(hand, hand_strength)
            cards_strengths = ["J23456789TQKA".index(card) for card in hand]
            ranking.append((cards_strengths, hand_strength, int(bid)))

        ranking = sorted(ranking, key=lambda x: (x[1], x[0]))

        return sum((i + 1) * rank[-1] for i, rank in enumerate(ranking))


def main() -> None:
    test_one = False
    test_two = False

    example_total_winnings = total_winnings(EXAMPLE)
    if example_total_winnings == 6440:
        print("PASSED TEST: EXAMPLE 1")
        test_one = True

    example_total_winnings = total_winnings_part_two(EXAMPLE)
    if example_total_winnings == 5905:
        print("PASSED TEST: EXAMPLE 2")
        test_two = True

    if test_one:
        input_total_winnings = total_winnings(INPUT)
        print(f"Total winnings for Part One: {input_total_winnings}")
    if test_two:
        input_total_winnings = total_winnings_part_two(INPUT)
        print(f"Total winnings for Part Two: {input_total_winnings}")

    return


if __name__ == "__main__":
    main()
