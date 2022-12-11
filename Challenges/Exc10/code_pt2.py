import numpy as np
from numpy.linalg import norm

# read all the lines
with open('Challenges\Exc10\input.txt') as f:
    lines = f.read().splitlines()

crt = np.empty(280, dtype=str)

clock_tick = 0
clock_is_ticking = True
commands = iter(lines) #next(lst)
is_command_executing = False
remaining_ticks = 0
X = 1

next_cycle_to_capture = 20
signal_strength = 0

while clock_is_ticking:
    
    

    # run instructions
    if clock_tick == next_cycle_to_capture:
        signal_strength += X * next_cycle_to_capture
        print(X * next_cycle_to_capture, X)
        next_cycle_to_capture += 40

        if next_cycle_to_capture > 220:
            next_cycle_to_capture = 9999999999999

    if remaining_ticks > 0:
        remaining_ticks -= 1
    
    if remaining_ticks == 0 and is_command_executing == True:
        if command.startswith("addx"):
            X += int(command.split(" ")[1])
        is_command_executing = False

    if not is_command_executing:
        command = next(commands, None)
        if command is None:
            break # end execution

        if command == "noop":
            remaining_ticks = 1
        else:
            remaining_ticks = 2

        is_command_executing = True

    
    # sprite location
    start_sprite = X-1
    end_sprite = X+1

    if clock_tick%40 >= start_sprite and clock_tick%40 <= end_sprite:
        crt[clock_tick] = "#"
    else:
        crt[clock_tick] = " "
    

    clock_tick += 1

print("signal strength:", signal_strength, ", X:", X)
print("# clock ticks:", clock_tick)

crt = crt.reshape((7,40))
print(crt)