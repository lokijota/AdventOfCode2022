# read all the lines
with open('Challenges\Exc3\input.txt') as f:
    lines = f.readlines()

# para cada string, obter a lista de caracteres que estão na primeira metade e que estáo também na segunda metade
# newlist = [x for x in fruits if "a" in x]

# Lowercase item types a through z have priorities 1 through 26.
# Uppercase item types A through Z have priorities 27 through 52.

def calculate_priorities(outliers):
    lowercase = [ord(x) - ord("a") + 1 for x in outliers if x >= "a" and x <= 'z']
    uppercase = [ord(x) - ord("A") + 27 for x in outliers if x >= "A" and x <= 'Z']

    return sum(lowercase) + sum(uppercase)

outliers = []

for line in lines:
    # print(line[:int(len(line)/2)])
    # print(line[int(len(line)/2):])
    for p1char in line[:int(len(line)/2)]:
        if p1char in line[int(len(line)/2):]:
            outliers.append(p1char)
            break

print(len(outliers))
print(calculate_priorities(outliers))

# 8018