# read all the lines
with open('Challenges\Exc5\input.txt') as f:
    lines = f.readlines()

crate_initial_positions = lines[:8]
crate_moves = lines[10:]

# read the initial structure
crate_config  = [ [], [],  [], [],  [], [],  [], [],  [] ]

for idx, row in enumerate(crate_initial_positions):
    if row[1] != " ":
        crate_config[0].append(row[1])

    if row[5] != " ":
        crate_config[1].append(row[5])

    if row[9] != " ":
        crate_config[2].append(row[9])

    if row[13] != " ":
        crate_config[3].append(row[13])

    if row[17] != " ":
        crate_config[4].append(row[17])

    if row[21] != " ":
        crate_config[5].append(row[21])

    if row[25] != " ":
        crate_config[6].append(row[25])

    if row[29] != " ":
        crate_config[7].append(row[29])

    if row[33] != " ":
        crate_config[8].append(row[33])

# function to do a movement
def move(how_many, from_column, to_column):
    block_to_move = crate_config[from_column-1][:how_many]
    del crate_config[from_column-1][0:how_many]
    # block_to_move.reverse() -- comment this for part 2

    crate_config[to_column-1] = block_to_move + crate_config[to_column-1]

# now parse the movements

for crete_move in crate_moves:
    parts = crete_move.split(" ")
    move(int(parts[1]), int(parts[3]), int(parts[5]))
    print(".")

solution = ""
for column in crate_config:
    solution = solution + column[0]

print(solution)

# part 1 - SPFMVDTZT
# part 2 - ZFSJBPRFP