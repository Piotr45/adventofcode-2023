"""Advent of code Day 19

The Elves of Gear Island are thankful for your help and send you on your way. 
They even have a hang glider that someone stole from Desert Island; since you're already going that direction, 
it would help them a lot if you would use it to get down there and return it to them.

As you reach the bottom of the relentless avalanche of machine parts, 
you discover that they're already forming a formidable heap. 
Don't worry, though - a group of Elves is already here organizing the parts, and they have a system.

--- Part Two ---

Even with your help, the sorting process still isn't fast enough.

One of the Elves comes up with a new plan: rather than sort parts individually through all of these workflows, 
maybe you can figure out in advance which combinations of ratings will be accepted or rejected.
"""

import re

EXAMPLE = "./example.txt"
INPUT = "./input.txt"


def process_input(lines: list) -> tuple:
    splitter = lines.index("")
    workflows, parts = lines[:splitter], lines[splitter + 1 :]
    # cast workflows to dict
    workflows = {
        workflow.split("{")[0]: workflow.split("{")[1].strip("}").split(",")
        for workflow in workflows
    }
    # cast parts to list of dicts
    parts = [
        {p.split("=")[0]: int(p.split("=")[1]) for p in part.strip("{}").split(",")}
        for part in parts
    ]
    return workflows, parts


def apply_rule(rule: str, part: dict) -> str:
    if rule in "AR":
        return rule
    if "<" not in rule and ">" not in rule:
        return rule

    category, new_rule = re.findall("[a-zA-Z]+", rule)
    value = int(re.findall("\d+", rule)[0])
    sign = re.findall("[<>]", rule)[0]

    if sign == "<":
        if part[category] < value:
            return new_rule
    elif sign == ">":
        if part[category] > value:
            return new_rule
    return -1


def process_part(
    part: dict,
    workflows: list,
) -> int:
    current_workflow = workflows["in"]
    decision = None

    while decision is None:
        for rule in current_workflow:
            nxt = apply_rule(rule, part)
            if nxt == -1:
                continue
            if nxt == "A":
                decision = "A"
                break
            if nxt == "R":
                decision = "R"
                break
            current_workflow = workflows[nxt]
            break

    if decision == "A":
        return sum(part.values())
    return 0


def process_workflow(curr_workflow: str, workflow_chain: list) -> None:
    global workflows, workflow_chains
    if curr_workflow == "A":
        workflow_chains.append(workflow_chain)
    elif curr_workflow != "R":
        rules = []
        for rule in workflows[curr_workflow][:-1]:
            if rule not in "AR":
                next_workflow = rule.split(":")[1]
                process_workflow(
                    next_workflow, workflow_chain + rules + [rule.split(":")[0]]
                )
                if rule[1] == "<":
                    category = re.findall("[a-zA-Z]+", rule)[0]
                    value = int(re.findall("\d+", rule)[0])
                    rules.append(f"{category}>{value-1}")
                elif rule[1] == ">":
                    category = re.findall("[a-zA-Z]+", rule)[0]
                    value = int(re.findall("\d+", rule)[0])
                    rules.append(f"{category}<{value+1}")
        else:
            next_workflow = workflows[curr_workflow][-1]
            process_workflow(next_workflow, workflow_chain + rules)


def calc_combos(constrains: list) -> int:
    categories = {"x": [1, 4000], "m": [1, 4000], "a": [1, 4000], "s": [1, 4000]}
    for constrain in constrains:
        category = re.findall("[a-zA-Z]+", constrain)[0]
        value = int(re.findall("\d+", constrain)[0])
        sign = re.findall("[<>]", constrain)[0]
        if sign == "<" and categories[category][1] > value:
            categories[category][1] = value - 1
        if sign == ">" and categories[category][0] < value:
            categories[category][0] = value + 1
    res = 1
    for x in [_max - _min + 1 for (_min, _max) in categories.values()]:
        res *= x
    return res


def calc_sum_of_accepted_workflows(filename: str, part2: bool = False) -> int:
    global workflows, workflow_chains
    with open(filename, "r", encoding="utf-8") as file:
        workflows, parts = process_input([line.strip() for line in file.readlines()])
        if part2:
            workflow_chains = []
            process_workflow("in", [])
            return sum(
                [calc_combos(workflow_chain) for workflow_chain in workflow_chains]
            )
        else:
            return sum([process_part(part, workflows) for part in parts])


def main() -> None:
    test_one = False
    test_two = False

    if calc_sum_of_accepted_workflows(EXAMPLE) == 19114:
        print("PASSED TEST: EXAMPLE 1")
        test_one = True
    if calc_sum_of_accepted_workflows(EXAMPLE, part2=True) == 167409079868000:
        print("PASSED TEST: EXAMPLE 2")
        test_two = True

    if test_one:
        print(
            f"Sum of all of the rating numbers for all of the parts that ultimately get accepted for Part One: {calc_sum_of_accepted_workflows(INPUT)}"
        )

    if test_two:
        print(
            f"How many distinct combinations of ratings will be accepted by the Elves' workflows?: {calc_sum_of_accepted_workflows(INPUT, part2=True)}"
        )
    return


if __name__ == "__main__":
    main()
