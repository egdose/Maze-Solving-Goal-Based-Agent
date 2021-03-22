import sys
import numpy as np

class Maze:
	class Node:
		def __init__(self, position):
			self.Adjacents = [None, None, None, None]
			self.Position = position
			self.cost = [0, 0, 0, 0]



	def __init__(self, dimensions)

	self.width = dimensions[0]
	self.height = dimensions[1]


def main():
	#Checking command-line arguments
	cmd_arguments = len(sys.argv)
	if cmd_arguments < 2:
		print("Maze size not defined... Taking 12x12")
		maze_dimensions = [12, 12]
	elif cmd_arguments > 2:
		print("Invalid number of arguments")
		print("Usage: python3 main.py <maze_size>")
		print("Example: python3 main.py 12")
	else:
		try:
			maze_dimensions[0] = int(sys.argv[1])
			maze_dimensions[1] = int(sys.argv[1])
		except Exception as e:
			print("Invalid Arguments")
			print("Usage: python3 main.py <maze_size>")
			print("Example: python3 main.py 12")


	#Initializing Maze
	maze_dimensions = [0, 0]

	grid = np.zeros([maze_dimensions[0], maze_dimensions[1]],
					dtype = bool)

	print("Hello World")


if __name__ == '__main__':
	main()