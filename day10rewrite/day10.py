from math import ceil
import sys
sys.setrecursionlimit(10000)

def printfile(file):
    for i in file:
        print(''.join(i))

def floodfill(array, coord):
    xpos = coord[0]
    ypos = coord[1]
    if array[xpos][ypos] == "X" or array[xpos][ypos] == "I":
        #        printfile(array)
        return array
    possnewcoords = []
    [[possnewcoords.append([x, y]) for y in range(ypos - 1, ypos + 2)] for x in range(xpos - 1, xpos + 2)]
    array[xpos][ypos] = "I"
    for i in possnewcoords:
        #        print(i)
        if not (0 <= i[0] < len(array)):
            continue
        if not (0 <= i[1] < len(array[0])):
            continue
        array = floodfill(array, i)
    return array

f = open('input.txt', 'r')
file = [list(x) for x in f.read().strip().split()]
#file = 
"""

S------7
L----7.|
F--7.|.|
|..L-J.|
L------J

""".strip().split()


file = [['.'] + list(x) +['.'] for x in file]
file.append(['.'] * len(file[0]))
file = [['.'] * len(file[0])] + file
start_coord = []
end = False
for i in enumerate(file):
    for j in enumerate(i[1]):
        if j[1] == "S":
            start_coord = [i[0], j[0]]
            end = True
            break
    if end:
        break

left_enter_pipes = ["F", "-", "L"]
right_exit_pipes = ["J", "-", "7"]
bottom_enter_pipes = ["|", "J", "L"]
top_exit_pipes = ["|", "F", "7"]

up_char_io = file[start_coord[0] - 1][start_coord[1]] in top_exit_pipes
down_char_io = file[start_coord[0] + 1][start_coord[1]] in bottom_enter_pipes
left_char_io = file[start_coord[0]][start_coord[1] - 1] in left_enter_pipes
right_char_io = file[start_coord[0]][start_coord[1] + 1] in right_exit_pipes

start_char_possibilites = []

left_to_right_mapping = {"-":[0, 1],
                         "J":[-1, 0],
                         "7":[1, 0]}
right_to_left_mapping = {"-":[0, -1],
                         "F":[1, 0],
                         "L":[-1, 0]}
top_to_bottom_mapping = {"|":[1, 0],
                         "J":[0, -1],
                         "L":[0, 1]}
bottom_to_top_mapping = {"|":[-1, 0],
                         "7":[0, -1],
                         "F":[0, 1]}

if up_char_io and down_char_io:
    start_char_possibilites.append(["|", [start_coord[0] - 1, start_coord[1]]])
if up_char_io and left_char_io:
    start_char_possibilites.append(["J", [start_coord[0] - 1, start_coord[1]]])
if up_char_io and right_char_io:
    start_char_possibilites.append(["L", [start_coord[0], start_coord[1] + 1]])
if down_char_io and left_char_io:
    start_char_possibilites.append(["7", [start_coord[0] + 1, start_coord[1]]])
if down_char_io and right_char_io:
    start_char_possibilites.append(["F", [start_coord[0], start_coord[1] + 1]])
if left_char_io and right_char_io:
    start_char_possibilites.append(["-", [start_coord[0], start_coord[1] + 1]])

output = []
outfile = []
outheading = []

for i in start_char_possibilites:
    file_copy = file
    locations = [start_coord]
    cur_coord = i[1]
    headings = []
    prev_coord = start_coord
    while True:
        currchar = file_copy[cur_coord[0]][cur_coord[1]]
        file_copy[cur_coord[0]][cur_coord[1]] = "X"
        if cur_coord in locations:
            break
        dictionary = {}
        match [prev_coord[0] - cur_coord[0], prev_coord[1] - cur_coord[1]]:
            case [-1, 0]:
                dictionary = top_to_bottom_mapping
                heading = "down"
            case [1, 0]:
                dictionary = bottom_to_top_mapping
                heading = "up"
            case [0, 1]:
                dictionary = right_to_left_mapping
                heading = "left"
            case [0, -1]:
                dictionary = left_to_right_mapping
                heading = "right"
            case _:
                break
        try:
            loc = dictionary[currchar]
        except KeyError:
            break
        locations.append(cur_coord)
        headings.append(heading)
        prev_coord = cur_coord
        cur_coord = [cur_coord[0] + loc[0], cur_coord[1] + loc[1]]
    if len(locations) > len(output):
        output = locations[:]
        outfile = file_copy[:]
        outheading = headings[:]

clockwise = False

clockwise_sum = 0
for i in enumerate(output[:-2]):
    pointa = i[1]
    pointb = output[i[0] + 1]
    clockwise_sum += (pointb[0] - pointa[0]) * (pointa[1] + pointb[1])
if clockwise_sum > 0:
    clockwise = True

print(clockwise)

for location, direction in zip(output, outheading):
    match direction:
        #i honestly don't know why this works
        case "down":
            right_coord = [0, -1]
            if not clockwise:
                right_coord = [0, 1]
        case "up":
            right_coord = [0, 1]
            if not clockwise:
                right_coord = [0, -1]
        case "left":
            right_coord = [-1, 0]
            if not clockwise:
                right_coord = [1, 0]
        case "right":
            right_coord = [1, 0]
            if not clockwise:
                right_coord = [-1, 0]
    right_coord = [location[0] + right_coord[0], location[1] + right_coord[1]]
    if outfile[right_coord[0]][right_coord[1]] == "X":
        continue
    else:
        outfile = floodfill(outfile, right_coord)
part2out = 0
for i in outfile:
    part2out += i.count("I")

printfile(outfile) #visualization
print("part 1: ", ceil(len(output) / 2))
print("part 2: ", part2out)
