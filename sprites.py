""" 
Filename: sprites.py
Purpose: Contains the classes necessary for Ghost Town. Classes include,
	- Control --> used for menu / button clicks.
	- Player --> contains functions for the player.
	- Ammo --> contains functions for the ammo.
	- Enemy --> contains functions for the enemies.
	- Wave --> contains the class for the infinite wave system.
	- Tree --> contains the class for the tree objects.

Author: Matthew Peres Tino

"""
#####################################################################################################
# imports
from settings import *

#####################################################################################################
# Player and enemy settings
ENEMY_IMAGE = pg.image.load('images/ghost.png')

# ammo settings
AMMO_IMAGE = pg.image.load('images/web_64.png')
AMMO_SMALL_VEL = 7
AMMO_W, AMMO_H = ENTITY_W / 2, ENTITY_H / 2

#####################################################################################################
# Control class
class Control():
	'''
	This class is responsible for controlling button clicks on the menu and other game events. 
	'''
	
	# constructor
	def __init__(self):
		super().__init__()

		# control stuff
		self.start_game = False
		self.quit_game = False
		self.go_to_options = False

		# title and author stuff
		self.title = TITLE_FONT.render("GHOST TOWN", 1, BLACK)
		self.author = HEALTH_FONT.render("Created by Matthew Peres Tino", 1, BLACK)

		# play button stuff
		self.play = PLAY_FONT.render("PLAY", 1, BLACK)
		self.play_rect = self.play.get_rect()
		self.play_rect.x = 0.5 * (WIDTH-self.play_rect.width)
		self.play_rect.y = 0.5 * (HEIGHT-self.play_rect.height)

		# options button stuff
		self.opt = PLAY_FONT.render("OPTIONS", 1, BLACK)
		self.opt_rect = self.opt.get_rect()
		self.opt_rect.x = 0.5 * (WIDTH-self.opt_rect.width)
		self.opt_rect.y = 0.5 * (HEIGHT-self.opt_rect.height) + 1.5*self.opt_rect.height
		
		# exit button stuff
		self.exit = PLAY_FONT.render("EXIT", 1, BLACK)
		self.exit_rect = self.exit.get_rect()
		self.exit_rect.x = 0.5 * (WIDTH-self.exit_rect.width)
		self.exit_rect.y = 0.5 * (HEIGHT-self.exit_rect.height) + 3*self.exit_rect.height

		# game stats
		self.ghosts_killed = 0
	
	# menu
	def draw_menu(self):
		
		# draw various menu items
		WIN.blit(grass_dark, (0,0))
		WIN.blit(self.title, (0.5*(WIDTH-self.title.get_width()), 120))
		WIN.blit(self.author, (0.5*(WIDTH-self.author.get_width()), 160 + self.title.get_height()))		
		WIN.blit(self.play, (self.play_rect.x, self.play_rect.y) )
		WIN.blit(self.exit, (self.exit_rect.x, self.exit_rect.y))
		WIN.blit(self.opt, (self.opt_rect.x, self.opt_rect.y))

	# options
	def draw_options(self):
		pass
		# draw options
		# opt 1 --> 

	# actual game
	def draw_game(self):

		# draw on screen the background
		WIN.blit(grass, (0,0))
		WIN.blit(house_main, (0.3*WIDTH, 0))
		WIN.blit(house_side, (0.3*WIDTH+house_side.get_width(), 0))
		WIN.blit(house_side, (0.3*WIDTH-house_side.get_width(), 0))

		# fence drawing
		num_fences = int(WIDTH / FENCE_W)
		middle_fence = math.floor(num_fences / 2)
		no_build = np.array([middle_fence-1, middle_fence, middle_fence+1])
		for i in range(num_fences):
			if i not in no_build :
				WIN.blit(fence, (i*FENCE_W, FENCE_DRAW_Y))

	def check_click(self):
		
		# play button
		if self.play_rect.collidepoint(pg.mouse.get_pos()):
			self.start_game = True
		
		# exit button
		elif self.exit_rect.collidepoint(pg.mouse.get_pos()):
			self.start_game = True
			self.quit_game = True
		
		# option button
		elif self.opt_rect.collidepoint(pg.mouse.get_pos()):
			self.start_game = True
			self.quit_game = False
			self.go_to_options = True 
	
	def hover_play(self):

		# change colours of buttons depending on hover position
		if self.play_rect.collidepoint(pg.mouse.get_pos()):
			self.play = PLAY_FONT.render("PLAY", 1, BUTTON_CLICK)
		elif ~self.play_rect.collidepoint(pg.mouse.get_pos()):
			self.play = PLAY_FONT.render("PLAY", 1, BLACK)		
	
	def hover_exit(self):
		# change colours of buttons depending on hover position
		if self.exit_rect.collidepoint(pg.mouse.get_pos()):
			self.exit = PLAY_FONT.render("EXIT", 1, BUTTON_CLICK)
		elif ~self.exit_rect.collidepoint(pg.mouse.get_pos()):
			self.exit = PLAY_FONT.render("EXIT", 1, BLACK)
	
	def hover_opt(self):
		# change colours of buttons depending on hover position
		if self.opt_rect.collidepoint(pg.mouse.get_pos()):
			self.opt = PLAY_FONT.render("OPTIONS", 1, BUTTON_CLICK)
		elif ~self.opt_rect.collidepoint(pg.mouse.get_pos()):
			self.opt = PLAY_FONT.render("OPTIONS", 1, BLACK)
	
	def update(self):
		self.hover_play()
		self.hover_exit()
		self.hover_opt()
	

