"""Advent of code Day 20

With your help, the Elves manage to find the right parts and fix all of the machines. 
Now, they just need to send the command to boot up the machines and get the sand flowing again.

The machines are far apart and wired together with long cables. 
The cables don't connect to the machines directly, 
but rather to communication modules attached to the machines that perform 
various initialization tasks and also act as communication relays.

Modules communicate using pulses. Each pulse is either a high pulse or a low pulse. 
When a module sends a pulse, it sends that type of pulse to each module in its list of destination modules.

--- Part Two ---

The final machine responsible for moving the sand down to Island Island has a module attached named rx. 
The machine turns on when a single low pulse is sent to rx.

Reset all modules to their default states. 
Waiting for all pulses to be fully handled after each button press, 
what is the fewest number of button presses required to deliver a single low pulse to the module named rx?
"""

from math import lcm

EXAMPLE_1 = "./example_1.txt"
EXAMPLE_2 = "./example_2.txt"
INPUT = "./input.txt"


def process_input(lines: list) -> dict:
    modules = {}
    conjunction_modules = []
    for line in lines:
        module, destination = [l.strip() for l in line.split("->")]
        destination = {d.strip() for d in destination.split(",")}
        if module == "broadcaster":
            modules[module] = [None, destination]
        else:
            mtype, module_name = module[0], module[1:]
            if mtype == "%":
                modules[module_name] = [False, mtype, destination]
            if mtype == "&":
                conjunction_modules.append(module_name)
                modules[module_name] = [{}, mtype, destination]

    for module, data in modules.items():
        if module == "broadcaster":
            mtype, dest = data
        else:
            _input, mtype, dest = data

        for cm in conjunction_modules:
            if cm in dest:
                modules[cm][0][module] = False

    return modules


def send_pulses(n: int = 1000) -> int:
    global modules
    low_pulses, high_pulses = 0, 0
    for i in range(n):
        processing = [(None, "broadcaster", False)]
        while processing:
            new_processes = []
            for prev_module, module, pulse in processing:
                # print(prev_module, module, pulse)
                if pulse == False:
                    low_pulses += 1
                else:
                    high_pulses += 1

                if module not in modules.keys():
                    continue
                # flip-flop
                if modules[module][1] == "%":
                    if pulse == True:
                        continue
                    modules[module][0] = not modules[module][0]
                    for dst in modules[module][-1]:
                        new_processes.append((module, dst, modules[module][0]))
                # conjunction
                elif modules[module][1] == "&":
                    modules[module][0][prev_module] = pulse
                    input_states = modules[module][0]

                    if sum(input_states.values()) == len(input_states):
                        output_pulse = False
                    else:
                        output_pulse = True

                    for dst in modules[module][-1]:
                        new_processes.append((module, dst, output_pulse))
                # broadcaster
                elif prev_module is None:
                    for dst in modules[module][-1]:
                        new_processes.append((module, dst, pulse))
            processing = new_processes
    return low_pulses * high_pulses


def send_pulses_part_two(
    n: int = 1000, lcm_modules: list = ["bg", "ls", "qq", "sj"]
) -> int:
    global modules
    lcm_conjunctions = {}

    for i in range(n):
        processing = [(None, "broadcaster", False)]
        while processing:
            new_processes = []
            for prev_module, module, pulse in processing:
                if module not in modules.keys():
                    continue
                # flip-flop
                if modules[module][1] == "%":
                    if pulse == True:
                        continue
                    modules[module][0] = not modules[module][0]
                    for dst in modules[module][-1]:
                        new_processes.append((module, dst, modules[module][0]))
                # conjunction
                elif modules[module][1] == "&":
                    modules[module][0][prev_module] = pulse
                    input_states = modules[module][0]

                    if sum(input_states.values()) == len(input_states):
                        output_pulse = False
                    else:
                        output_pulse = True

                    if module in lcm_modules and output_pulse == True:
                        if module not in lcm_conjunctions.keys():
                            lcm_conjunctions[module] = i + 1

                    for dst in modules[module][-1]:
                        new_processes.append((module, dst, output_pulse))
                # broadcaster
                elif prev_module is None:
                    for dst in modules[module][-1]:
                        new_processes.append((module, dst, pulse))
            processing = new_processes
    return lcm(*list(lcm_conjunctions.values()))


def total_pulses(filename: str, part2: bool = False) -> int:
    global modules
    with open(filename, "r", encoding="utf-8") as file:
        lines = [line.strip() for line in file.readlines()]
        if part2:
            modules = process_input(lines)
            return send_pulses_part_two(10000)
        else:
            modules = process_input(lines)
            return send_pulses()


def main() -> None:
    test_one = False
    test_two = True

    if total_pulses(EXAMPLE_1) == 32000000 and total_pulses(EXAMPLE_2) == 11687500:
        print("PASSED TEST: EXAMPLE 1")
        test_one = True

    if test_one:
        print(
            f"Value of multiply the total number of low pulses sent by the total number of high pulses sent for Part One: {total_pulses(INPUT)}"
        )

    if test_two:
        print(
            f"The fewest number of button presses required to deliver a single low pulse to the module named rx?: {total_pulses(INPUT, part2=True)}"
        )
    return


if __name__ == "__main__":
    main()
