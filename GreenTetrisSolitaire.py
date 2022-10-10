import arcade
"""
The License for the Python Arcade Library used in this project is as follows:
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

#UPGRADED AND CUSTOMIZED FROM THE TETRIS TEMPLATE FROM ARCADE ACADEMY
"""
# Copyright (c) 2021 NoahTheCorgi @Github
What was newly implemented from the default template:
# color is now green only :D
# scoring system
# horizontal acceleration by pressing longer left or right --> faster
# longpress horizontal capability --> much faster
# vertical acceleration by pressing down --> faster
# longpress vertical capabilitiy --> much faster
# next block type preview implemented
# window size change scaling implemented
# smooth sliding and control of blocks
# difficulty level
# controlled randomization of block types based on the level,,,
# controlled speed based on levels,,,
# e.g. scoring system updated to value tetris 4 lines the most
# color changes as difficulty goes up,,,
# difficulty level,,, <-- various things to make difficulty level different,,,
# artistic and beauty improvements
# Starting Screen with Explanation
# Ending Screen with Data Analysis each on how many blocks to each level as well as the total score
# start page UI and font improvements, better for the theme
# end page UI and font improvements, better for the theme
# improve and innovate scoring system for more variation
# pause functionality
# (not yet) interesting sound effects, whenever there is a collision or, row complete. or tetris!,,,
# ... ...
"""
import TetrisLevelAI
import random
import PIL #Alternative is Pillow, which forked PIL
#import random

################################################################################
##############INITIAL-SETTING-BEFORE-WINDOW RESIZE##############################
ROW_COUNT = 24
COLUMN_COUNT = 10
################################################################################

CellWidth = 30
CellHeight = 30

CellMARGIN = 5

Width = (CellWidth + CellMARGIN) * COLUMN_COUNT + CellMARGIN
Height = (CellHeight + CellMARGIN) * ROW_COUNT + CellMARGIN
################################################################################
################################################################################


SCREEN_TITLE = "GreenTetrisSolitaire: Check Your Performance!!!"

# Define the shapes of the single parts
tetris_shapes = [
	[[1, 1, 1],
	 [0, 1, 0]],

	[[0, 2, 2],
	 [2, 2, 0]],

	[[3, 3, 0],
	 [0, 3, 3]],

	[[4, 0, 0],
	 [4, 4, 4]],

	[[0, 0, 5],
	 [5, 5, 5]],

	[[6, 6, 6, 6]],

	[[7, 7],
	 [7, 7]]
]


def rotate_clockwise(shape):
	""" Rotates a matrix clockwise """
	return [[shape[y][x] for y in range(len(shape) -1, -1, -1)] for x in range(len(shape[0]))]

def rotate_counterclockwise(shape):
	""" Rotates a matrix clockwise """
	return [[shape[y][x] for y in range(len(shape))] for x in range(len(shape[0]) - 1, -1, -1)]


def check_collision(board, shape, offset):
	"""
	See if the matrix stored in the shape will intersect anything
	on the board based on the offset. Offset is an (x, y) coordinate.
	"""
	off_x, off_y = offset
	for cy, row in enumerate(shape):
		for cx, cell in enumerate(row):
			if cell and board[cy + off_y][cx + off_x]:
				return True
	return False


def remove_row(board, row):
	""" Remove a row from the board, add a blank row on top. """
	del board[row]
	return [[0 for _ in range(COLUMN_COUNT)]] + board


def join_matrixes(matrix_1, matrix_2, matrix_2_offset):
	""" Copy matrix 2 onto matrix 1 based on the passed in x, y offset coordinate """
	offset_x, offset_y = matrix_2_offset
	for cy, row in enumerate(matrix_2):
		for cx, val in enumerate(row):
			matrix_1[cy + offset_y - 1][cx + offset_x] += val
	return matrix_1


def new_board():
	""" Create a grid of 0's. Add 1's to the bottom for easier collision detection. """
	# Create the main board of 0's
	board = [[0 for _x in range(COLUMN_COUNT)] for _y in range(ROW_COUNT)]
	# Add a bottom border of 1's
	board += [[1 for _x in range(COLUMN_COUNT)]]
	return board


################################################################################
################################################################################
'''
def create_textures():
	""" Create a list of images for sprites based on the global self.colors. """
	new_textures = []
	for color in self.colors:
		# noinspection PyUnresolvedReferences
		image = PIL.Image.new('RGB', (CellWidth, CellHeight), color)
		new_textures.append(arcade.Texture(str(color), image=image))
	return new_textures
'''
################################################################################
################################################################################


class MyGame(arcade.Window):
	""" Main application class. """

	def __init__(self, width, height, title):
		""" Set up the application. """

		super().__init__(width, height, title, resizable=True)

		self.count4animate = 0

		##########################################################################
		# [[time it took to get to level i, # of blocks it took to reach level i]]
		self.data = [[0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0]]
		#self.time_counter = 0
		self.number_of_blocks_counter = 0
		##########################################################################

		self.three_UI_pages = 1

		self.level = 1

		self.colors = [
				  (0,  0,   0),
				  (10, 255, 70),
				  (20, 255, 60),
				  (30, 255, 50),
				  (40, 255, 40),
				  (50, 255, 30),
				  (60, 255, 20),
				  (70, 255, 10)
				  ]

		self.MARGIN = None

		self.SCORE = None

		########################################################################
		########################################################################

		arcade.set_background_color((0,255,0))

		self.board = None
		self.frame_count = 0
		self.game_over = False
		self.paused = False
		self.board_sprite_list = None

		self.current_and_next_stone_index = None #[index of current stone, index of next stone]
		self.stone = None
		self.stone_x = 0
		self.stone_y = 0

		self.next_stone = None

		#variable to keep track of how long down key has been pressed for,,,
		self.v = 0 #figure out why the variable needs to be referred to like this,,,
		#it must have to do with how classes refer to variables in python compilation,,,
		self.v_assist = 0

		self.m = 0
		self.move_assist = 0

		#SOUNDS
		self.gamestartsound = arcade.load_sound("gamestartsound.wav")
		self.collisionsound = arcade.load_sound("collisionsound.wav")
		self.rowclearsound = arcade.load_sound("rowclearsound.wav")
		self.tetrisclearsound = arcade.load_sound("tetrisclearsound.wav")
		self.rotatesound = arcade.load_sound("rotatesound.wav")
		self.levelupsound = arcade.load_sound("levelupsound.wav")
		self.gameoversound = arcade.load_sound("gameoversound.wav")


	def on_resize(self, width, height):
		""" This method is automatically called when the window is resized. """

		# Call the parent. Failing to do this will mess up the coordinates, and
		# default to 0,0 at the center and thE edges being -1 to 1.
		'''
		if self.width < 300:
			self.width = 300
		if self.height < 300:
			self.height = 800
		'''

		super().on_resize(width, height)


	def new_stone(self):
		"""
		Generate a new stone/block using TetrisLevelAI class...
		"""
		self.number_of_blocks_counter +=1
		#this creates an instance of the TetrisLevelAI and then chooses the Next Block from "tetris_shapes"
		self.current_and_next_stone_index[0] = self.current_and_next_stone_index[1]
		self.current_and_next_stone_index[1] = TetrisLevelAI.TetrisLevelAI(self.board, self.level).chooseNextBlock()
		return tetris_shapes[self.current_and_next_stone_index[1]]

	def cellHeight(self):
		return (self.height - self.MARGIN)/(ROW_COUNT) - self.MARGIN

	def cellWidth(self):
		return self.cellHeight()


	def create_textures(self):
		""" Create a list of images for sprites based on the global self.colors. """
		new_textures = []
		for color in self.colors:
			image = PIL.Image.new('RGB', (int(self.cellWidth()), int(self.cellHeight())), color)
			new_textures.append(arcade.Texture(str(color), image=image))
		return new_textures


	def setup(self):

		arcade.play_sound(self.gamestartsound)

		self.level = 1
		self.SCORE = 0

		self.MARGIN = 5

		texture_list = self.create_textures()

		########################################################################
		########################################################################
		#self.height <-- notice that this is built in
		#self.cellHeight() = (self.height - self.MARGIN)/(COLUMN_COUNT) - self.MARGIN
		#self.cellWidth() = self.cellHeight()

		#self.width = (CellWidth + self.MARGIN) * COLUMN_COUNT + self.MARGIN
		#self.height = (CellHeight + self.MARGIN) * ROW_COUNT + self.MARGIN
		########################################################################
		########################################################################

		self.board = new_board()

		self.board_sprite_list = arcade.SpriteList()
		for row in range(len(self.board)):

			for column in range(len(self.board[0])):
				sprite = arcade.Sprite()

				for texture in texture_list:
					sprite.append_texture(texture)
				sprite.set_texture(0)
				sprite.center_x = (self.MARGIN + self.cellWidth()) * column + self.MARGIN + self.cellWidth() // 2
				sprite.center_y = self.height - (self.MARGIN + self.cellHeight()) * row + self.MARGIN + self.cellHeight() // 2

				self.board_sprite_list.append(sprite)

		#######

		#the first element is the "current" the second index is the "next stone"
		#self.current_and_next_stone_index = [current stone index, next stone index]
		self.current_and_next_stone_index = [random.randint(0,6), random.randint(0,6)]

		self.stone = tetris_shapes[self.current_and_next_stone_index[0]]
		self.stone_x = int(COLUMN_COUNT / 2 - len(self.stone[0]) / 2)
		self.stone_y = 0
		#######

		self.next_stone = tetris_shapes[self.current_and_next_stone_index[1]]

		self.update_board()


	def drop(self):
		"""
		Drop the stone down one place.
		Check for collision.
		If collided, then
		  join matrixes
		  Check for rows we can remove
		  Update sprite list with stones
		  Create a new stone
		"""

		if not self.game_over and not self.paused:
			self.stone_y += 1


			if check_collision(self.board, self.stone, (self.stone_x, self.stone_y)):
				arcade.play_sound(self.collisionsound)
				###########################
				if self.stone_y <= 1:
					self.game_over = True
				###########################

				self.v_assist = 0
				self.move_assist = 0
				self.board = join_matrixes(self.board, self.stone, (self.stone_x, self.stone_y))

				soundvariable = 0 #keeps track of if sound is played so that multiple sounds don't play too much
				while True:
					for i, row in enumerate(self.board[:-1]):
						if 0 not in row:
							self.board = remove_row(self.board, i)

							####################################################
							####################################################
							##########``sophisticated'' scoring system##########
							""" Block Index: Tetris Block General Difficulty Ranking:
							in other words, for now...
							self.boardevaluation.append(0) #the T block #the "easiest" block
							self.boardevaluation.append(5) #the I block
							self.boardevaluation.append(6) #the square block
							self.boardevaluation.append(3) #the J block
							self.boardevaluation.append(4) #the L block
							self.boardevaluation.append(2) #the Z block
							self.boardevaluation.append(1) #the S block #most difficult block
							"""
							if i % 4 == 0: #case of "tetris"
								self.SCORE += 200
								self.rotatesound.set_volume(0.5, arcade.play_sound(self.tetrisclearsound))

							if self.current_and_next_stone_index[0] == 0:
								self.SCORE += 23
								if soundvariable == 0:
									self.rotatesound.set_volume(0.5, arcade.play_sound(self.rowclearsound))
									soundvariable+=1
							elif self.current_and_next_stone_index[0] == 5:
								self.SCORE += 33
								if soundvariable == 0:
									self.rotatesound.set_volume(0.5, arcade.play_sound(self.rowclearsound))
									soundvariable+=1
							elif self.current_and_next_stone_index[0] == 6:
								self.SCORE += 43
								if soundvariable == 0:
									self.rotatesound.set_volume(0.5, arcade.play_sound(self.rowclearsound))
									soundvariable+=1
							elif self.current_and_next_stone_index[0] == 3:
								self.SCORE += 63
								if soundvariable == 0:
									self.rotatesound.set_volume(0.5, arcade.play_sound(self.rowclearsound))
									soundvariable+=1
							elif self.current_and_next_stone_index[0] == 4:
								self.SCORE += 73
								if soundvariable == 0:
									self.rotatesound.set_volume(0.5, arcade.play_sound(self.rowclearsound))
									soundvariable+=1
							elif self.current_and_next_stone_index[0] == 2:
								self.SCORE += 93
								if soundvariable == 0:
									self.rotatesound.set_volume(0.5, arcade.play_sound(self.rowclearsound))
									soundvariable+=1
							elif self.current_and_next_stone_index[0] == 1:
								self.SCORE += 103
								if soundvariable == 0:
									self.rotatesound.set_volume(0.5, arcade.play_sound(self.rowclearsound))
									soundvariable+=1
							####################################################
							####################################################
							####################################################

							if self.SCORE < 1000:
								pass #level already set at 1

							elif self.SCORE in range(1000, 2000) and self.level == 1:
								arcade.play_sound(self.levelupsound)
								self.level = 2#

								self.data[0][1] = self.number_of_blocks_counter
								self.number_of_blocks_counter =0
								arcade.set_background_color((100,255,0))

							elif self.SCORE in range(2000, 3000) and self.level == 2:
								arcade.play_sound(self.levelupsound)
								self.level = 3

								self.data[1][1] = self.number_of_blocks_counter
								self.number_of_blocks_counter =0
								arcade.set_background_color((200,255, 0))

							elif self.SCORE in range(3000, 4000) and self.level == 3:
								arcade.play_sound(self.levelupsound)
								self.level = 4

								self.data[2][1] = self.number_of_blocks_counter

								self.number_of_blocks_counter =0
								arcade.set_background_color((150,255,50))
								self.colors = [
										  (0,  0,   0),
										  (0, 0,  255),
										  (20,  120, 255),
										  (40,  100,  255),
										  (60, 80, 255),
										  (80, 60, 255),
										  (100, 40, 255),
										  (120, 20, 255)
										  ]

							elif self.SCORE in range(4000, 5000) and self.level ==4:
								arcade.play_sound(self.levelupsound)
								self.level = 5

								self.data[3][1] = self.number_of_blocks_counter

								self.number_of_blocks_counter =0
								arcade.set_background_color((100,255,100))


							elif self.SCORE in range(5000, 7000) and self.level ==5:
								arcade.play_sound(self.levelupsound)
								self.data[4][1] = self.number_of_blocks_counter

								self.number_of_blocks_counter =0
								self.level = 6
								arcade.set_background_color((100,255,150))


							elif self.SCORE in range(7000, 10000) and self.level ==6:
								arcade.play_sound(self.levelupsound)
								self.level = 7

								self.data[5][1] = self.number_of_blocks_counter

								self.number_of_blocks_counter =0
								arcade.set_background_color((100,255,200))
								self.colors = [
										  (0,  0,   0),
										  (255, 0,  120),
										  (255,  20, 100),
										  (255,  40,  80),
										  (255, 60, 60),
										  (255, 80, 40),
										  (255, 100, 20),
										  (255, 120, 0)
										  ]

							elif self.SCORE >= 10000 and self.level == 7:
								arcade.play_sound(self.levelupsound)
								self.level = 8 #this level is called "infinity"

								self.data[6][1] = self.number_of_blocks_counter

								self.number_of_blocks_counter =0
								arcade.set_background_color((200,255,200))
								self.colors = [
										  (0,  0,   0),
										  (0, 0,  255),
										  (210,  45, 255),
										  (165,  90,  255),
										  (120, 135, 255),
										  (75, 180, 255),
										  (30, 225, 255),
										  (0, 255, 255)
										  ]
							break
					else:
						break

				#######
				self.stone = self.next_stone
				self.stone_x = int(COLUMN_COUNT / 2 - len(self.stone[0]) / 2)
				self.stone_y = 0
				#######

				#######
				self.next_stone = self.new_stone()
				#######


	def rotate_stone(self):
		""" Rotate the stone, check collision. """
		if not self.game_over and not self.paused:
			new_stone = rotate_clockwise(self.stone)
			if self.stone_x + len(new_stone[0]) >= COLUMN_COUNT:
				self.stone_x = COLUMN_COUNT - len(new_stone[0])
			if not check_collision(self.board, new_stone, (self.stone_x, self.stone_y)):
				self.stone = new_stone

	def check_game_over(self):
		pass

	def on_update(self, dt):
		""" Update, drop stone if warrented """

		###################################################################################
		#this part of the code updates self.count4animate every update to use for animation
		if self.count4animate < 100:
			self.count4animate +=1;
		else: # self.count4animate == 100
			self.count4animate = 0
		###################################################################################

		if self.paused == False:
			if self.game_over == True and self.three_UI_pages == 2:
				self.three_UI_pages += 1
				arcade.play_sound(self.gameoversound)

			if self.three_UI_pages == 1:
				pass

			elif self.three_UI_pages == 2:
				self.frame_count += 1

				self.update_board()

				################################################################
				########_drop speed control based on level and key press_#######
				################################################################
				if self.v <= 0:
					if self.frame_count % (18-2*self.level) == 0:
						self.drop()

				elif self.v > 0:
					if self.v <= 10: #the upper bound is the down key pressed buffer
						if self.frame_count % 10 == 0:
							self.drop()
					else:
						self.drop()

				if self.v_assist == 0:
					self.v = 0
				elif self.v_assist == 1:
					self.v+=1

				######################################################################
				if self.m >10:#the bound is the buffer for right key pressed
					self.move(1)
				elif self.m <-10:#the bound is the buffer for left key pressed
					self.move(-1)

				if self.move_assist ==0:
					self.m = 0
				elif self.move_assist ==1:
					self.m +=1
				elif self.move_assist == -1:
					self.m -=1

			elif self.three_UI_pages == 3: #if self.three_UI_pages = 3
				pass

	def move(self, delta_x):
		""" Move the stone back and forth based on delta x. """
		if not self.game_over and not self.paused:

			'''
			if self.m <2:
				new_x = self.stone_x + delta_x
			elif self.m >=2:
				new_x = self.stone_x + *delta_x
			'''
			new_x = self.stone_x + delta_x

			if new_x < 0:
				new_x = 0
			if new_x > COLUMN_COUNT - len(self.stone[0]):
				new_x = COLUMN_COUNT - len(self.stone[0])
			if not check_collision(self.board, self.stone, (new_x, self.stone_y)):
				self.stone_x = new_x

	def on_key_press(self, key, modifiers):
		"""
		Handle user key presses
		User goes left, move -1
		User goes right, move 1
		Rotate stone,
		or drop down
		"""
		if key == arcade.key.ENTER:
			if self.three_UI_pages == 1:
				self.three_UI_pages +=1
			arcade.play_sound(self.gamestartsound)

		if key == arcade.key.P:
			if self.paused == True:
				self.paused = False
			else:
				self.paused = True
			arcade.play_sound(self.gamestartsound)

		elif key == arcade.key.LEFT:
			self.move_assist = -1
			self.move(-1)
		elif key == arcade.key.RIGHT:
			self.move_assist = 1
			self.move(1)
		elif key == arcade.key.SPACE:
			self.rotate_stone()
			#arcade.Sound.set_volume(0.5, arcade.play_sound(self.rotatesound))
			self.rotatesound.set_volume(1, arcade.play_sound(self.rotatesound))
		elif key == arcade.key.DOWN:
			self.drop()
			self.v_assist = 1
		elif key == arcade.key.ESCAPE:
			if self.three_UI_pages == 1 or self.three_UI_pages == 3:
				self.close()
			else: #if self.three_UI_pages ==2
				self.three_UI_pages = 3
	def on_key_release(self, key, modifiers):
		if key == arcade.key.DOWN:
			self.v_assist = 0
		if key == arcade.key.LEFT or key == arcade.key.RIGHT:
			self.move_assist = 0

	def draw_grid(self, grid, offset_x, offset_y):
		"""
		Draw the grid. Used to draw the falling stones. The board is drawn
		by the sprite list.
		"""
		# Draw the grid
		for row in range(len(grid)):
			for column in range(len(grid[0])):
				# Figure out what color to draw the box
				if grid[row][column]:
					color = self.colors[grid[row][column]]
					# Do the math to figure out where the box is
					x = (self.MARGIN + self.cellWidth()) * (column + offset_x) + self.MARGIN + self.cellWidth() // 2
					y = self.height - (self.MARGIN + self.cellHeight()) * (row + offset_y) + self.MARGIN + self.cellHeight() // 2

					arcade.draw_rectangle_filled(x, y, self.cellWidth(), self.cellHeight(), color)


	def draw_next(self, Stoneee):
		for i in range(len(Stoneee)):
			for j in range(len(Stoneee[i])):
				color = self.colors[Stoneee[i][j]]
				x = (self.MARGIN + self.cellWidth()) * (j) + self.MARGIN + (self.cellWidth()//2)
				y = self.height - (self.MARGIN + self.cellHeight()) * (i+1) + self.MARGIN + (self.cellHeight()//2)
				arcade.draw_rectangle_filled(x, y, self.cellWidth(), self.cellHeight(), color)


	def update_board(self):
		"""
		Update the sprite list to reflect the contents of the 2d grid
		"""
		for row in range(len(self.board)):
			for column in range(len(self.board[0])):
				v = self.board[row][column]
				i = row * COLUMN_COUNT + column

				self.board_sprite_list[i].scale = self.height/Height
				self.board_sprite_list[i].center_x = (self.MARGIN + self.cellWidth()) * column + self.MARGIN + self.cellWidth() // 2
				self.board_sprite_list[i].center_y = self.height - (self.MARGIN + self.cellHeight()) * row + self.MARGIN + self.cellHeight() // 2

				if self.game_over == False:
					self.board_sprite_list[i].set_texture(v)


	def on_draw(self):
		""" Render the screen. """

		# This command has to happen before we start drawing
		arcade.start_render()

		if self.three_UI_pages == 1:
			#draw current level and other stuff you can add
			s = 12
			arcade.draw_text("Welcome to GreenTetrisSolitaire! XD", 30, self.height/1.25, arcade.color.BLACK, s, font_name="Kenney Pixel Square")
			arcade.draw_text("All Blocks Turn Green! Try to beat your best scores! XD", 30, self.height/1.25 - 2*s, arcade.color.BLACK, s, font_name="Kenney Pixel Square")
			arcade.draw_text("At the end, you will see your Performance Summary :D", 30, self.height/1.25 - 4*s, arcade.color.BLACK, s, font_name="Kenney Pixel Square")

			arcade.draw_text(" ", 30, self.height/1.25 - 6*s, arcade.color.BLACK, s, font_name="Kenney Pixel Square")

			arcade.draw_text("Left and Right Keys (Short Press): Horizontal Movement", 30, self.height/1.25 - 8*s, arcade.color.BLACK, s, font_name="Kenney Pixel Square")
			arcade.draw_text("Left and Right Keys (Long Press): Horizontal Accelration", 30, self.height/1.25 - 10*s, arcade.color.BLACK, s, font_name="Kenney Pixel Square")
			arcade.draw_text("Down Key (Short press): Jump Vertically", 30, self.height/1.25 - 12*s, arcade.color.BLACK, s, font_name="Kenney Pixel Square")
			arcade.draw_text("Down Key (Long press): Acceleration Vertically", 30, self.height/1.25 - 14*s, arcade.color.BLACK, s, font_name="Kenney Pixel Square")
			arcade.draw_text("P: To Pause and Unpause", 30, self.height/1.25 - 16*s, arcade.color.BLACK, s, font_name="Kenney Pixel Square")

			arcade.draw_text(" ", 30, self.height/1.25 - 18*s, arcade.color.BLACK, s, font_name="Kenney Pixel Square")

			arcade.draw_text("See you at Level INFINITY! :)", 30, self.height/1.25 - 20*s, arcade.color.BLACK, s, font_name="Kenney Pixel Square")

			arcade.draw_text(" ", 30, self.height/1.25 - 22*s, arcade.color.BLACK, s, font_name="Kenney Pixel Square")

			if self.count4animate <50: #simple blinking animation of "Enter"
				arcade.draw_text("Press ENTER to continue ..", 90, self.height/1.25 - 32*s, arcade.color.BLACK, 20, font_name="Kenney Pixel Square")
			else:
				arcade.draw_text("Press                to continue .", 90, self.height/1.25 - 32*s, arcade.color.BLACK, 20, font_name="Kenney Pixel Square")

		elif self.three_UI_pages == 2:
			#####################this is what needs to get updated##################
			self.board_sprite_list.draw()

			self.draw_grid(self.stone, self.stone_x, self.stone_y)

			#draw the black area for the upcoming next stone shown
			arcade.draw_rectangle_filled(2*(self.cellWidth() + self.MARGIN), self.height
				- (self.cellHeight() + self.MARGIN) + self.MARGIN, 4*(self.cellWidth()+self.MARGIN), 2*(self.cellHeight() + self.MARGIN)
					, (0,0,0))

			#draw the white area for the level and self.SCORE details
			arcade.draw_rectangle_filled(self.width - (1.5)*(self.cellWidth() + self.MARGIN),
				self.height - (self.cellHeight() + self.MARGIN) + self.MARGIN, 3*(self.cellWidth()+self.MARGIN)
					, 2*(self.cellHeight() + self.MARGIN), (30,255,30))

			#draw current level and other stuff you can add
			if self.level < 8:
				arcade.draw_text("Level: " + str(self.level), self.width - (3)*(self.cellWidth() + self.MARGIN), self.height - (self.cellHeight() + self.MARGIN) + 2*self.MARGIN, arcade.color.BLACK, 12, font_name="Kenney Pixel Square")
			else: #self.level = 8
				arcade.draw_text("Level: INFINITY!!!", self.width - (3)*(self.cellWidth() + self.MARGIN), self.height - (self.cellHeight() + self.MARGIN) + 2*self.MARGIN, arcade.color.BLACK, 12, font_name="Kenney Pixel Square")
			#draw self.SCORE
			arcade.draw_text("Score: " + str(self.SCORE), self.width - (3)*(self.cellWidth() + self.MARGIN), self.height - (self.cellHeight() + self.MARGIN) - 2*self.MARGIN, arcade.color.BLACK, 12, font_name="Kenney Pixel Square")

			#preview of the next stone that will be coming
			self.draw_next(self.next_stone)

		else: #self.three_UI_pages == 3: #THIS IS THE CASE WHEN GAME IS OVER,,,
			s = 10
			arcade.draw_text("Thank You for Playing GreenTetrisSolitaire!", 30, self.height/1.25, arcade.color.BLACK, s, font_name="Kenney Pixel Square")
			arcade.draw_text("All Blocks Turn Green!", 30, self.height/1.25 - 2*s, arcade.color.BLACK, s, font_name="Kenney Pixel Square")
			arcade.draw_text("The following is your Performance Summary :D", 30, self.height/1.25 - 4*s, arcade.color.BLACK, s, font_name="Kenney Pixel Square")

			if self.count4animate <50:
				arcade.draw_text(" ", 30, self.height/1.25 - 6*s, arcade.color.BLACK, s, font_name="Kenney Pixel Square")
				arcade.draw_text("Your Total Score Was: " + str(self.SCORE), 30, self.height/1.25 - 8*s, arcade.color.BLACK, s, font_name="Kenney Pixel Square")
				arcade.draw_text(" ", 30, self.height/1.25 - 10*s, arcade.color.BLACK, s, font_name="Kenney Pixel Square")
				arcade.draw_text("       The number of blocks it took for you to reach level 2: " + str(self.data[0][1]-1), 30, self.height/1.25 - 14*s, arcade.color.BLACK, s, font_name="Kenney Pixel Square")
				arcade.draw_text(" ", 30, self.height/1.25 - 16*s, arcade.color.BLACK, s, font_name="Kenney Pixel Square")
				arcade.draw_text("       The number of blocks it took for you to reach level 3: " + str(self.data[1][1]), 30, self.height/1.25 - 20*s, arcade.color.BLACK, s, font_name="Kenney Pixel Square")
				arcade.draw_text(" ", 30, self.height/1.25 - 22*s, arcade.color.BLACK, s, font_name="Kenney Pixel Square")
				arcade.draw_text("       The number of blocks it took for you to reach level 4: " + str(self.data[2][1]), 30, self.height/1.25 - 26*s, arcade.color.BLACK, s, font_name="Kenney Pixel Square")
				arcade.draw_text(" ", 30, self.height/1.25 - 28*s, arcade.color.BLACK, s, font_name="Kenney Pixel Square")
				arcade.draw_text("       The number of blocks it took for you to reach level 5: " + str(self.data[3][1]), 30, self.height/1.25 - 32*s, arcade.color.BLACK, s, font_name="Kenney Pixel Square")
				arcade.draw_text(" ", 30, self.height/1.25 - 34*s, arcade.color.BLACK, s, font_name="Kenney Pixel Square")
				arcade.draw_text("       The number of blocks it took for you to reach level 6: "+ str(self.data[4][1]), 30, self.height/1.25 - 38*s, arcade.color.BLACK, s, font_name="Kenney Pixel Square")
				arcade.draw_text(" ", 30, self.height/1.25 - 40*s, arcade.color.BLACK, s, font_name="Kenney Pixel Square")
				arcade.draw_text("       The number of blocks it took for you to reach level 7: "+ str(self.data[5][1]), 30, self.height/1.25 - 44*s, arcade.color.BLACK, s, font_name="Kenney Pixel Square")
				arcade.draw_text(" ", 30, self.height/1.25 - 46*s, arcade.color.BLACK, s, font_name="Kenney Pixel Square")
				arcade.draw_text("       The number of blocks it took for you to reach level INFINITY!: "+ str(self.data[6][1]), 30, self.height/1.25 - 50*s, arcade.color.BLACK, s, font_name="Kenney Pixel Square")
				arcade.draw_text(" ", 30, self.height/1.25 - 52*s, arcade.color.BLACK, s, font_name="Kenney Pixel Square")
				arcade.draw_text("See you at Level INFINITY! :)", 180, self.height/1.25 - 58*s, arcade.color.BLACK, s, font_name="Kenney Pixel Square")
			else:
				arcade.draw_text(" ", 30, self.height/1.25 - 6*s, arcade.color.BLACK, s, font_name="Kenney Pixel Square")
				arcade.draw_text("Your Total Score Was: " , 30, self.height/1.25 - 8*s, arcade.color.BLACK, s, font_name="Kenney Pixel Square")
				arcade.draw_text(" ", 30, self.height/1.25 - 10*s, arcade.color.BLACK, s, font_name="Kenney Pixel Square")
				arcade.draw_text("       The number of blocks it took for you to reach level 2: " , 30, self.height/1.25 - 14*s, arcade.color.BLACK, s, font_name="Kenney Pixel Square")
				arcade.draw_text(" ", 30, self.height/1.25 - 16*s, arcade.color.BLACK, s, font_name="Kenney Pixel Square")
				arcade.draw_text("       The number of blocks it took for you to reach level 3: " , 30, self.height/1.25 - 20*s, arcade.color.BLACK, s, font_name="Kenney Pixel Square")
				arcade.draw_text(" ", 30, self.height/1.25 - 22*s, arcade.color.BLACK, s, font_name="Kenney Pixel Square")
				arcade.draw_text("       The number of blocks it took for you to reach level 4: " , 30, self.height/1.25 - 26*s, arcade.color.BLACK, s, font_name="Kenney Pixel Square")
				arcade.draw_text(" ", 30, self.height/1.25 - 28*s, arcade.color.BLACK, s, font_name="Kenney Pixel Square")
				arcade.draw_text("       The number of blocks it took for you to reach level 5: " , 30, self.height/1.25 - 32*s, arcade.color.BLACK, s, font_name="Kenney Pixel Square")
				arcade.draw_text(" ", 30, self.height/1.25 - 34*s, arcade.color.BLACK, s, font_name="Kenney Pixel Square")
				arcade.draw_text("       The number of blocks it took for you to reach level 6: ", 30, self.height/1.25 - 38*s, arcade.color.BLACK, s, font_name="Kenney Pixel Square")
				arcade.draw_text(" ", 30, self.height/1.25 - 40*s, arcade.color.BLACK, s, font_name="Kenney Pixel Square")
				arcade.draw_text("       The number of blocks it took for you to reach level 7: ", 30, self.height/1.25 - 44*s, arcade.color.BLACK, s, font_name="Kenney Pixel Square")
				arcade.draw_text(" ", 30, self.height/1.25 - 46*s, arcade.color.BLACK, s, font_name="Kenney Pixel Square")
				arcade.draw_text("       The number of blocks it took for you to reach level INFINITY!: ", 30, self.height/1.25 - 50*s, arcade.color.BLACK, s, font_name="Kenney Pixel Square")
				arcade.draw_text(" ", 30, self.height/1.25 - 52*s, arcade.color.BLACK, s, font_name="Kenney Pixel Square")
				arcade.draw_text("See you at Level INFINITY  :)", 180, self.height/1.25 - 58*s, arcade.color.BLACK, s, font_name="Kenney Pixel Square")


		if self.paused == True and self.three_UI_pages == 2:
			if self.count4animate <50:
				arcade.draw_text("Paused... Press P to continue ..", 30, self.height/1.25 - 260, arcade.color.WHITE, 23, font_name="Kenney Pixel Square", bold = False)
			else:
				arcade.draw_text("Paused... Press     to continue .", 30, self.height/1.25 - 260, arcade.color.WHITE, 23, font_name="Kenney Pixel Square", bold = False)



def main():
	""" Create the game window, setup, run """
	my_game = MyGame(Width + 280, Height + 71, SCREEN_TITLE)
	my_game.setup()
	############################################################################
	my_game.switch_to()
	############################################################################
	arcade.run()

if __name__ == "__main__":
	main()
