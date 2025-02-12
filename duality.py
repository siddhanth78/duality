import pygame, sys
from pygame.locals import *

screen = pygame.display.set_mode((1000, 500))
clock = pygame.time.Clock()

all_points = []
other_lines = []
#TODO segments = []

class Point(pygame.sprite.Sprite):
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.rect = Rect(x-5, y-5, 10, 10)
		self.color = (255, 255, 255)

class Line(pygame.sprite.Sprite):
	def __init__(self, px, py, sx, ex):
		self.startx = sx
		self.starty = 250 + (((px*(-250))/100)-py)
		self.endx = ex
		self.endy = 250 + ((px*250)/100 - py)
		self.color = (255, 255, 255)

point_selected = None

mode = "point"

while True:
	screen.fill((0,0,0))

	mx, my = pygame.mouse.get_pos()
	mx, my = int(mx), int(my)

	pygame.draw.line(screen, (0, 255, 255), (500, 0), (500, 500), 7)
	pygame.draw.line(screen, (64, 64, 64), (250, 0), (250, 500), 3)
	pygame.draw.line(screen, (64, 64, 64), (750, 0), (750, 500), 3)
	pygame.draw.line(screen, (64, 64, 64), (0, 250), (1000, 250), 3)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit(0)
		elif event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 1:
				if mx <= 500:
					px = mx - 250
					py = my - 250
					sx, ex = 500, 1000
				elif mx > 500:
					px = mx - 750
					py = my - 250
					sx, ex = 0, 500
				if point_selected is None:
					for p in range(len(all_points)):
						if all_points[p].rect.collidepoint((mx, my)):
							point_selected = p
							break
					if point_selected is None:
						all_points.append(Point(mx, my))
						other_lines.append(Line(px, py, sx, ex))
				elif point_selected is not None:
						point_selected = None

	if point_selected is not None:
		if mx <= 500:
			px = mx - 250
			py = my - 250
			sx, ex = 500, 1000
		elif mx > 500:
			px = mx - 750
			py = my - 250
			sx, ex = 0, 500
		all_points[point_selected].x, all_points[point_selected].y = mx, my
		all_points[point_selected].rect = Rect(mx-5, my-5, 10, 10)
		other_lines[point_selected].startx = sx
		other_lines[point_selected].starty = 250 + (((px*(-250))/100)-py)
		other_lines[point_selected].endx = ex
		other_lines[point_selected].endy = 250 + ((px*250)/100 - py)

	for p in range(len(all_points)):
		if all_points[p].rect.collidepoint((mx, my)):
			all_points[p].collided = True
			all_points[p].color = (255, 0, 0)
			other_lines[p].color = (0, 255, 0)
		else:
			all_points[p].collided = False
			all_points[p].color = (255, 255, 255)
			other_lines[p].color = (255, 255, 255)
		pygame.draw.circle(screen, all_points[p].color, (all_points[p].x, all_points[p].y), 5)
		pygame.draw.line(screen, other_lines[p].color, (other_lines[p].startx, other_lines[p].starty), (other_lines[p].endx, other_lines[p].endy))

	pygame.display.flip()
	clock.tick(15)
