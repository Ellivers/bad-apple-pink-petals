ffmpeg -i base.webm -vf scale=80x60,fps=20 -y downscaled.mp4
ffmpeg -i downscaled.mp4 -i palette.png -lavfi paletteuse -y colorlimited.mp4