#####################################################################################################
# Player class
#####################################################################################################
class Player(pg.sprite.Sprite):
	'''
	This class is responsible for the player (aka the user).
	'''
	
	# Constructor
	def __init__(self):
		super().__init__()
		self.image = pg.transform.scale(pg.image.load('images/player.png'), (ENTITY_W, ENTITY_H))
		self.rect = self.image.get_rect()
		self.rect.x = WIDTH / 2 - self.rect.width
		self.rect.y = HEIGHT / 2 

		self.direction = pg.math.Vector2()
		self.pos = pg.math.Vector2(self.rect.center)
		self.speed = 2000
		
		# health bar stuff
		self.health_bar = 0
		self.max_health = 1000
		self.curr_health = 1000

		# ammo
		self.ammo = pg.sprite.Group()
		self.curr_shot_t = pg.time.get_ticks()
		self.prev_shot_t = pg.time.get_ticks()
		self.fire_rate = 100 # this is the delay between firing ammo

	def move_player(self):
		keys_pressed = pg.key.get_pressed()
		if keys_pressed[pg.K_a] and self.rect.x > 0:
			self.direction.x = -1
		elif keys_pressed[pg.K_d] and self.rect.x < WIDTH-self.rect.width:
			self.direction.x = 1
		else:
			self.direction.x = 0

		if keys_pressed[pg.K_w] and self.rect.y > 0:
			self.direction.y = -1
		elif keys_pressed[pg.K_s] and self.rect.y < HEIGHT-self.rect.height:
			self.direction.y = 1
		else:
			self.direction.y = 0
	
	def adjust_speed(self):
		if self.direction.magnitude() > 0:
			self.direction = self.direction.normalize()
		self.pos += self.direction * self.speed * 0.002
		self.rect.center = self.pos
	
	def shoot(self):
		keys = pg.key.get_pressed()

		if keys[pg.K_i] or keys[pg.K_k] or keys[pg.K_j] or keys[pg.K_l]:
			self.curr_shot_t = pg.time.get_ticks()

			if self.curr_shot_t - self.prev_shot_t > self.fire_rate:
				if keys[pg.K_i]:
					self.ammo.add(Ammo('UP', \
					self.rect.x+0.8*self.rect.width, 
					self.rect.y+self.rect.height/2) )
				elif keys[pg.K_k]:
					self.ammo.add(Ammo('DOWN', \
					self.rect.x+0.8*self.rect.width, 
					self.rect.y+self.rect.height/2) )
				elif keys[pg.K_j]:
					self.ammo.add(Ammo('LEFT', \
					self.rect.x+0.5*self.rect.width, 
					self.rect.y+0.5*self.rect.height) )
				elif keys[pg.K_l]:
					self.ammo.add(Ammo('RIGHT', \
					self.rect.x+0.8*self.rect.width, 
					self.rect.y+0.5*self.rect.height) )
				self.prev_shot_t = pg.time.get_ticks()
				

	def update_health_bar(self):
		
		# quickly check for dead player!
		if self.curr_health < 1:
			sys.exit()

		# the physical health bar
		self.health_bar_out = pg.Rect(self.rect.x, self.rect.y-20, self.rect.width+8, 10)
		self.full_health = self.rect.width + 3
		self.health_bar_in = pg.Rect(self.rect.x+3, self.rect.y-17, self.full_health * (self.curr_health/self.max_health), 4)

		# health bar stats
		PLAYER_HEALTH_TEXT = HEALTH_FONT.render(str(int(100*self.curr_health/self.max_health)), 1, BLACK)
		draw_x = (self.health_bar_out.width - PLAYER_HEALTH_TEXT.get_width() ) / 2

		# drawing
		pg.draw.rect(WIN, BLACK, self.health_bar_out, 3)
		pg.draw.rect(WIN, RED, self.health_bar_in, 0)
		WIN.blit(PLAYER_HEALTH_TEXT, (self.rect.x+draw_x, self.rect.y - 40))


	def update(self):

		# note: health bar first otherwise there's a weird delay?
		self.shoot()
		self.update_health_bar()
		self.move_player()
		self.adjust_speed()


