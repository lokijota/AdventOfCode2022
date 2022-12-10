# read all the lines
with open('Challenges\Exc7\input.txt') as f:
    lines = f.readlines()

# [full_path, size]

filesystem_dict = { "/": 0 }

current_folder = ""
current_full_path = ""

for command in lines:

    # cd command
    
    if command.startswith("$ cd"):
        new_folder = command[5:-1]
        
        if new_folder == "..":

            pos_last_folder = current_full_path.rfind('/')
            current_full_path = current_full_path[:pos_last_folder]
            
            pos_last_folder = current_full_path.rfind('/')
            current_folder = current_full_path[pos_last_folder-1:] 
        elif new_folder == "/":
            current_folder = "/"
            current_full_path = "/"
        else:
            current_folder = new_folder
            current_full_path = current_full_path + "/" + new_folder 
            current_full_path = current_full_path.replace("//", "/") # fix to root special case
        continue

    # # ls command
    # if command.startswith("$ ls"):
    #     continue
    
    if command.startswith("dir "):
        if current_full_path == "/":
            filesystem_dict["/" + command[4:-1]] = 0
        else:
            filesystem_dict[current_full_path + "/" + command[4:-1]] = 0
        continue

    if command[0].isdigit(): #found a file
        parts = command.split(" ")
        filesystem_dict[current_full_path] = filesystem_dict[current_full_path] + int(parts[0])
        # add the size of the file, but just on the current folder
        continue

# little recursive function to add up
def add_sizes_folders_above(folder_to_add, size_to_add):

    if len(folder_to_add) > 1 and folder_to_add[-1] == "/":
        folder_to_add = folder_to_add[:-1]

    filesystem_dict[folder_to_add] += size_to_add

    if folder_to_add == "/": #we got to the root / end recursion
        return
    else:
        folder_above = folder_to_add[0:folder_to_add.rfind("/") ]
        if folder_above == "":
            folder_above = "/"
        add_sizes_folders_above(folder_above, size_to_add) #filesystem_dict[folder_to_add] - this was a bug... i was just making up used space

    return

# trigger "backpropagation" of folder sizes
for folder, folder_size in filesystem_dict.items():
    # print("-", folder, folder_size)
    if folder != "/":
        add_sizes_folders_above(folder[:folder.rfind("/")+1], folder_size)


total_size = 0
smallest_folder_to_free_30000000 = 90000000
free_space = 70000000 - filesystem_dict["/"]

for k, v in filesystem_dict.items():
    if v <= 100000:
        total_size += v

    if free_space + v > 30000000 and v < smallest_folder_to_free_30000000:
        smallest_folder_to_free_30000000 = v 

print("Grand total:", total_size)
print("Free space:", free_space)
print("Size of folder to delete:", smallest_folder_to_free_30000000)

# the total is correct, 95437, for the sample
# 1886043 for part 1
# 3842121 for part 2
# truque: há pastas com o mesmo nome em sítios diferentes da hierarquia


