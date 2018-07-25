import cranberry, threading

import pygame

# Initialize.
pygame.init()

# Call senpai.
import assets.api.SenPy as senpai
imouto = senpai.remote["imouto"]

# Make imouto pretty.
imouto.background = None

# Start the game.
imouto.start(
	60,
	(320, 480),
	pygame.HWSURFACE|pygame.DOUBLEBUF
)

def draw():
	import render

# Wait for the the screen to load before drawing.
threading.Timer(1, draw).start()

while True:
	imouto.update()