from math import ceil
import sys
sys.setrecursionlimit(100000)

def printfile(file):
    for i in file:
        print(''.join(i))
def process(file, coord, prevcoord):
    xpos = coord[0]
    ypos = coord[1]
    out = [coord]
    leftenter = {"J":[-1, 0], "7":[1, 0], "-":[0, 1]}
    rightenter = {"F":[1, 0], "L":[-1, 0], "-":[0, -1]}
    bottomenter = {"|":[-1, 0], "F":[0, 1], "7":[0, -1]}
    topenter = {"|":[1, 0], "L":[0, 1], "J":[0, -1]}
    possresults = []
    currchar = file[xpos][ypos]
    if currchar not in "FL7J|-":
        return [[], [file]]
    processindices = []
    file[xpos][ypos] = "X"
#    print()
#    print(f"{xpos=}, {ypos=}")
#    print(currchar)
    #printfile(file)
    if prevcoord == [xpos, ypos + 1]:
        dictionary = rightenter
    elif prevcoord == [xpos, ypos - 1]:
        dictionary = leftenter
    elif prevcoord == [xpos + 1, ypos]:
        dictionary = bottomenter 
    elif prevcoord == [xpos - 1, ypos]:
        dictionary = topenter 
    try:
        loc = dictionary[currchar]
    except KeyError:
        return [[], [file]]
    processindices = [xpos + loc[0], ypos + loc[1]]
    processoutput = process(file, processindices, coord)
    out += processoutput[0]
    file = processoutput[1]
    return [out, file]

def floodfill(array, coord):
    xpos = coord[0]
    ypos = coord[1]
    ispipe = False
    if array[xpos][ypos] == "X":
        ispipe = True
    if array[xpos][ypos] == "#":
        return array
    array[xpos][ypos] = "#"
    tryposs = []
    [[tryposs.append([x, y]) for y in range(ypos - 1, ypos + 2)] for x in range(xpos - 1, xpos + 2)]
#    print(tryposs, coord)
    for i in tryposs:
        if not (0 <= i[0] and i[0] < len(array)):
            continue
        if not (0 <= i[1] and i[1] < len(array[0])):
            continue
        if ispipe and  array[i[0]][i[1]] != "X":
            continue
#        print(i, coord)
        array = floodfill(array, i)
    return array
f = open("input.txt", 'r')
file = f.read().strip().split('\n')
#file = 
"""

.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ...

""".strip().split('\n')
#extra periods to pad it out so we don't run into errors
file = [['.'] + list(x) + ['.'] for x in file]
file.append(['.'] * len(file[0]))
file = [['.'] * len(file[0])] + file
data = []
end = False
data = [[], []]
for line in enumerate(file):
    for char in enumerate(line[1]):
        if char[1] == "S":
            leftenter = {"J":[-1, 0], "7":[1, 0], "-":[0, 1]}
            rightenter = {"F":[1, 0], "L":[-1, 0], "-":[0, -1]}
            bottomenter = {"|":[-1, 0], "F":[0, 1], "7":[0, -1]}
            topenter = {"|":[1, 0], "L":[0, 1], "J":[0, -1]}
            xpos = line[0]
            ypos = char[0]
            up = file[xpos - 1][ypos]
            down = file[xpos + 1][ypos]
            left = file[xpos][ypos - 1]
            right = file[xpos][ypos + 1]
            vert = list(topenter.keys()) + list(bottomenter.keys())
            horiz = list(rightenter.keys()) + list(leftenter.keys())
            possdicts = []
            if down in vert and right in horiz:
                file[xpos][ypos] = "F"
                possdicts.append(["F", rightenter | bottomenter])
            if left in horiz and right in horiz:
                file[xpos][ypos] = "-"
                possdicts.append(["-", rightenter | leftenter])
            if up in vert and right in horiz:
                file[xpos][ypos] = "L"
                possdicts.append(['L', rightenter | topenter])
            if down in vert and up in vert:
                file[xpos][ypos] = "|"
                possdicts.append(['|', bottomenter | topenter])
            if down in vert and left in horiz:
                file[xpos][ypos] = '7'
                possdicts.append(['7', leftenter | bottomenter])
            if up in vert and left in horiz:
                file[xpos][ypos] = 'J'
                possdicts.append(['J', leftenter | topenter])
            for i in possdicts:
                loc = i[1][i[0]]
                out = process(file, [xpos + loc[0], ypos + loc[1]], [xpos, ypos])
                if len(out[0]) > len(data[0]):
                    data = out[:]
            end = True
            break
    if end:
        break
print(data[0])
print(ceil(len(data[0]) / 2))
array = data[1][0]
printfile(array)
for i in range(len(file[0])):
    array = floodfill(array, [0, i])
    array = floodfill(array, [len(array) - 1, i])
for i in range(len(file)):
    array = floodfill(array, [i, 0])
    array = floodfill(array, [i, len(array[i]) - 1])

printfile(array)
out = 0
for i in array:
    out += len(i) - i.count("#")
print(out)