#####################################################################################################
# Ammo class
#####################################################################################################
class Ammo(pg.sprite.Sprite):

	'''
	This class is responsible for the ammo. Each ammo is an instance of this class.
	'''
	
	def __init__(self, dir, posX, posY):
		super().__init__()
		self.dir = dir
		self.image = pg.transform.scale(AMMO_IMAGE, (AMMO_W, AMMO_H))
		self.rect = self.image.get_rect()
		self.rect.x, self.rect.y = posX, posY
	
	def move(self):
		if self.dir == 'UP':
			self.rect.y -= AMMO_SMALL_VEL
		elif self.dir == 'DOWN':
			self.rect.y += AMMO_SMALL_VEL
		elif self.dir == 'LEFT':
			self.rect.x -= AMMO_SMALL_VEL
		elif self.dir == 'RIGHT':
			self.rect.x += AMMO_SMALL_VEL
	
	def check_bounds(self):
		# check to see if it is off screen, then kill the instance (don't overload container)
		if self.rect.x not in np.linspace(0-self.rect.width, WIDTH, WIDTH+1+self.rect.width ) \
		or self.rect.y not in np.linspace(0-self.rect.height, HEIGHT, HEIGHT+1+self.rect.height ):
			self.kill()

	def update(self):
		self.move()
		self.check_bounds()


