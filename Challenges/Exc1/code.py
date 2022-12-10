with open('Challenges\Exc1\input.txt') as f:
    lines = f.readlines()

elf_total_load = []

current_sum = 0
current_max = 0

for line in lines:
    if line == '\n':
        elf_total_load.append(current_sum)

        if current_max < current_sum:
            current_max = current_sum
        
        current_sum = 0
    else:
        current_sum += int(line)

elf_total_load.sort(reverse=True)

print("max: ", current_max)
print("max 3: ", sum(elf_total_load[:3]))
