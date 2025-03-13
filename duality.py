import pygame, sys
from pygame.locals import *
import random
from color_gen import gen_color

screen = pygame.display.set_mode((1000, 500))
clock = pygame.time.Clock()

all_points = []
point_dual = []
segments = []
segment_dual = []
segment_eps = []
wedges = []
rays = []
ray_dual = []
ray_wedges = []
ray_eps = []
color_pallete = gen_color()
color_pt = 0

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

def draw_polygon_alpha(surface, color, points):
	lx, ly = zip(*points)
	min_x, min_y, max_x, max_y = min(lx), min(ly), max(lx), max(ly)
	target_rect = pygame.Rect(min_x, min_y, max_x - min_x, max_y - min_y)
	shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
	pygame.draw.polygon(shape_surf, color, [(x - min_x, y - min_y) for x, y in points])
	surface.blit(shape_surf, target_rect)

def get_segment_dual(e1, e2):
	x_0, y_0 = e1[0], e1[1]
	x_1, y_1 = e2[0], e2[1]
	
	if x_0 <= 500:
		x_0 = x_0 - 250
		x_1 = x_1 - 250
		x_flag = 0
	else:
		x_0 = x_0 - 750
		x_1 = x_1 - 750
		x_flag = 1
	
	y_0 = y_0 - 250
	y_1 = y_1 - 250

	if x_0 == x_1: x_1 += 1

	m = (y_1 - y_0)/(x_1 - x_0)
	if x_flag == 0:
		x = int(750 + m*50)
	elif x_flag == 1:
		x = int(250 + m*50)
	y = 250 + int(m*x_0 - y_0)

	if x_flag == 0 and x < 500:
		x = 1500
	elif x_flag == 1 and x > 500:
		x = -10

	return Point(x, y)

def get_ray(coords):
	ox, oy = coords[0], coords[1]
	mx, my = coords[2], coords[3]
	if ox <= 500:
		min_x = 0
		max_x = 500
	elif ox > 500:
		min_x = 500
		max_x = 1000

	if ox == mx:
		ox += 1
	m = (my - oy)/(mx - ox)
	b = int(my - m*mx)
	if mx > ox:
		ey = int(m*max_x + b)
		ex = max_x
	elif mx < ox:
		ey = int(m*min_x + b)
		ex = min_x

	return [ox, oy, ex, ey]

point_selected = None
seg_selected = None
end_point_1 = None
end_point_2 = None
ray_drawn = False
ray_selected = None
ray_redrawn = False