#####################################################################################################
# Enemy class
#####################################################################################################
class Enemy(pg.sprite.Sprite):
	
	'''
	This class is responsible for the enemy. Each enemy is an insstance of this class. 
	'''

	# Constructor
	def __init__(self, menu, player = None):
		super().__init__()
		self.menu = menu 
		self.image = pg.transform.scale(pg.image.load('images/ghost.png'), (ENTITY_W, ENTITY_H))
		self.rect = self.image.get_rect()		

		# if this ghost is a menu ghost
		if self.menu:
			self.spawn_side = None
			self.despawn = None
			self.rect.x, self.rect.y = self.menu_coords()
		
		else:
			self.rect.x, self.rect.y = self.game_coords()
			self.player = player

	def menu_coords(self):
		
		coord_random_length = 1000 # how many ways to break up spawn point
		self.spawn_side = np.random.choice(np.array(['left', 'right']))

		# handle x
		if self.spawn_side == 'left':
			x_random = 0
		else:
			x_random = WIDTH-self.rect.width

		y_random = np.random.choice(np.linspace(self.rect.height, HEIGHT-self.rect.height, \
			coord_random_length))
		
		return x_random, y_random


	def game_coords(self):

		coord_random_length = 1000 # how many ways to breakup the x, y length
		min_y_spawn = 2 * (FENCE_DRAW_Y + ENTITY_H) # this is the min y that ghosts can spawn on L, R

		# randomize left, right, or bottom (i.e., where they spawn)
		spawn_from_where = np.random.choice(np.array(['left','right','bottom']))

		if spawn_from_where == 'left':
			x_random = 0.
			y_random = np.random.choice(np.linspace(min_y_spawn, WIDTH-self.rect.width, coord_random_length))

		elif spawn_from_where == 'right':
			x_random = WIDTH-self.rect.width
			y_random = np.random.choice(np.linspace(min_y_spawn, WIDTH-self.rect.height, coord_random_length))

		elif spawn_from_where == 'bottom':
			x_random = np.random.choice(np.linspace(0, HEIGHT-self.rect.height, coord_random_length))
			y_random = HEIGHT-self.rect.height

		return x_random, y_random
	
	def menu_move(self):
		if self.spawn_side == 'left':
			if self.rect.x > WIDTH:
				self.kill()
			self.rect.x += 5
		elif self.spawn_side == 'right':
			if self.rect.x < 0-self.rect.width:
				self.kill()
			self.rect.x -= 5


	def move(self):

		# get the difference vector between current ghost and middle of screen
		diff = np.array([WIDTH/2 - self.rect.x, HEIGHT/2 - self.rect.y])
		diff = np.array([self.player.rect.x - self.rect.x, self.player.rect.y - self.rect.y])

		# magnitude of difference vector
		diff_mag = np.linalg.norm(diff)

		if diff_mag < 1:
			diff_mag = 0.5

		# get the new x, y coordinates
		self.rect.x = self.rect.x + 1.5*diff[0]/diff_mag
		self.rect.y = self.rect.y + 1.5*diff[1]/diff_mag

	def update(self):
		if self.menu:
			self.menu_move()
		else:
			self.move()


#####################################################################################################
# Wave class
#####################################################################################################
class Wave():

	'''
	This class is responsible for the wave details. Waves only increase, without an upper bound.
	'''
	
	def __init__(self, enemy):
		self.wave_num = 1
		self.score = 0
		self.enemy = enemy
	
	def render(self):
		# draw the wave number in top right
		WAVE_TEXT = ALL_FONT.render("WAVE " + str(self.wave_num), 1, BLACK)
		WIN.blit(WAVE_TEXT, (WIDTH-WAVE_TEXT.get_width() - 10, 10))
		# draw the ghost_killed tab in the top right 
		GHOSTS_KILLED_TEXT = ALL_FONT.render("SCORE " + str(self.score), 1, BLACK)
		WIN.blit(GHOSTS_KILLED_TEXT, (WIDTH-GHOSTS_KILLED_TEXT.get_width() - 10, WAVE_TEXT.get_height()+10))	

	def advance(self):

		if self.score > self.wave_num * 5:
			self.wave_num += 1
			self.enemy = pg.sprite.Group()
		return self.enemy

	def update(self):
		self.render()
		return self.advance()


#####################################################################################################
# Tree class
#####################################################################################################
class Tree(pg.sprite.Sprite):

	'''
	This class is responsible for the tree sprite. Each tree is an instance of this class.
	'''
	
	def __init__(self):
		super().__init__()
		self.image = pg.transform.scale(pg.image.load('images/tree.png'), (1.5*ENTITY_W, 1.5*ENTITY_H))
		self.rect = self.image.get_rect()
		self.spawn_coords()
	
	def spawn_coords(self):
		
		self.rect.x, self.rect.y = 500, 500
	


