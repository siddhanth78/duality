import pygame, sys
from pygame.locals import *
import numpy as np

screen = pygame.display.set_mode((1000, 500))
mode = 'point'
clock = pygame.time.Clock()

all_points = []
other_lines = []

class Point(pygame.sprite.Sprite):
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.rect = Rect(x-5, y-5, 10, 10)
		self.color = (255, 255, 255)
		self.selected = False
		self.collided = True

class Line(pygame.sprite.Sprite):
	def __init__(self, px, py):
		self.startx = 500
		self.starty = 250 + (((px*(-250))/100)-py)
		self.endx = 1000
		self.endy = 250 + ((px*250)/100 - py)

point_selected = False

while True:
	clock.tick(15)

	screen.fill((0,0,0))

	mx, my = pygame.mouse.get_pos()
	mx, my = int(mx), int(my)

	pygame.draw.line(screen, (128, 128, 128), (500, 0), (500, 500), 7)
	pygame.draw.line(screen, (128, 128, 128), (250, 0), (250, 500), 3)
	pygame.draw.line(screen, (128, 128, 128), (750, 0), (750, 500), 3)
	pygame.draw.line(screen, (128, 128, 128), (0, 250), (1000, 250), 3)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit(0)
		elif event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 1:
				if mx <= 500:
					px = mx - 250
					py = my - 250

					all_points.append(Point(mx, my))
					other_lines.append(Line(px, py))

	for l in other_lines:
		pygame.draw.line(screen, (255, 255, 255), (l.startx, l.starty), (l.endx, l.endy))

	for p in all_points:
		if p.rect.collidepoint((mx, my)):
			p.collided = True
			p.color = (255, 0, 0)
		else:
			p.collided = False
			p.color = (255, 255, 255)
		pygame.draw.circle(screen, p.color, (p.x, p.y), 5)

	pygame.display.flip()
