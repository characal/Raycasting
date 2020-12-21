import pygame, sys, math
from pygame.locals import *

pygame.init()

width = 500
height = 300
win = pygame.display.set_mode((width * 2, height * 2))
screen = pygame.Surface((width, height))

clock = pygame.time.Clock()
cell_size = 20

fists = pygame.image.load("fists.png")

map = [
"###############",
"###...........#",
"#.....###.....#",
"#.............#",
"#.............#",
"#.............#",
"#.............#",
"#.............#",
"#######....####",
"#.............#",
"#...####......#",
"#.............#",
"#......#####..#",
"#######.......#",
"#.............#",
"#........######",
"#........#.....",
"#........#.....",
"#.............#",
"###############",
]
music = pygame.mixer.music.load("soundtrack.mp3")
pygame.mixer.music.play(-1)

walls = []
for y in range(0, len(map)):
		for x in range(0, len(map[y])):
			if map[y][x] == "#":
				walls.append(pygame.Rect(x, y,  1, 1))

player_angle = 0
player_pos_x = 3
player_pos_y = 1
fov = 90
sens = 10
speed = 0.3
pygame.mouse.set_visible(False)
pygame.event.set_grab(True)
pygame.mouse.set_pos = (width, height)
mouse_dist = 0

while True:
	screen.fill((0, 0, 0))
	win.fill((0, 0, 0))

	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
		if event.type == KEYDOWN:
			if event.key == K_ESCAPE:
				pygame.event.set_grab(False)
				pygame.mouse.set_visible(True)
		if event.type == MOUSEBUTTONDOWN:
				pygame.mouse.set_visible(False)
				pygame.event.set_grab(True)
				pygame.mouse.set_pos = (width / 2, height / 2)

	player_angle += pygame.mouse.get_rel()[0] / sens
	x_vel = 0
	y_vel = 0

	keys = pygame.key.get_pressed()
	if keys[K_w]:
		y_vel = math.sin(math.radians(player_angle)) * speed
		x_vel = math.cos(math.radians(player_angle)) * speed
	if keys[K_s]:
		y_vel = -math.sin(math.radians(player_angle)) * speed
		x_vel = -math.cos(math.radians(player_angle)) * speed
	if keys[K_a]:
		y_vel = math.sin(math.radians(player_angle - 90)) * speed
		x_vel = math.cos(math.radians(player_angle - 90)) * speed
	if keys[K_d]:
		y_vel = math.sin(math.radians(player_angle + 90)) * speed
		x_vel = math.cos(math.radians(player_angle + 90)) * speed

	try:
		player_pos_x += x_vel
		if map[int(player_pos_y)][int(player_pos_x)] == "#":
			player_pos_x -= x_vel

		player_pos_y += y_vel
		if map[int(player_pos_y)][int(player_pos_x)] == "#":
			player_pos_y -= y_vel
	except:
		pass



	for x in range(0, width):
		angle = (player_angle - (fov / 2)) + (x / width) * fov

		hit_wall = False
		dist_to_wall = 0
		while not hit_wall and dist_to_wall < 16:
			dist_to_wall += 0.1
			pos_y = math.sin(math.radians(angle)) * dist_to_wall
			pos_x = math.cos(math.radians(angle)) * dist_to_wall

			try:
				if map[math.floor(pos_y + player_pos_y)][math.floor(pos_x + player_pos_x)] == "#":
					hit_wall = True
			except:
				pass

		colour = 255 - dist_to_wall * 15
		ceiling = height / 2 - height / dist_to_wall
		floor = height - ceiling

		for y in range(0, height):
			if y < ceiling:
				screen.set_at((x, y), (0, 0, 255))
			elif y > ceiling and y <= floor:
				screen.set_at((x, y), (colour, colour, colour))
			else:
				screen.set_at((x, y), (15 + (150 * ((y - floor) / (height - floor))), 20, 0 + (70 * ((y - floor) / (height - floor)))))

	screen.blit(pygame.transform.scale(fists, (int(height / 2), int(height / 2))), (0, height - height / 2))
	screen.blit(pygame.transform.flip(pygame.transform.scale(fists, (int(height / 2), int(height / 2))), True, False), (width - height / 2, height - height / 2))

	win.blit(pygame.transform.scale(screen, (width * 2, height * 2)), (0, 0))



	minimap_size = width * 2 / 7
	minimap = pygame.Surface((minimap_size, minimap_size))
	minimap.fill((125, 0, 0))
	player_x = player_pos_x * cell_size
	player_y = player_pos_y * cell_size

	for y in range(0, len(map)):
		for x in range(0, len(map[y])):
			if map[y][x] == "#":
				pygame.draw.rect(minimap, (255, 255, 255), (x * cell_size - player_x + minimap_size / 2, y * cell_size - player_y + minimap_size / 2,  cell_size, cell_size))

	pygame.draw.circle(minimap, (255, 255, 255), (minimap_size / 2, minimap_size / 2), 5)
	pygame.draw.rect(win, (255, 255, 255), (0, 0, minimap_size + 12, minimap_size + 12), 0)
	win.blit(minimap, (6, 6))


	pygame.display.update()
	clock.tick(60)