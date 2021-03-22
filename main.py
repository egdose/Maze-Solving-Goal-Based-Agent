import sys
import numpy as np
import pandas as pd

class Maze:
	class Node:
		def __init__(self, y, x):
			self.Adjacents = [None, None, None, None]
			self.x = x
			self.y = y
			self.cost = [0, 0, 0, 0]



	def __init__(self, dimensions):
		self.width = dimensions[0]
		self.height = dimensions[1]

		self.count = 0

		self.start_node = None
		self.end_node = None

		#Hard Coding in Start Node and End Node
		self.start_node = Maze.Node(4, 11)
		self.end_node = Maze.Node(10, 0)
		self.count += 2

		#Reading Data From input.csv
		df = None

		print("Reading maze data from input.csv")
		try:
			df = pd.read_csv('input.csv', header=None)
		except Exception as e:
			print("Failed to read input.csv, Make sure the folder has input.csv with it.")
			print("input.csv should be included in the submission")
			sys.exit()

		self.grid = df.to_numpy().astype('bool')

		if self.grid.shape != (self.width, self.height):
			print("Input file(rows, columns) mismatched the dimensions provided in command-line")
			sys.exit()

		#Temporary Printing For Debugging
		print("Nodes Should be like these: ")
		print("1, 1")
		print("1, 3")
		print("1, 5")
		print("1, 10")
		print("2, 1")
		print("3, 5")
		print("3, 8")
		print("4, 1")
		print("4, 3")
		print("4, 4")
		print("4, 10")
		print("4, 11")
		print("5, 6")
		print("6, 1")
		print("6, 2")
		print("8, 1")
		print("8, 2")
		print("8, 4")
		print("8, 6")
		print("8, 8")
		print("10, 0")
		print("10, 6")
		print("10, 8")
		print("10, 10")

		#Now Making Graph from the Provided Grid
		temp_top = self.width*[None]

		for y in range(1, self.height-1):
			#Some variables for parsing
			left_node = None
			new_node = None
			prv = False
			cur = self.grid[y, 0]
			nxt = self.grid[y, 1]

			for x in range(self.width):
				left_node = None
				new_node = None

				#Edge Case for End Node
				if x == 0 and cur == True:
					if end_node == None:
						end_node = Maze.Node(y, x)
						left_node = end_node
						new_node = None




def main():
	maze_dimensions = [0, 0]
	#Checking command-line arguments
	cmd_arguments = len(sys.argv)
	if cmd_arguments < 2:
		print("Maze size not defined... Taking 12x12")
		maze_dimensions = [12, 12]
	elif cmd_arguments > 2:
		print("Invalid number of arguments")
		print("Usage: python3 main.py <maze_size>")
		print("Example: python3 main.py 12")
		sys.exit()
	else:
		try:
			maze_dimensions[0] = int(sys.argv[1])
			maze_dimensions[1] = int(sys.argv[1])
		except Exception as e:
			print("Invalid Arguments")
			print("Usage: python3 main.py <maze_size>")
			print("Example: python3 main.py 12")
			sys.exit()


	#Initializing Maze
	maze = Maze(maze_dimensions)


if __name__ == '__main__':
	main()