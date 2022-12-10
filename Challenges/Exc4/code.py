# read all the lines
with open('Challenges\Exc4\input.txt') as f:
    lines = f.readlines()

def contained(set1_start, set1_end, set2_start, set2_end):
    if set1_start <= set2_start and set1_end >= set2_end:
        return True

    if set1_start >= set2_start and set1_end <= set2_end:
        return True

    return False


def overlap(set1_start, set1_end, set2_start, set2_end):
    
    if(contained(set1_start, set1_end, set2_start, set2_end)):
        return True

    if set1_start >= set2_start and set1_start <= set2_end:
        return True

    if set1_end >= set2_start and set1_end <= set2_end:
        return True

    return False


contained_sum = 0
overlap_sum = 0

for line in lines:
    parts = line.split(",")
    left_split = parts[0].split("-")
    right_split = parts[1].split("-")

    start_elf_1 = int(left_split[0])
    end_elf_1 = int(left_split[1])

    start_elf_2 = int(right_split[0])
    end_elf_2 = int(right_split[1])

    if contained(start_elf_1, end_elf_1, start_elf_2, end_elf_2):
        contained_sum+=1

    if overlap(start_elf_1, end_elf_1, start_elf_2, end_elf_2):
        overlap_sum += 1


print(contained_sum, overlap_sum)

# 431
# 823