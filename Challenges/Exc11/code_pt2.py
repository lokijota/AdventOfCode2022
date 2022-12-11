import numpy as np
import sympy
from sympy.ntheory import primefactors
from mod import Mod
import math

# read all the lines
with open('Challenges\Exc11\input.txt') as f:
    lines = f.read().splitlines()


# Define useful classes
class Monkey:
    """ 
    O Macaco Gosta de Banana
    Todos os objectos em falta são portanto bananas 
    """

    def __init__(self):
        self.operation = "*"
        self.operand = 0
        self.test_operand = 1
        self.test_true_monkeyid = -1
        self.test_true_monkeyid = -1
        self.worry_levels = []
        self.inspections = 0
    
    def parse_monkey(self, line_iterator):
        row = next(line_iterator)
        row = [int(val) for val in row.replace("  Starting items: ", "").replace(" ","").split(",")]
        self.worry_levels = row

        row = next(line_iterator)
        row = row.replace("  Operation: new = old ", "").split(" ")
        self.operation = row[0]
        self.operand = row[1]
        if self.operand.isdigit():
            self.operand = int(self.operand)

        row = next(line_iterator)
        self.test_operand = int(row.replace("  Test: divisible by ", ""))

        row = next(line_iterator)
        self.test_true_monkeyid = int(row.replace("    If true: throw to monkey ", ""))

        row = next(line_iterator)
        self.test_false_monkeyid = int(row.replace("    If false: throw to monkey ", ""))

        return self

    def round(self):
        worry_transfers = []
        
        for worry_level in self.worry_levels:

            self.inspections += 1

            # step 1
            if type(self.operand) == int:
                if self.operation == "+":
                    worry_level += self.operand
                else:
                    worry_level *= self.operand
            else:
                worry_level = worry_level**2 # faster for large numbers https://stackoverflow.com/questions/72152748/time-it-takes-to-square-in-python

            # step 2
            # worry_level = int(np.floor(worry_level/3)) - removed on part 2

            # a = primefactors(worry_level)

            # if math.gcd(worry_level,self.test_operand) == self.test_operand:
            #     print("found for ", self.test_operand)

            # if worry_level % self.test_operand == 0:
            # if math.gcd(worry_level,self.test_operand) == self.test_operand:
            #     worry_transfers.append([self.test_true_monkeyid, worry_level])
            # else:
            #     worry_transfers.append([self.test_false_monkeyid, worry_level])

            # step 3
            if self.test_operand == 2 and worry_level & 1 == 0:
                worry_transfers.append([self.test_true_monkeyid, worry_level])
            elif worry_level % self.test_operand == 0:
                worry_transfers.append([self.test_true_monkeyid, worry_level])
            else:
                worry_transfers.append([self.test_false_monkeyid, worry_level])

        self.worry_levels = [] 
        return worry_transfers


# global variables
monkeys = np.empty(8, dtype = Monkey)

# read the monkey data
monkey_iterator = iter(lines)
monkey_data = next(monkey_iterator, None)
while monkey_data != None:
    
    # shouldn't happen -- but will help with skipping separators
    if not monkey_data.startswith("Monkey"):
        monkey_data = next(monkey_iterator, None)
        continue

    monkey_nr = int(monkey_data.split(" ")[1][:-1])
    monkeys[monkey_nr] = Monkey().parse_monkey(monkey_iterator)

    monkey_data = next(monkey_iterator, None)

# Now, implement the behaviour
throws_count_per_round = np.empty(8, dtype = list)
current_monkey = 0
throws_count_per_round[0] = []
throws_count_per_round[1] = []
throws_count_per_round[2] = []
throws_count_per_round[3] = []
throws_count_per_round[4] = []
throws_count_per_round[5] = []
throws_count_per_round[6] = []
throws_count_per_round[7] = []

for _ in range(110): #10000

    print(".", end = '')

    for monkey in monkeys:
        throws = monkey.round()

        throws_count_per_round[current_monkey].append(monkey.inspections)
        current_monkey += 1

        # process throws
        for throw in throws:
            monkeys[throw[0]].worry_levels.append(throw[1])
            # print(thclsrow[1])

    current_monkey = 0

for monkeyid, monkey in enumerate(monkeys):
    print(monkey.inspections) #monkeyid, 

# print(throws_count_per_round)



# Identify regularities in deltas -- for 2 and 7 they happen - 36 movements every 3 rounds starting around 30 (*3) = 60
# round 
# step = 1
# max_step = 10
# start_position = 0

# fixed_values = []
# for pos in range(1,90):
#     fixed_values.append(throws_count_per_round[2][pos] - throws_count_per_round[2][pos-1])

# throws_count_per_round[2] = fixed_values

# for step in range(3, max_step):

#     print("***** testing step", step)
#     for pos in range(start_position, 90, step):
#         the_sum = sum(throws_count_per_round[2][pos:pos+step])
#         print(the_sum, end=",")
#         the_sum = 0
    
#     print()
