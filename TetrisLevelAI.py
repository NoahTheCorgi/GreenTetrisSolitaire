import random

# In order to use this Class, create an instance --> call fct chooseNextBlock --> use the return value
# --> it will return an index that corresponds to the block type in GreenTetrisSolitaire.py's "tetris_shapes"

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

#Possible Future Improvements #1: Implement evaluateBlock "innovatively",,,
#Possible Future Improvements #2: Update chooseNextBlock so that it is more "forgiving",,,

class TetrisLevelAI():
	
	"""this Class looks at the current tetris board and generates the next blocks
	accordingly to the level of the current player..."""

	def __init__(self, board, level):
		self.level = level
		self.board = board
		self.boardevaluation = None # this is a list of 7 possible blocks in hierarchy ordered lists

		#self.nextblock = None  # seven possible block shapes

	def evaluateBlock(self, block):
		""" Future task: """
		""" returns the scoring of the block based on the number of possibilities the block has to land nicely out of all the options"""
		""" the higher the value the more possibilities of good placements i.e. higher value --> "easier" block"""
		return 100

	def sort_on_eval(self, eval): #sorting 7 things.
		"""quick sorts the eval two dimensional list and sorts it based on the zero-th index"""
		"""earlier the index the more easier the block is to place"""
		sorted_eval = []
		for block in eval: #a block here is an list of the form [evaluation, block index]
			if len(sorted_eval) == 0:
				sorted_eval = [block]
			else:
				j=0 #position of the insert for the sorting
				for i in range(len(sorted_eval)):
					if sorted_eval[i][0] > block[0]:
						j = i + 1
					else:
						j = i
						break
				sorted_eval.insert(j, block)
		return sorted_eval

	def evaluateBoard(self): #update the boardevaluation and returns it

		"""update self.boardevaluation
		currently this code does not evaluate the board
		but uses a general tetris block ranking order for now,,,

		This AI Should go through each block and look at all possibility
		and then check which block has the most options to land nicely
		based on this rating, it should ranking each block"""

		eval = [[self.evaluateBlock(0)+10, 0], [self.evaluateBlock(5)+9, 5], [self.evaluateBlock(6)+8, 6], [self.evaluateBlock(3)+7, 3], [self.evaluateBlock(4)+6, 4], [self.evaluateBlock(2)+5, 2], [self.evaluateBlock(1)+4, 1]]

		eval = self.sort_on_eval(eval)

		self.boardevaluation = []
		self.boardevaluation.append(eval[0][1])
		self.boardevaluation.append(eval[1][1])
		self.boardevaluation.append(eval[2][1])
		self.boardevaluation.append(eval[3][1])
		self.boardevaluation.append(eval[4][1])
		self.boardevaluation.append(eval[5][1])
		self.boardevaluation.append(eval[6][1])

		return self.boardevaluation

	def chooseNextBlock(self):
		evaluation = self.evaluateBoard()
		chance_distribution = random.randint(1,100)
		if self.level == 1:

			if chance_distribution < 26: #26 percent
				return evaluation[0]
			elif chance_distribution <= 52: #26%
				return evaluation[1]
			elif chance_distribution <= 68: #16%
				return evaluation[2]
			elif chance_distribution <= 81: #13%
				return evaluation[3]
			elif chance_distribution <= 90: #9%
				return evaluation[4]
			elif chance_distribution <= 95: #5%
				return evaluation[5]
			elif chance_distribution <= 100: #5%
				return evaluation[6]


		elif self.level == 2:

			if chance_distribution <= 20: #20%
				return evaluation[0]
			elif chance_distribution <= 40: #20%
				return evaluation[1]
			elif chance_distribution <= 60: #20%
				return evaluation[2]
			elif chance_distribution <= 75: #15%
				return evaluation[3]
			elif chance_distribution <= 85: #10%
				return evaluation[4]
			elif chance_distribution <= 93: #8%
				return evaluation[5]
			elif chance_distribution <= 100: #7%
				return evaluation[6]


		elif self.level == 3:

			if chance_distribution <= 15: #15%
				return evaluation[0]
			elif chance_distribution <= 30: #15%
				return evaluation[1]
			elif chance_distribution <= 50: #20%
				return evaluation[2]
			elif chance_distribution <= 65: #15%
				return evaluation[3]
			elif chance_distribution <= 78: #13%
				return evaluation[4]
			elif chance_distribution <= 89: #11%
				return evaluation[5]
			elif chance_distribution <= 100: #11%
				return evaluation[6]


		elif self.level == 4:

			if chance_distribution <= 15: #10%
				return evaluation[0]
			elif chance_distribution <= 30: #15%
				return evaluation[1]
			elif chance_distribution <= 45: #15%
				return evaluation[2]
			elif chance_distribution <= 60: #15%
				return evaluation[3]
			elif chance_distribution <= 75: #15%
				return evaluation[4]
			elif chance_distribution <= 90: #15%
				return evaluation[5]
			elif chance_distribution <= 100: #15%
				return evaluation[6]


		elif self.level == 5:

			if chance_distribution <= 11: #11
				return evaluation[0]
			elif chance_distribution <= 22: #11
				return evaluation[1]
			elif chance_distribution <= 35: #13
				return evaluation[2]
			elif chance_distribution <= 50: #15
				return evaluation[3]
			elif chance_distribution <= 70: #20
				return evaluation[4]
			elif chance_distribution <= 85: #15
				return evaluation[5]
			elif chance_distribution <= 100: #15
				return evaluation[6]


		elif self.level == 6:

			if chance_distribution <= 7: #7
				return evaluation[0]
			elif chance_distribution <= 15: #8
				return evaluation[1]
			elif chance_distribution <= 25: #10
				return evaluation[2]
			elif chance_distribution <= 40: #15
				return evaluation[3]
			elif chance_distribution <= 60: #20
				return evaluation[4]
			elif chance_distribution <= 80: #20
				return evaluation[5]
			elif chance_distribution <= 100: #20
				return evaluation[6]


		elif self.level == 7:

			if chance_distribution <= 5: #5
				return evaluation[0]
			elif chance_distribution <= 10: #5
				return evaluation[1]
			elif chance_distribution <= 20: #10
				return evaluation[2]
			elif chance_distribution <= 35: #15
				return evaluation[3]
			elif chance_distribution <= 50: #15
				return evaluation[4]
			elif chance_distribution <= 75: #25
				return evaluation[5]
			elif chance_distribution <= 100: #25
				return evaluation[6]


		elif self.level == 8: #label this the "Final Boss"
		#this should be almost imposs so game ends with stats,,,

			if chance_distribution <= 5: #5
				return evaluation[0]
			elif chance_distribution <= 10: #5
				return evaluation[1]
			elif chance_distribution <= 19: #9
				return evaluation[2]
			elif chance_distribution <= 32: #13
				return evaluation[3]
			elif chance_distribution <= 48: #16
				return evaluation[4]
			elif chance_distribution <= 74: #26
				return evaluation[5]
			elif chance_distribution <= 100: #26
				return evaluation[6]
