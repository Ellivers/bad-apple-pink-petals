import os
import os.path
import shutil
from time import sleep

import cv2

###################
# CONFIGURATION
outputname = "Generated Pack" # data pack name
worldstart = [-95,78,-104] # world start corner coordinates (northwest corner)
###################

if os.path.isdir(outputname):
    if input('"' + outputname + '" path already exists. Delete it? (y/n) ').lower() == 'y':
        shutil.rmtree(outputname)
    else:
        exit()

# Folders
os.makedirs(outputname + '/data/bad_apple/functions/frames')
os.makedirs(outputname + '/data/minecraft/tags/functions')

cap = cv2.VideoCapture("colorlimited.mp4")
res,frame = cap.read()
height, width, channels = frame.shape
print("Dimensions:", str(width) + "x" + str(height))
print("In-game:", str(int(width/2)) + "x" + str(int(height/2)))

if width % 2 == 1 or height % 2 == 1:
    print("\nERROR: Width and height of video must be divisible by 2.")
    sleep(2)
    exit()

pixels = []
for x in range(int(width/2)):
    pixels.append([])
    for y in range(int(height/2)):
        pixels[-1].append([-1,-1,-1])

count = 0

blockstates = {
    "[1, 0, 0, 0]": "",
    "[0, 1, 1, 0]": "flower_amount=4",
    "[1, 0, 0, 1]": "flower_amount=4",
    "[1, 1, 0, 0]": "facing=east,flower_amount=2",
    "[1, 1, 1, 0]": "facing=east,flower_amount=3",
    "[1, 1, 1, 1]": "flower_amount=4",
    "[0, 0, 0, 1]": "facing=south",
    "[0, 0, 1, 1]": "facing=west,flower_amount=2",
    "[0, 1, 1, 1]": "facing=west,flower_amount=3",
    "[0, 0, 1, 0]": "facing=west",
    "[1, 0, 1, 0]": "facing=north,flower_amount=2",
    "[0, 1, 0, 1]": "facing=south,flower_amount=2",
    "[1, 1, 0, 1]": "facing=south,flower_amount=3",
    "[1, 0, 1, 1]": "facing=north,flower_amount=3",
    "[0, 1, 0, 0]": "facing=east"
}

def chkframe(fr, x, y):
    br = fr[y,x][0]
    if (br >= 100):
        return 1
    else:
        return 0

print("Generating... (this shouldn't take too long)")

# pack.mcmeta file
file = open(outputname + '/pack.mcmeta', 'w')
file.write('{"pack":{"pack_format":11,"description":"Bad Apple with cherry petals"}}')
file.close()

# Load function tag
file = open(outputname + '/data/minecraft/tags/functions/load.json', 'w')
file.write('{"values":["bad_apple:load"]}')
file.close()

# Tick function tag
file = open(outputname + '/data/minecraft/tags/functions/tick.json', 'w')
file.write('{"values":["bad_apple:tick"]}')
file.close()

# Load function
file = open(outputname + '/data/bad_apple/functions/load.mcfunction', 'w')
file.write('scoreboard objectives add bad_apple dummy\nscoreboard players set #tick bad_apple -1')
file.close()

# Tick function
tick = open(outputname + '/data/bad_apple/functions/tick.mcfunction', 'w')
tick.write('scoreboard players add #tick bad_apple 1\n')

# Frame functions
while res:
    tick.write('execute if score #tick bad_apple matches %s run function bad_apple:frames/%s\n' % (count,count))

    file = open(outputname + "/data/bad_apple/functions/frames/%s.mcfunction" % count, 'w')

    for y in range(0, int(height), 2):
        for x in range(0, int(width), 2):
            points = [chkframe(frame, x, y),
                      chkframe(frame, x+1, y),
                      chkframe(frame, x, y+1),
                      chkframe(frame, x+1, y+1)]
            if points == pixels[int(x/2)][int(y/2)]:
                continue
            pixels[int(x/2)][int(y/2)] = points

            if (points == [0,0,0,0]):
                file.write("setblock " + str(int(worldstart[0]+(x/2))) + " " + str(worldstart[1]) + " " + str(int(worldstart[2]+(y/2))) +
                    " minecraft:air\n")
                continue
            file.write("setblock " + str(int(worldstart[0]+(x/2)))+ " " + str(worldstart[1]) + " " + str(int(worldstart[2]+(y/2))) +
                " minecraft:pink_petals[%s]\n" % blockstates[str(points)])
    file.close()

    res,frame = cap.read()
    count += 1

tick.close()
cap.release()
cv2.destroyAllWindows()

print("Done!")
