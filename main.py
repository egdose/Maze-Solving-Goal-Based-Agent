import sys
import numpy as np
import pandas as pd
from PIL import Image

#Important Enum variables for Indexing
UP = 0
LEFT = 1
RIGHT = 2
DOWN = 3

class Maze:
	class Node:
		def __init__(self, y, x):
			self.Adjacents = [None, None, None, None]
			self.x = x
			self.y = y
			#self.cost = [0, 0, 0, 0]
			#print(f"New Node({self.x}, {self.y})")

		def print_info(self):
			if self.Adjacents[UP] != None:
				print(f"->Up ({self.Adjacents[UP].x}, {self.Adjacents[UP].y})")
			else:
				print(f"->Up (None)")
			if self.Adjacents[LEFT] != None:
				print(f"->Left ({self.Adjacents[LEFT].x}, {self.Adjacents[LEFT].y})")
			else:
				print(f"->Left (None)")
			if self.Adjacents[RIGHT] != None:
				print(f"->Right ({self.Adjacents[RIGHT].x}, {self.Adjacents[RIGHT].y})")
			else:
				print(f"->Right (None)")
			if self.Adjacents[DOWN] != None:
				print(f"->Down ({self.Adjacents[DOWN].x}, {self.Adjacents[DOWN].y})")
			else:
				print(f"->Down (None)")



	def __init__(self, dimensions):
		self.width = dimensions[0]
		self.height = dimensions[1]

		self.count = 0

		self.start_node = None
		self.end_node = None

		#Hard Coding in Start Node and End Node
		#self.start_node = Maze.Node(4, 11)
		#self.end_node = Maze.Node(10, 0)
		#self.count += 2

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

		#Now Making Graph from the Provided Grid
		temp_top = self.width*[None]

		for y in range(1, self.height-1):
			#Some variables for parsing
			left_node = None
			new_node = None
			prv = False
			cur = False
			nxt = False

			for x in range(self.width):
				prv = cur
				cur = self.grid[y, x]
				if x != self.width-1:
					nxt = self.grid[y, x+1]
				else:
					nxt = False

				new_node = None


				#Edge Case for End Node - MUST BE ON LEFT
				if x == 0 and cur == True:
					if self.end_node == None:
						self.end_node = Maze.Node(y, x)
						print(f"End Node Created at ({x}, {y})")
						self.count += 1
						left_node = self.end_node
						new_node = None #No Need for Top Buffer in End Node
						continue
				#Edge Case for Start Node - MUST BE ON RIGHT
				elif x == self.width-1 and cur == True:
					if self.start_node == None:
						self.start_node = Maze.Node(y, x)
						print(f"Start Node Created at ({x}, {y})")
						self.count += 1
						left_node.Adjacents[RIGHT] = self.start_node
						self.start_node.Adjacents[LEFT] = left_node
						new_node = None #No Need for Top Buffer in Start Node
						left_node = None
						continue
				#For A Wall
				if cur == False:
					continue

				#For a Node with Some Left Node waiting to be connected
				if prv == True:
					new_node = Maze.Node(y, x)
					self.count += 1
					left_node.Adjacents[RIGHT] = new_node
					new_node.Adjacents[LEFT] = left_node
					if nxt == True:
						left_node = new_node
					else:
						left_node = None
				#For a Node without any Left Node
				else:
					new_node = Maze.Node(y, x)
					self.count += 1
					if nxt == True:
						left_node = new_node
						#prv = True
					else:
						left_node = None
						#prv = False

				#Using Top Buffer
				if new_node != None:
					#If there exists a node above
					#if temp_top[x] != None: #BAD BAD IF
					if self.grid[new_node.y-1, new_node.x]:
						temp_top[x].Adjacents[DOWN] = new_node
						new_node.Adjacents[UP] = temp_top[x]

					#Updating Top Buffer
					temp_top[x] = new_node
				else:
					#Resetting Top Buffer
					temp_top[x] = None


		temp_count = 0

		for i in range(self.height):
			for j in range(self.width):
				if self.grid[i, j] == True:
					temp_count += 1

		print("Nodes Created:", self.count)
		print("Expected:", temp_count)

	def traverse_graph(self):
		temp_count = np.zeros(1, dtype=int)
		temp_grid = np.copy(self.grid)

		if self.start_node == None:
			print("Start Node shouldn't be None!")
			return
		elif self.end_node == None:
			print("End Node shouldn't be None!")
			return

		#print("Start Node:", self.start_node.x, self.start_node.y)
		#print("End Node:", self.end_node.x, self.end_node.y)

		self.traverse_util(self.start_node, temp_count, temp_grid)

		print("Confirmed Nodes:", temp_count[0])


	def traverse_util(self, cur, temp_count, temp_grid):
		print(f"Node Traversed at({cur.x}, {cur.y})")
		cur.print_info()
		temp_count[0] += 1
		temp_grid[cur.y, cur.x] = False
		up_node = cur.Adjacents[UP]
		left_node = cur.Adjacents[LEFT]
		right_node = cur.Adjacents[RIGHT]
		down_node = cur.Adjacents[DOWN]

		if up_node != None and temp_grid[up_node.y, up_node.x] == True:
			self.traverse_util(up_node, temp_count, temp_grid)
		if left_node != None and temp_grid[left_node.y, left_node.x] == True:
			self.traverse_util(left_node, temp_count, temp_grid)
		if right_node != None and temp_grid[right_node.y, right_node.x] == True:
			self.traverse_util(right_node, temp_count, temp_grid)
		if down_node != None and temp_grid[down_node.y, down_node.x] == True:
			self.traverse_util(down_node, temp_count, temp_grid)

	def DFS(self):
		temp_count = np.zeros(1, dtype=int)
		temp_grid = np.copy(self.grid)

		if self.start_node == None:
			print("Start Node shouldn't be None!")
			return
		elif self.end_node == None:
			print("End Node shouldn't be None!")
			return

		#print("Start Node:", self.start_node.x, self.start_node.y)
		#print("End Node:", self.end_node.x, self.end_node.y)

		is_finished = self.DFS_util(self.start_node, temp_count, temp_grid)

		if is_finished:
			print(f"Algorithm used = \"DFS\", No of moves utilized = {temp_count[0]}")
		else:
			print(f"Algorithm used = \"DFS\", End State Not Found!")

		
		self.save_image("DFS", temp_grid)


	def DFS_util(self, cur, temp_count, temp_grid):
		#print(f"Node Traversed at({cur.x}, {cur.y})")
		temp_count[0] += 1
		temp_grid[cur.y, cur.x] = False
		up_node = cur.Adjacents[UP]
		left_node = cur.Adjacents[LEFT]
		right_node = cur.Adjacents[RIGHT]
		down_node = cur.Adjacents[DOWN]

		if cur == self.end_node:
			return True

		bool_up = False
		bool_left = False
		bool_right = False
		bool_down = False

		if up_node != None and temp_grid[up_node.y, up_node.x] == True:
			bool_up = self.DFS_util(up_node, temp_count, temp_grid)
			if bool_up:
				return True
		if left_node != None and temp_grid[left_node.y, left_node.x] == True:
			bool_left = self.DFS_util(left_node, temp_count, temp_grid)
			if bool_left:
				return True
		if right_node != None and temp_grid[right_node.y, right_node.x] == True:
			bool_right = self.DFS_util(right_node, temp_count, temp_grid)
			if bool_right:
				return True
		if down_node != None and temp_grid[down_node.y, down_node.x] == True:
			bool_down = self.DFS_util(down_node, temp_count, temp_grid)
			if bool_down:
				return True

		return False

	def BFS(self):
		temp_count = np.zeros(1, dtype=int)
		temp_grid = np.copy(self.grid)

		if self.start_node == None:
			print("Start Node shouldn't be None!")
			return
		elif self.end_node == None:
			print("End Node shouldn't be None!")
			return

		queue = []

		queue.append(self.start_node)
		temp_grid[self.start_node.y, self.start_node.x] = False

		is_finished = False

		while(len(queue) != 0):
			#Updating Current Node
			cur = queue.pop(0)
			#Printing/Debugging
			#print(f"Node Traversed at({cur.x}, {cur.y})")

			#Incrementing the Cost
			temp_count[0] += 1
			if cur == self.end_node:
				is_finished = True
				break
			#Some temporary variables
			up_node = cur.Adjacents[UP]
			left_node = cur.Adjacents[LEFT]
			right_node = cur.Adjacents[RIGHT]
			down_node = cur.Adjacents[DOWN]
			#Inserting to the queue
			if up_node != None and temp_grid[up_node.y, up_node.x]:
				queue.append(up_node)
				temp_grid[up_node.y, up_node.x] = False
			if left_node != None and temp_grid[left_node.y, left_node.x]:
				queue.append(left_node)
				temp_grid[left_node.y, left_node.x] = False
			if right_node != None and temp_grid[right_node.y, right_node.x]:
				queue.append(right_node)
				temp_grid[right_node.y, right_node.x] = False
			if down_node != None and temp_grid[down_node.y, down_node.x]:
				queue.append(down_node)
				temp_grid[down_node.y, down_node.x] = False
			
		if is_finished:
			print(f"Algorithm used = \"BFS\", No of moves utilized = {temp_count[0]}")
		else:
			print(f"Algorithm used = \"BFS\", End State Not Found!")


		self.save_image("BFS", temp_grid)


	def save_image(self, algo_name, temp_grid):
		image_grid = np.copy(self.grid).astype('uint8')*255

		for x in range(self.width):
			for y in range(self.height):
				if self.grid[y, x]:
					if temp_grid[y, x] == False:
						image_grid[y, x] = 127

		im = Image.fromarray(image_grid, 'L')
		im.resize((512,512), Image.NEAREST).save(algo_name+".png")


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

	#Checking Nodes
	#maze.traverse_graph()

	#Find Result
	maze.DFS()
	maze.BFS()


if __name__ == '__main__':
	main()