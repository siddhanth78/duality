import pygame, sys
from pygame.locals import *

screen = pygame.display.set_mode((1000, 500))
clock = pygame.time.Clock()

all_points = []
point_dual = []
segments = []
segment_dual = []
segment_eps = []

class Point(pygame.sprite.Sprite):
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.rect = Rect(x-5, y-5, 10, 10)
		self.color = (255, 255, 255)

class Line(pygame.sprite.Sprite):
	def __init__(self, px, py, sx, ex):
		self.startx = sx
		self.starty = 250 + (((px*(-5)))-py)
		self.endx = ex
		self.endy = 250 + ((px*5) - py)
		self.color = (255, 255, 255)

point_selected = None
end_point_1 = None
end_point_2 = None

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
						point_dual.append(Line(px, py, sx, ex))
				elif point_selected is not None:
						point_selected = None

			elif event.button == 3 and point_selected is None:
				if end_point_1 is None:
					for p in range(len(all_points)):
						if all_points[p].rect.collidepoint((mx, my)):
							end_point_1 = p
							break
				elif end_point_1 is not None:
					flag = 0
					for p in range(len(all_points)):
						if all_points[p].rect.collidepoint((mx, my)):
							end_point_2 = p
							if end_point_1 == end_point_2:
								flag = 1
							break
					if end_point_2 is not None:
						if flag == 1:
							seg_pops = []
							for s in range(len(segments)):
								if p in segment_eps[s]:
									seg_pops.append(s)
							for i in range(len(seg_pops)-1, -1, -1):
								segments.pop(seg_pops[i])
								segment_eps.pop(seg_pops[i])
							all_points.pop(p)
							point_dual.pop(p)
							if all_points == []:
								segments = []
								segment_eps = []
						else:
							if ((all_points[end_point_1].x <= 500 and all_points[end_point_2].x <= 500)
								or (all_points[end_point_1].x > 500 and all_points[end_point_2].x > 500)) and ((end_point_1, end_point_2) not in segment_eps):
								segment_eps.append((end_point_1, end_point_2))
								segments.append(((all_points[end_point_1].x, all_points[end_point_1].y),
												(all_points[end_point_2].x, all_points[end_point_2].y)))
								#TODO: point representation of segment
					end_point_1 = None
					end_point_2 = None

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
		point_dual[point_selected].startx = sx
		point_dual[point_selected].starty = 250 + (((px*(-5)))-py)
		point_dual[point_selected].endx = ex
		point_dual[point_selected].endy = 250 + ((px*5) - py)

	for p in range(len(all_points)):
		if all_points[p].rect.collidepoint((mx, my)):
			all_points[p].color = (255, 0, 0)
			point_dual[p].color = (0, 255, 0)
		else:
			all_points[p].color = (255, 255, 255)
			point_dual[p].color = (255, 255, 255)

		if p == end_point_1:
			all_points[p].color = (0, 0, 255)
		pygame.draw.circle(screen, all_points[p].color, (all_points[p].x, all_points[p].y), 5)
		pygame.draw.line(screen, point_dual[p].color, (point_dual[p].startx, point_dual[p].starty), (point_dual[p].endx, point_dual[p].endy))

	for s in range(len(segments)):
		pygame.draw.line(screen, (255, 255, 255), segments[s][0], segments[s][1])

	pygame.display.flip()
	clock.tick(15)
