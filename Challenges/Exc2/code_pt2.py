# read all the lines
with open('Challenges\Exc2\input.txt') as f:
    lines = f.readlines()

# replace the letters with R(ock) P(aper) S(cisors) just to be obvious to me
fixed_plays = [row.replace('A', 'R').replace('B', 'P').replace('C', 'S').replace('X', 'L').replace('Y', 'D').replace('Z', 'W') for row in lines]

def score(play_a, play_b):
    score_a = 0
    score_b = 0

    if play_a == 'R':
        score_a = 1
    if play_b == 'R':
        score_b = 1

    if play_a == 'P':
        score_a = 2
    if play_b == 'P':
        score_b = 2

    if play_a == 'S':
        score_a = 3
    if play_b == 'S':
        score_b = 3

    if  play_a == play_b:
        score_a += 3
        score_b += 3
    elif (play_a == 'R' and play_b == "S") or (play_a == 'S' and play_b == "P") or (play_a == 'P' and play_b == "R"):
        score_a += 6
    else:
        score_b += 6

    return (score_a, score_b)

def what_to_play(play_a, outcome):
    # Rock defeats Scissors, Scissors defeats Paper, and Paper defeats Rock. 

    config = {
        "RD": "R",
        "PD": "P",
        "SD": "S",
        "RW": "P",
        "PW": "S",
        "SW": "R",
        "RL": "S",
        "PL": "R",
        "SL": "P",
    }

    return config[play_a + outcome]

total_score_a = 0
total_score_b = 0
rows = 0

for play in fixed_plays:
    round_score = score(play[0], what_to_play(play[0], play[2]))
    total_score_a += round_score[0]
    total_score_b += round_score[1]
    rows += 1

print("total score a:", total_score_a, "vs total_score_b:", total_score_b, ", rows:", rows)

