import numpy as np

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
                worry_level *= worry_level

            # step 2
            worry_level = int(np.floor(worry_level/3))

            # step 3
            if worry_level % self.test_operand == 0:
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
for _ in range(20):

    for monkey in monkeys:
        throws = monkey.round()

        # process throws
        for throw in throws:
            monkeys[throw[0]].worry_levels.append(throw[1])

for monkeyid, monkey in enumerate(monkeys):
    print(monkeyid, monkey.inspections)



# too low - 50830 (230 * 221)