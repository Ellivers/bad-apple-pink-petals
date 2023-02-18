# Instructions for how to use this tool

## Prerequisites
* FFMPEG. You can check if it's intalled by running `ffmpeg`.
* The opencv-python Python package.
* Your own copy of the Bad Apple! music video. Rename it to "base.webm" and put it in this folder. (If it's not a WEBM file, edit the first line in convert.bat/convert.sh to use your file extension instead)
* Setting Minecraft to use 8GB RAM is recommended.

## Steps
1. Run convert.bat or convert.sh
2. Edit the generate.py file and change the coordinates at the second config line in the file to the northwest coordinates of where you want your video in-game. Make sure that you have base blocks underneath the video area, made of blocks that Pink Petals can be placed on. The default video area is 40x30 blocks.
3. Run generate.py.
4. Copy the generated data pack folder to your Minecraft world's "datapacks" folder.
6. Exit and reopen the Minecraft world.

You can replay the video without reloading by typing "/function bad_apple:load"