while True:
	screen.fill((0,0,0))

	mx, my = pygame.mouse.get_pos()
	mx, my = int(mx), int(my)

	pygame.draw.line(screen, (128, 128, 128), (500, 0), (500, 500), 7)
	pygame.draw.line(screen, (64, 64, 64), (250, 0), (250, 500), 3)
	pygame.draw.line(screen, (64, 64, 64), (750, 0), (750, 500), 3)
	pygame.draw.line(screen, (64, 64, 64), (0, 250), (1000, 250), 3)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit(0)
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				pygame.quit()
				sys.exit(0)
			elif event.key == pygame.K_BACKSPACE:
				if point_selected is not None:
					p = point_selected
					seg_pops = []
					ray_pops = []
					for s in range(len(segments)):
						if p in segment_eps[s]:
							seg_pops.append(s)
					for r in range(len(rays)):
						if [all_points[p][0].x, all_points[p][0].y] == ray_eps[r]:
							ray_pops.append(r)
					for i in range(len(seg_pops)-1, -1, -1):
						segments.pop(seg_pops[i])
						segment_eps.pop(seg_pops[i])
						segment_dual.pop(seg_pops[i])
						wedges.pop(seg_pops[i])
					for j in range(len(ray_pops)-1, -1, -1):
						rays.pop(ray_pops[j])
						ray_eps.pop(ray_pops[j])
						ray_dual.pop(ray_pops[j])
						ray_wedges.pop(ray_pops[j])
					all_points.pop(p)
					point_dual.pop(p)
					if seg_pops:
						all_ps = []
						for ap in all_points:
							all_ps.append([ap[0].x, ap[0].y])
						for se in range(len(segment_eps)):
							segment_eps[se] = [all_ps.index(segments[se][0]), all_ps.index(segments[se][1])]
					if all_points == []:
						segments = []
						segment_eps = []
						wedges = []
						segment_dual = []
						rays = []
						ray_eps = []
						ray_dual = []
						ray_wedges = []
					end_point_1 = None
					point_selected = None
			elif event.key == pygame.K_c:
				segments = []
				all_points = []
				point_dual = []
				segment_dual = []
				segment_eps = []
				wedges = []
				rays = []
				ray_eps = []
				ray_dual = []
				ray_wedges = []
				point_selected = None
				seg_selected = False
				ray_selected = None
				ray_drawn = False
				end_point_1 = None
				end_point_2 = None
				ray_redrawn = False
				seg_changed = []
				ray_changed = []
			elif event.key == pygame.K_r:
				if end_point_1 is not None and ray_selected is None:
					if mx <= 500:
						px = mx - 250
						py = my - 250
						sx, ex = 500, 1000
					elif mx > 500:
						px = mx - 750
						py = my - 250
						sx, ex = 0, 500
					color_del = color_pallete[color_pt]
					color_pt = (color_pt+1)%len(color_pallete)
					all_points[end_point_1][1] = color_del
					rays.append([get_ray([all_points[end_point_1][0].x, all_points[end_point_1][0].y, mx, my]), color_del])
					ray_eps.append([all_points[end_point_1][0].x, all_points[end_point_1][0].y])
					ray_dual.append(get_segment_dual([rays[-1][0][0], rays[-1][0][1]], [rays[-1][0][2], rays[-1][0][3]]))
					if all_points[end_point_1][0].x <= 500:
						if mx >= all_points[end_point_1][0].x:
							topc = (500, 0)
							bottomc = (1000, 500)
							raywsx, raywsy = point_dual[end_point_1].startx, point_dual[end_point_1].starty
							raywex, raywey = point_dual[end_point_1].endx, point_dual[end_point_1].endy
						else:
							topc = (1000, 0)
							bottomc = (500, 500)
							raywsx, raywsy = point_dual[end_point_1].endx, point_dual[end_point_1].endy
							raywex, raywey = point_dual[end_point_1].startx, point_dual[end_point_1].starty
					else:
						if mx >= all_points[end_point_1][0].x:
							topc = (0, 0)
							bottomc = (500, 500)
							raywsx, raywsy = point_dual[end_point_1].startx, point_dual[end_point_1].starty
							raywex, raywey = point_dual[end_point_1].endx, point_dual[end_point_1].endy
						else:
							topc = (500, 0)
							bottomc = (0, 500)
							raywsx, raywsy = point_dual[end_point_1].endx, point_dual[end_point_1].endy
							raywex, raywey = point_dual[end_point_1].startx, point_dual[end_point_1].starty
					ray_wedges.append([ray_dual[-1], 0, 500,
									raywsx, raywsy, raywex, raywey,
									topc, bottomc])
					ray_selected = -1
					ray_drawn = True
					
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
				if end_point_1 is not None:
					end_point_1 = None
					end_point_2 = None
				elif point_selected is None:
					for p in range(len(all_points)):
						if all_points[p][0].rect.collidepoint((mx, my)):
							point_selected = p
							break
					if point_selected is None:
						color_del = color_pallete[color_pt]
						color_pt = (color_pt+1)%len(color_pallete)
						all_points.append([Point(mx, my), color_del])
						point_dual.append(Line(px, py, sx, ex))
					elif point_selected is not None:
						seg_changed = []
						ray_changed = []
						for s in range(len(segment_eps)):
							if point_selected in segment_eps[s]:
								seg_changed.append([s, segment_eps[s].index(point_selected)])
						for r in range(len(ray_eps)):
							if [all_points[point_selected][0].x, all_points[point_selected][0].y] == ray_eps[r]:
								ray_changed.append(r)
						if seg_changed != []:
							seg_selected = True
						if ray_changed != []:
							ray_redrawn = True
				elif point_selected is not None:
						point_selected = None
						seg_selected = False
						end_point_1 = None
						end_point_2 = None
						ray_redrawn = False
						seg_changed = []
						ray_changed = []

				if ray_selected is not None:
					rays[ray_selected][0] = get_ray(rays[ray_selected][0])
					ray_eps[ray_selected] = [rays[ray_selected][0][0], rays[ray_selected][0][1]]
					ray_dual[ray_selected] = get_segment_dual([rays[ray_selected][0][0], rays[ray_selected][0][1]], [rays[ray_selected][0][2], rays[ray_selected][0][3]])
					ray_wedges[ray_selected] = [ray_dual[ray_selected], 0, 500,
									ray_wedges[ray_selected][3], ray_wedges[ray_selected][4], ray_wedges[ray_selected][5], ray_wedges[ray_selected][6],
									ray_wedges[ray_selected][7], ray_wedges[ray_selected][8]]

					ray_selected = None
					ray_drawn = False

			elif event.button == 3 and point_selected is None:
				if end_point_1 is None:
					for p in range(len(all_points)):
						if all_points[p][0].rect.collidepoint((mx, my)):
							end_point_1 = p
							break
				elif end_point_1 is not None:
					flag = 0
					for p in range(len(all_points)):
						if all_points[p][0].rect.collidepoint((mx, my)):
							end_point_2 = p
							if end_point_1 == end_point_2:
								flag = 1
							break
					if end_point_2 is not None:
						if flag == 1:
							seg_pops = []
							ray_pops = []
							for s in range(len(segment_eps)):
								if p in segment_eps[s]:
									seg_pops.append(s)
							for r in range(len(ray_eps)):
								if [all_points[p][0].x, all_points[p][0].y] == ray_eps[r]:
									ray_pops.append(r)
							for i in range(len(seg_pops)-1, -1, -1):
								segments.pop(seg_pops[i])
								segment_eps.pop(seg_pops[i])
								segment_dual.pop(seg_pops[i])
								wedges.pop(seg_pops[i])
							for j in range(len(ray_pops)-1, -1, -1):
								rays.pop(ray_pops[j])
								ray_eps.pop(ray_pops[j])
								ray_dual.pop(ray_pops[j])
								ray_wedges.pop(ray_pops[j])
							all_points.pop(p)
							point_dual.pop(p)
							if seg_pops:
								all_ps = []
								for ap in all_points:
									all_ps.append([ap[0].x, ap[0].y])
								for se in range(len(segment_eps)):
									try:
										segment_eps[se] = [all_ps.index(segments[se][0]), all_ps.index(segments[se][1])]
									except:
										print(all_ps, segment_eps, segments)
							if all_points == []:
								segments = []
								segment_eps = []
								wedges = []
								segment_dual = []
								rays = []
								ray_eps = []
								ray_dual = []
								ray_wedges = []
						else:
							if (((all_points[end_point_1][0].x <= 500 and all_points[end_point_2][0].x <= 500)
								or (all_points[end_point_1][0].x > 500 and all_points[end_point_2][0].x > 500))
								and (((end_point_1, end_point_2) not in segment_eps) and ((end_point_2, end_point_1) not in segment_eps))):
								if all_points[end_point_1][0].y == all_points[end_point_2][0].y:
									all_points[end_point_2][0].y -= 1
								sorted_eps = sorted([[all_points[end_point_1][0].x, all_points[end_point_1][0].y], [all_points[end_point_2][0].x, all_points[end_point_2][0].y]],
													key=lambda point_: point_[0])
								segments.append([sorted_eps[0], sorted_eps[1]])
								if [sorted_eps[0], sorted_eps[1]] == [[all_points[end_point_1][0].x, all_points[end_point_1][0].y],
																	[all_points[end_point_2][0].x, all_points[end_point_2][0].y]]:
									segment_eps.append([end_point_1, end_point_2])
								else:
									segment_eps.append([end_point_2, end_point_1])
								segment_dual.append(get_segment_dual(sorted_eps[0], sorted_eps[1]))
								p1, p2 = segment_eps[-1][0], segment_eps[-1][1]
								all_points[end_point_1][1] = color_pallete[color_pt]
								color_pt = (color_pt+1)%len(color_pallete)
								all_points[end_point_2][1] = all_points[end_point_1][1]
								wedges.append([[point_dual[p1].startx, point_dual[p1].starty, point_dual[p1].endx, point_dual[p1].endy],
												[point_dual[p2].startx, point_dual[p2].starty, point_dual[p2].endx, point_dual[p2].endy],
												segment_dual[-1], (*all_points[end_point_1][1], 127)])
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
		all_points[point_selected][0].x, all_points[point_selected][0].y = mx, my
		all_points[point_selected][0].rect = Rect(mx-5, my-5, 10, 10)
		point_dual[point_selected].startx = sx
		point_dual[point_selected].starty = 250 + (((px*(-5)))-py)
		point_dual[point_selected].endx = ex
		point_dual[point_selected].endy = 250 + ((px*5) - py)
		if seg_selected == True:
			for sc in seg_changed:
				if (segments[sc[0]][(sc[1]-1)*(-1)][0] <= 495 and all_points[point_selected][0].x > 495):
					all_points[point_selected][0].x = 495
					all_points[point_selected][0].rect = Rect(490, my-5, 10, 10)
					point_dual[point_selected].startx = 500
					point_dual[point_selected].starty = 250 + (((245*(-5)))-py)
					point_dual[point_selected].endx = 1000
					point_dual[point_selected].endy = 250 + ((245*5) - py)

				elif (segments[sc[0]][(sc[1]-1)*(-1)][0] > 505 and all_points[point_selected][0].x <= 505):
					all_points[point_selected][0].x = 505
					all_points[point_selected][0].rect = Rect(500, my-5, 10, 10)
					point_dual[point_selected].startx = 0
					point_dual[point_selected].starty = 250 + ((((-245)*(-5)))-py)
					point_dual[point_selected].endx = 500
					point_dual[point_selected].endy = 250 + (((-245)*5) - py)

				segments[sc[0]][sc[1]] = [all_points[point_selected][0].x, all_points[point_selected][0].y]
				if segments[sc[0]][0][1] == segments[sc[0]][1][1]:
					segments[sc[0]][1][1] -= 1
				sorted_eps = sorted([segments[sc[0]][0], segments[sc[0]][1]],
									key=lambda point_: point_[0])
				if (sorted_eps[0], sorted_eps[1]) != (segments[sc[0]][0], segments[sc[0]][1]):
					segment_eps[sc[0]] = [segment_eps[sc[0]][1], segment_eps[sc[0]][0]]
					segments[sc[0]] = [sorted_eps[0], sorted_eps[1]]
					seg_changed[seg_changed.index(sc)][1] = 0 if seg_changed[seg_changed.index(sc)][1] == 1 else 1
				segment_dual[sc[0]] = get_segment_dual(sorted_eps[0], sorted_eps[1])
				p1, p2 = segment_eps[sc[0]][0], segment_eps[sc[0]][1]
				wedges[sc[0]] = [[point_dual[p1].startx, point_dual[p1].starty, point_dual[p1].endx, point_dual[p1].endy],
								[point_dual[p2].startx, point_dual[p2].starty, point_dual[p2].endx, point_dual[p2].endy],
								segment_dual[sc[0]], wedges[sc[0]][3]]
		if ray_redrawn == True:
			for rc in ray_changed:
				if all_points[point_selected][0].x > 495 and rays[rc][0][0] <= 495:
					all_points[point_selected][0].x = 495
					all_points[point_selected][0].rect = Rect(490, my-5, 10, 10)
					point_dual[point_selected].startx = 500
					point_dual[point_selected].starty = 250 + (((245*(-5)))-py)
					point_dual[point_selected].endx = 1000
					point_dual[point_selected].endy = 250 + ((245*5) - py)

				elif all_points[point_selected][0].x <= 505 and rays[rc][0][0] > 505:
					all_points[point_selected][0].x = 505
					all_points[point_selected][0].rect = Rect(500, my-5, 10, 10)
					point_dual[point_selected].startx = 0
					point_dual[point_selected].starty = 250 + ((((-245)*(-5)))-py)
					point_dual[point_selected].endx = 500
					point_dual[point_selected].endy = 250 + (((-245)*5) - py)

				if all_points[point_selected][0].x <= 500:
					if rays[rc][0][2] >= all_points[point_selected][0].x:
						topc = (500, 0)
						bottomc = (1000, 500)
						raywsx, raywsy = point_dual[point_selected].startx, point_dual[point_selected].starty
						raywex, raywey = point_dual[point_selected].endx, point_dual[point_selected].endy
					else:
						topc = (1000, 0)
						bottomc = (500, 500)
						raywsx, raywsy = point_dual[point_selected].endx, point_dual[point_selected].endy
						raywex, raywey = point_dual[point_selected].startx, point_dual[point_selected].starty
				else:
					if rays[rc][0][2] >= all_points[point_selected][0].x:
						topc = (0, 0)
						bottomc = (500, 500)
						raywsx, raywsy = point_dual[point_selected].startx, point_dual[point_selected].starty
						raywex, raywey = point_dual[point_selected].endx, point_dual[point_selected].endy
					else:
						topc = (500, 0)
						bottomc = (0, 500)
						raywsx, raywsy = point_dual[point_selected].endx, point_dual[point_selected].endy
						raywex, raywey = point_dual[point_selected].startx, point_dual[point_selected].starty

				rays[rc][0][0], rays[rc][0][1] = all_points[point_selected][0].x, all_points[point_selected][0].y
				ray_eps[rc] = [all_points[point_selected][0].x, all_points[point_selected][0].y]
				ray_dual[rc] = get_segment_dual([all_points[point_selected][0].x, all_points[point_selected][0].y], [rays[rc][0][2], rays[rc][0][3]])
				ray_wedges[rc] = [ray_dual[rc], 0, 500,
									raywsx, raywsy, raywex, raywey,
									topc, bottomc]


	if ray_drawn == True:
		if rays[ray_selected][0][0] <= 500:
			if mx >= rays[ray_selected][0][0]:
				topc = (500, 0)
				bottomc = (1000, 500)
				raywsx, raywsy = point_dual[end_point_1].startx, point_dual[end_point_1].starty
				raywex, raywey = point_dual[end_point_1].endx, point_dual[end_point_1].endy
			else:
				topc = (1000, 0)
				bottomc = (500, 500)
				raywsx, raywsy = point_dual[end_point_1].endx, point_dual[end_point_1].endy
				raywex, raywey = point_dual[end_point_1].startx, point_dual[end_point_1].starty
		else:
			if mx >= rays[ray_selected][0][0]:
				topc = (0, 0)
				bottomc = (500, 500)
				raywsx, raywsy = point_dual[end_point_1].startx, point_dual[end_point_1].starty
				raywex, raywey = point_dual[end_point_1].endx, point_dual[end_point_1].endy
			else:
				topc = (500, 0)
				bottomc = (0, 500)
				raywsx, raywsy = point_dual[end_point_1].endx, point_dual[end_point_1].endy
				raywex, raywey = point_dual[end_point_1].startx, point_dual[end_point_1].starty

		rays[ray_selected][0][2] = mx
		rays[ray_selected][0][3] = my
		ray_eps[ray_selected] = [rays[ray_selected][0][0], rays[ray_selected][0][1]]
		ray_dual[ray_selected] = get_segment_dual([rays[ray_selected][0][0], rays[ray_selected][0][1]], [rays[ray_selected][0][2], rays[ray_selected][0][3]])
		ray_wedges[ray_selected] = [ray_dual[ray_selected], 0, 500,
							raywsx, raywsy, raywex, raywey,
							topc, bottomc]

	for r in range(len(rays)):
		if ray_dual[r].rect.collidepoint((mx, my)):
			r_col = (255,255,255)
			thicn = 3
		else:
			r_col = (*rays[r][1], 127)
			thicn = 1
		pygame.draw.line(screen, r_col, (rays[r][0][0], rays[r][0][1]), (rays[r][0][2], rays[r][0][3]), width=thicn)
		pygame.draw.line(screen, r_col, (ray_dual[r].x, 0), (ray_dual[r].x, 500))
		pygame.draw.circle(screen, r_col, (ray_dual[r].x, ray_dual[r].y), 5)
		draw_polygon_alpha(screen, r_col, ((ray_wedges[r][0].x, ray_wedges[r][0].y), (ray_wedges[r][3], ray_wedges[r][4]), ray_wedges[r][7], (ray_wedges[r][0].x, 0)))
		draw_polygon_alpha(screen, r_col, ((ray_wedges[r][0].x, ray_wedges[r][0].y), (ray_wedges[r][5], ray_wedges[r][6]), ray_wedges[r][8], (ray_wedges[r][0].x, 500)))

	for s in range(len(segments)):
		if segment_dual[s].rect.collidepoint((mx, my)):
			segment_dual[s].color = (255, 255, 255)
			pygame.draw.line(screen, (255, 255, 255), segments[s][0], segments[s][1], width=3)
		else:
			segment_dual[s].color = wedges[s][3]
			pygame.draw.line(screen, wedges[s][3], segments[s][0], segments[s][1])
		pygame.draw.circle(screen, segment_dual[s].color, (segment_dual[s].x, segment_dual[s].y), 5)
		draw_polygon_alpha(screen, segment_dual[s].color, ((wedges[s][0][0], wedges[s][0][1]), (wedges[s][1][0], wedges[s][1][1]), (wedges[s][2].x, wedges[s][2].y)))
		draw_polygon_alpha(screen, segment_dual[s].color, ((wedges[s][0][2], wedges[s][0][3]), (wedges[s][1][2], wedges[s][1][3]), (wedges[s][2].x, wedges[s][2].y)))

	for p in range(len(all_points)):
		if all_points[p][0].rect.collidepoint((mx, my)):
			all_points[p][0].color = (255, 255, 255) 
			point_dual[p].color = (255, 255, 255)
			thiccness = 3
		else:
			all_points[p][0].color = all_points[p][1]
			point_dual[p].color = all_points[p][1]
			thiccness = 1
		if p == end_point_1:
			all_points[p][0].color = (255, 255, 0)
			point_dual[p].color = (255, 255, 0)
			thiccness = 3
		pygame.draw.circle(screen, all_points[p][0].color, (all_points[p][0].x, all_points[p][0].y), 5)
		pygame.draw.line(screen, point_dual[p].color, (point_dual[p].startx, point_dual[p].starty), (point_dual[p].endx, point_dual[p].endy), width=thiccness)

	pygame.display.update()
	clock.tick(15)
