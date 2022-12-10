# read all the lines
with open('Challenges\Exc3\input.txt') as f:
    lines = f.readlines()

# para cada string, obter a lista de caracteres que estão na primeira metade e que estáo também na segunda metade

# Lowercase item types a through z have priorities 1 through 26.
# Uppercase item types A through Z have priorities 27 through 52.

def calculate_priorities(outliers):
    lowercase = [ord(x) - ord("a") + 1 for x in outliers if x >= "a" and x <= 'z']
    uppercase = [ord(x) - ord("A") + 27 for x in outliers if x >= "A" and x <= 'Z']

    return sum(lowercase) + sum(uppercase)

outliers = []

for idx, line in enumerate(lines[::3]):
    for p1char in line:
        if p1char in lines[idx*3+1] and p1char in lines[idx*3+2]:
            outliers.append(p1char)
            break

print(len(outliers))
print(calculate_priorities(outliers))

# 2518
# another simpler approach would have been to use sets https://www.w3schools.com/python/python_sets.asp
