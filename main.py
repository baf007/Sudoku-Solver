import math
import time
import copy

#Test cases
#filename = "10 Apr 2026 4x4.txt"  #https://sudokubliss.com/5B10-4-2026-sudoku
#filename = "2 Nov 2025 Easy.txt" #https://sudokubliss.com/5E2-11-2025-sudoku
#filename = "2 Nov 2025 Hard.txt" #https://sudokubliss.com/5H2-11-2025-sudoku
filename = "2 Nov 2025 Expert.txt" #https://sudokubliss.com/5V2-11-2025-sudoku
#filename = "10 Nov 2025 16x16.txt" #https://sudokubliss.com/5Y10-11-2025-sudoku

#Create grid + solution grid
with open(filename) as file:
	gridSize = int(file.readline())
	if math.sqrt(gridSize) != math.floor(math.sqrt(gridSize)):
		print("Error: grid size must be perfect square")
		quit()
	grid = [[] * gridSize for i in range(gridSize)]
	for x in range(gridSize):
		currLine = file.readline()
		for y in range(len(currLine) - 1):
			grid[x].append(currLine[y])
	solutionGrid = [[] * gridSize for i in range(gridSize)]
	for x in range(gridSize):
		currLine = file.readline()
		for y in range(len(currLine) - 1):
			solutionGrid[x].append(currLine[y])
marksGrid = [[set()] * gridSize for i in range(gridSize)]
boxSize = int(math.sqrt(gridSize))
match(gridSize):
	case 4:
		charSet = {"1", "2", "3", "4"}
	case 9:
		charSet = {"1", "2", "3", "4", "5", "6", "7", "8", "9"}
	case 16:
		charSet = {"1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F", "G"}
	case 25:
		charSet = {"1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P"}
	case _:
		print("Error: undefined charset")
		quit()

charSetList = list(charSet)
charSetList.sort()
markSpaces = {}
k = 0
for i in range(boxSize):
	for j in range(boxSize):
		markSpaces.update({(i, j) : charSetList[k]})
		k += 1

class Box:
	def __init__(self, x, y):
		self.leftBound = math.floor(x / boxSize) * boxSize
		self.rightBound = (math.floor(x / boxSize) + 1) * boxSize
		self.lowerBound = math.floor(y / boxSize) * boxSize
		self.upperBound = (math.floor(y / boxSize) + 1) * boxSize
		self.position = (math.floor(x / boxSize)), (math.floor(y / boxSize))

		match(gridSize):
			case 4:
				match(self.position):
					case (0, 0): self.number = 1
					case (0, 1): self.number = 2
					case (1, 0): self.number = 3
					case (1, 1): self.number = 4
			case 9:
				match(self.position):
					case (0, 0): self.number = 1
					case (0, 1): self.number = 2
					case (0, 2): self.number = 3
					case (1, 0): self.number = 4
					case (1, 1): self.number = 5
					case (1, 2): self.number = 6
					case (2, 0): self.number = 7
					case (2, 1): self.number = 8
					case (2, 2): self.number = 9
			case 16:
				match(self.position):
					case (0, 0): self.number = 1
					case (0, 1): self.number = 2
					case (0, 2): self.number = 3
					case (0, 3): self.number = 4
					case (1, 0): self.number = 5
					case (1, 1): self.number = 6
					case (1, 2): self.number = 7
					case (1, 3): self.number = 8
					case (2, 0): self.number = 9
					case (2, 1): self.number = 10
					case (2, 2): self.number = 11
					case (2, 3): self.number = 12
					case (3, 0): self.number = 13
					case (3, 1): self.number = 14
					case (3, 2): self.number = 15
					case (3, 3): self.number = 16
			case 25:
				match(self.position):
					case (0, 0): self.number = 1
					case (0, 1): self.number = 2
					case (0, 2): self.number = 3
					case (0, 3): self.number = 4
					case (0, 4): self.number = 5
					case (1, 0): self.number = 6
					case (1, 1): self.number = 7
					case (1, 2): self.number = 8
					case (1, 3): self.number = 9
					case (1, 4): self.number = 10
					case (2, 0): self.number = 11
					case (2, 1): self.number = 12
					case (2, 2): self.number = 13
					case (2, 3): self.number = 14
					case (2, 4): self.number = 15
					case (3, 0): self.number = 16
					case (3, 1): self.number = 17
					case (3, 2): self.number = 18
					case (3, 3): self.number = 19
					case (3, 4): self.number = 20
					case (4, 0): self.number = 21
					case (4, 1): self.number = 22
					case (4, 2): self.number = 23
					case (4, 3): self.number = 24
					case (4, 4): self.number = 25

	def __str__(self):
		return f"""Box Number: {self.number}
Box Position: {self.position}
Horizontal Bounds: ({self.leftBound}, {self.rightBound}]
Vertical Bounds: ({self.lowerBound}, {self.upperBound}]"""

#SETUP FUNCTIONS
def borderGrid(num):
	match(num):
		case 1: gridBorder = "┌"
		case 2: gridBorder = "├"
		case 3: gridBorder = "└"
	for i in range(boxSize):
		for j in range(boxSize * 2 + 1):
			gridBorder += "─"
		match (num):
			case 1: gridBorder += "┬"
			case 2: gridBorder += "┼"
			case 3: gridBorder += "┴"
	match (num):
		case 1: return gridBorder[:-1] + "┐"
		case 2: return gridBorder[:-1] + "┤"
		case 3: return gridBorder[:-1] + "┘"

def printGrid(isSolution):
	print(borderGrid(1))
	for x in range(gridSize):
		if x > 0 and x % boxSize == 0:
			print(borderGrid(2))
		for y in range(gridSize):
			if y % boxSize == 0:
				if y != 0:
					print(" ", end="")
				print("│ ", end="")
			else:
				print(" ", end="")
			print(solutionGrid[x][y] if isSolution else grid[x][y], end="")
		print(" │")
	print(borderGrid(3))

def borderMarksGrid(num):
	match(num):
		case 1: gridBorder = "╔"
		case 2: gridBorder = "╟"
		case 3: gridBorder = "╠"
		case 4: gridBorder = "╚"
	for i in range(boxSize):
		for j in range(boxSize):
			for k in range(boxSize * 2 + 1):
				match (num):
					case 1: gridBorder += "═"
					case 2: gridBorder += "─"
					case 3: gridBorder += "═"
					case 4: gridBorder += "═"
			if j == boxSize - 1:
				match (num):
					case 1: gridBorder += "╦"
					case 2: gridBorder += "╫"
					case 3: gridBorder += "╬"
					case 4: gridBorder += "╩"
			else:
				match (num):
					case 1: gridBorder += "╤"
					case 2: gridBorder += "┼"
					case 3: gridBorder += "╪"
					case 4: gridBorder += "╧"
	match (num):
		case 1: return gridBorder[:-1] + "╗"
		case 2: return gridBorder[:-1] + "╢"
		case 3: return gridBorder[:-1] + "╣"
		case 4: return gridBorder[:-1] + "╝"

def printMarksGrid():
	print(borderMarksGrid(1))
	for x in range(gridSize * boxSize):
		if x > 0:
			if x % gridSize == 0:
				print(borderMarksGrid(3))
			elif x % boxSize == 0:
				print(borderMarksGrid(2))
		for y in range(gridSize * boxSize):
			if y % boxSize == 0:
				if y > 0:
					print(" ", end="")
				if y % gridSize == 0:
					print("║ ", end="")
				else:
					print("│ ", end="")
			else:
				print(" ", end="")
			currMark = markSpaces.get((x % boxSize, y % boxSize))
			if currMark in marksGrid[math.floor(x/boxSize)][math.floor(y/boxSize)]:
				print(currMark, end="")
			else:
				print(" ", end="")
		print(" ║")
	print(borderMarksGrid(4))

def validateGrid():
	for x in range(gridSize):
		numbers = []
		for y in range(gridSize):
			if grid[x][y] != "_":
				numbers.append(grid[x][y])
		if len(numbers) >= 2:
			numbers.sort()
			for i in range(len(numbers) - 1):
				if numbers[i] == numbers[i + 1]:
					print(f"Error: duplicates in column {y}")
					print(numbers)
					quit()

	for y in range(gridSize):
		numbers = []
		for x in range(gridSize):
			if grid[x][y] != "_":
				numbers.append((grid[x][y]))
		if len(numbers) >= 2:
			numbers.sort()
			for i in range(len(numbers) - 1):
				if numbers[i] == numbers[i + 1]:
					print(f"Error: duplicates in row {x}")
					print(numbers)
					quit()

	for box in range(boxSize):
		numbers = []
		for x in range(boxSize):
			for y in range(boxSize):
				if grid[x][y] != "_":
					numbers.append((grid[x][y]))
		if len(numbers) >= 2:
			numbers.sort()
			for i in range(len(numbers) - 1):
				if numbers[i] == numbers[i + 1]:
					print(f"Error: duplicates in box {box}")
					print(numbers)
					quit()

#PLACEMENT FUNCTIONS
#Clear number i from marks in current space's row, column, and box. Also clears all marks from current space
def clearMarks(x, y, box, i):
	for j in range(gridSize):
		if i in marksGrid[x][j]:
			marksGrid[x][j].remove(i)
		if i in marksGrid[j][y]:
			marksGrid[j][y].remove(i)

	for y2 in range(box.lowerBound, box.upperBound):
		for x2 in range(box.leftBound, box.rightBound):
			if i in marksGrid[x2][y2]:
				marksGrid[x2][y2].remove(i)

	marksGrid[x][y].clear()

def checkPlacement(x, y, i, loopCt):
	if grid[x][y] != solutionGrid[x][y]:
		grid[x][y] = "X"
		printMarksGrid()
		printGrid(False)
		sortedMarks = list(marksGrid[x][y])
		sortedMarks.sort()
		print(f"Error: tried to place incorrect {i} at ({x}, {y}) on loop {loopCt}")
		print(f"Marks: {sortedMarks}")
		quit()

def placeNumbers(x, y):
	box = Box(x, y)

	# Place number if it's the only mark in the space
	if len(marksGrid[x][y]) == 1:
		for i in list(marksGrid[x][y]):
			grid[x][y] = i
			checkPlacement(x, y, i, loopCt)
			clearMarks(x, y, box, i)

	# Place number if it's only marked once in any group
	else:
		for i in list(marksGrid[x][y]):

			#Row
			currGroup = set()
			for y2 in range(gridSize):
				if grid[x][y2] == "_" and y2 != y:
					currGroup.update(marksGrid[x][y2])
					if i in currGroup:
						break
			if i not in currGroup:
				grid[x][y] = i
				checkPlacement(x, y, i, loopCt)
				clearMarks(x, y, box, i)

			#Column
			currGroup = set()
			for x2 in range(gridSize):
				if grid[x2][y] == "_" and x2 != x:
					currGroup.update(marksGrid[x2][y])
					if i in currGroup:
						break
			if i not in currGroup:
				grid[x][y] = i
				checkPlacement(x, y, i, loopCt)
				clearMarks(x, y, box, i)

			#Box
			currGroup = set()
			breakLoop = False
			for y2 in range(box.lowerBound, box.upperBound):
				for x2 in range(box.leftBound, box.rightBound):
					if grid[x2][y2] == "_" and (x2 != x or y2 != y):
						currGroup.update(marksGrid[x2][y2])
						if i in currGroup:
							breakLoop = True
							break
				if breakLoop:
					break
			if i not in currGroup:
				grid[x][y] = i
				checkPlacement(x, y, i, loopCt)
				clearMarks(x, y, box, i)
	del box

#ELIMINATION FUNCTIONS
#If multiple spaces' marks are a subset of the current space's, remove those marks from all other spaces in group
def checkSubsets(x, y):
	box = Box(x, y)

	#Row
	subsetIndices = set()
	for x2 in range(gridSize):
		if grid[x2][y] == "_" and marksGrid[x2][y].issubset(marksGrid[x][y]):
			subsetIndices.add(x2)
	if len(subsetIndices) == len(marksGrid[x][y]):
		for x2 in range(gridSize):
			if x2 not in subsetIndices:
				marksGrid[x2][y] -= marksGrid[x][y]

	#Column
	subsetIndices = set()
	for y2 in range(gridSize):
		if grid[x][y2] == "_" and marksGrid[x][y2].issubset(marksGrid[x][y]):
			subsetIndices.add(y2)
	if len(subsetIndices) == len(marksGrid[x][y]):
		for y2 in range(gridSize):
			if y2 not in subsetIndices:
				marksGrid[x][y2] -= marksGrid[x][y]

	#Box
	subsetIndices = set()
	for y2 in range(box.lowerBound, box.upperBound):
		for x2 in range(box.leftBound, box.rightBound):
			if grid[x2][y2] == "_" and marksGrid[x2][y2].issubset(marksGrid[x][y]):
				subsetIndices.add((x2, y2))
	if len(subsetIndices) == len(marksGrid[x][y]):
		for y2 in range(box.lowerBound, box.upperBound):
			for x2 in range(box.leftBound, box.rightBound):
				if (x2, y2) not in subsetIndices:
					marksGrid[x2][y2] -= marksGrid[x][y]
	del box

#Handle cases like {1, 2}, {2, 3}, {1, 3} and remove those marks from rest of group
def checkBrokenSets(x, y):
	box = Box(x, y)

	#If n spaces have a set n long, remove those numbers' marks from rest of the row
	subsetIndices = {x}
	superSet = copy.deepcopy(marksGrid[x][y])
	for x2 in range(gridSize):
		if grid[x2][y] == "_" and not marksGrid[x2][y].issubset(marksGrid[x][y]) and len(
				marksGrid[x2][y]) == len(marksGrid[x][y]) and not marksGrid[x2][y].isdisjoint(
				marksGrid[x][y]):
			subsetIndices.add(x2)
			superSet.update(marksGrid[x2][y])
	if len(subsetIndices) == len(superSet) and len(subsetIndices) > 1:
		for x2 in range(gridSize):
			if x2 not in subsetIndices and grid[x2][y] == "_":
				marksGrid[x2][y] -= superSet

	# If n spaces have a set n long, remove those numbers' marks from rest of the column
	subsetIndices = {y}
	superSet = copy.deepcopy(marksGrid[x][y])
	for y2 in range(gridSize):
		if grid[x][y2] == "_" and not marksGrid[x][y2].issubset(marksGrid[x][y]) and len(
				marksGrid[x][y2]) == len(marksGrid[x][y]) and not marksGrid[x][y2].isdisjoint(
				marksGrid[x][y]):
			subsetIndices.add(y2)
			superSet.update(marksGrid[x][y2])
	if len(superSet) == len(subsetIndices) and len(subsetIndices) > 1:
		for y2 in range(gridSize):
			if y2 not in subsetIndices and grid[x][y2] == "_":
				marksGrid[x][y2] -= superSet

	# If n spaces have a set n long, remove those numbers' marks from rest of the box
	subsetIndices = {(x, y)}
	superSet = copy.deepcopy(marksGrid[x][y])
	for y2 in range(box.lowerBound, box.upperBound):
		for x2 in range(box.leftBound, box.rightBound):
			if grid[x2][y2] == "_" and not marksGrid[x2][y2].issubset(marksGrid[x][y]) and len(
					marksGrid[x2][y2]) == len(marksGrid[x][y]) and not marksGrid[x2][y2].isdisjoint(
					marksGrid[x][y]):
				subsetIndices.add((x2, y2))
				superSet.update(marksGrid[x2][y2])
	if len(subsetIndices) == len(superSet) and len(subsetIndices) > 1:
		for y2 in range(box.lowerBound, box.upperBound):
			for x2 in range(box.leftBound, box.rightBound):
				if (x2, y2) not in subsetIndices:
					marksGrid[x2][y2] -= superSet
	del box

#If number can only be in one row/col in box, remove mark in row/col outside box
# ┌───────┬───────┬───────┐		┌───────┬───────┬───────┐
# │     X │       │   X   │	->	│     X │       │   X   │
# │ X     │ X X X │ X X X │		│       │ X X X │       │
# │   X   │       │ X   X │	->	│   X   │       │ X   X │
# └───────┴───────┴───────┘		└───────┴───────┴───────┘
def checkLockedCandidate1(x, y):
	box = Box(x, y)
	rowCandidates = set()
	colCandidates = set()
	for i in marksGrid[x][y]:
		#Row
		candidate = False
		for y2 in range(box.lowerBound, box.upperBound):
			breakLoop = False
			for x2 in range(box.leftBound, box.rightBound):
				if x2 == x and y2 == y:
					continue
				if grid[x2][y2] == "_" and i in marksGrid[x2][y2]:
					if x2 == x and y2 != y:
						candidate = True
					elif i in marksGrid[x2][y2]:
						candidate = False
						breakLoop = True
						break
			if breakLoop:
				break
		if candidate:
			rowCandidates.add(i)

		#Column
		candidate = False
		for y2 in range(box.lowerBound, box.upperBound):
			breakLoop = False
			for x2 in range(box.leftBound, box.rightBound):
				if x2 == x and y2 == y:
					continue
				if grid[x2][y2] == "_" and i in marksGrid[x2][y2]:
					if x2 != x and y2 == y:
						candidate = True
					else:
						candidate = False
						breakLoop = True
						break
			if breakLoop:
				break
		if candidate:
			colCandidates.add(i)

	if len(rowCandidates) > 0:
		for y2 in range(gridSize):
			if grid[x][y2] == "_" and not box.lowerBound <= y2 < box.upperBound:
				marksGrid[x][y2] -= rowCandidates

	if len(colCandidates) > 0:
		for x2 in range(gridSize):
			if grid[x2][y] == "_" and not box.leftBound <= x2 < box.rightBound:
				marksGrid[x2][y] -= colCandidates
	del box

#If number can only be in one box in row/col, remove mark in box outside row/col
# ┌───────┬───────┬───────┐		┌───────┬───────┬───────┐
# │ X     │ X     │       │	->	│ X     │       │       │
# │       │ X X X │       │		│       │ X X X │       │
# │       │     X │     X │	->	│       │       │     X │
# └───────┴───────┴───────┘		└───────┴───────┴───────┘
def checkLockedCandidate2(x, y):
	box = Box(x, y)

	for i in marksGrid[x][y]:
		#Row
		for y2 in range(gridSize):
			candidate = True
			if grid[x][y2] == "_" and not box.leftBound <= y2 < box.rightBound and i in marksGrid[x][y2]:
				candidate = False
				break
		if candidate:
			for x2 in range(box.lowerBound, box.upperBound):
				for y2 in range(box.leftBound, box.rightBound):
					if x2 != x and i in marksGrid[x2][y2]:
						marksGrid[x2][y2].remove(i)
		#Column
		for x2 in range(gridSize):
			candidate = True
			if grid[x2][y] == "_" and not box.lowerBound <= x2 < box.upperBound and i in marksGrid[x2][y]:
				candidate = False
				break
		if candidate:
			for x2 in range(box.lowerBound, box.upperBound):
				for y2 in range(box.leftBound, box.rightBound):
					if y2 != y and i in marksGrid[x2][y2]:
						marksGrid[x2][y2].remove(i)
	del box

#If a mark appears in exactly 4 corners across two rows/cols, clear mark from those corners' cols/rows aside from the corners themselves
def xWing(x, y):
	#Scan rows
	for i in marksGrid[x][y]:
		corners = []
		for y2 in range(gridSize):
			if y2 == y:
				continue
			for x2 in range(gridSize):
				if (i not in marksGrid[x2][y] and i in marksGrid[x2][y2]) or (i in marksGrid[x2][y] and i not in marksGrid[x2][y2]):
					corners.clear()
					break
				if i in marksGrid[x2][y] and i in marksGrid[x2][y2]:
					corners.append((x2, y))
					corners.append((x2, y2))
			if len(corners) == 4:
				break
			corners.clear()
		if len(corners) == 4:
			for y2 in range(gridSize):
				if y2 == corners[0][1] or y2 == corners[1][1]:
					continue
				marksGrid[corners[0][0]][y2].discard(i)
				marksGrid[corners[2][0]][y2].discard(i)

		#Scan columns	
		corners = []
		for x2 in range(gridSize):
			if x2 == x:
				continue
			for y2 in range(gridSize):
				if (i not in marksGrid[x][y2] and i in marksGrid[x2][y2]) or (i in marksGrid[x][y2] and i not in marksGrid[x2][y2]):
					corners.clear()
					break
				if i in marksGrid[x][y2] and i in marksGrid[x2][y2]:
					corners.append((x, y2))
					corners.append((x2, y2))
			if len(corners) == 4:
				break
			corners.clear()
		if len(corners) == 4:
			for x2 in range(gridSize):
				if x2 == corners[0][0] or x2 == corners[1][0]:
					continue
				marksGrid[x2][corners[0][1]].discard(i)
				marksGrid[x2][corners[2][1]].discard(i)

#If row and col both have two of a number, remove number from intersection
def twoStringKite(x, y):
	box = Box(x, y)
	for i in marksGrid[x][y]:
		start1 = (x, y)
		end1 = None
		start2 = None
		end2 = None
		vertEnd = None
		horizEnd = None
		horizCt = 0
		vertCt = 0
		horizCt2 = 0
		vertCt2 = 0
		firstIsVertical = False
		firstIsHorizontal = False
		secondIsVertical = False
		secondIsHorizontal = False
		for j in range(gridSize):
			if i in marksGrid[j][y]:
				vertCt += 1
				if j != x:
					vertEnd = (j, y)
			if i in marksGrid[x][j]:
				horizCt += 1
				if j != y:
					horizEnd = (x, j)
		if vertCt != 2 and horizCt != 2:
			continue
		if vertCt == 2:
			firstIsVertical = True
			end1 = vertEnd
		if horizCt == 2:
			firstIsHorizontal = True
			end1 = horizEnd

		for x2 in range(box.leftBound, box.rightBound):
			if x2 == x:
				continue
			for y2 in range(box.lowerBound, box.upperBound):
				if y2 == y:
					continue
				if i in marksGrid[x2][y2]:
					start2 = (x2, y2)
					for j in range(gridSize):
						if i in marksGrid[j][y2] and firstIsHorizontal and not firstIsVertical:
							vertCt2 += 1
							if j != x2:
								vertEnd = (j, y2)
						if i in marksGrid[x2][j] and firstIsVertical and not firstIsHorizontal:
							horizCt2 += 1
							if j != y2:
								horizEnd = (x2, j)
					if vertCt2 == 2:
						secondIsVertical = True
						end2 = vertEnd
						break
					if horizCt2 == 2:
						secondIsHorizontal = True
						end2 = horizEnd
						break
			if secondIsVertical or secondIsHorizontal:
				break
		if start2 == None or end2 == None:
			continue

		isRow1 = False
		isCol1 = False
		isRow2 = False
		isCol2 = False
		if start1[0] == end1[0]: isCol1 = True
		if start1[1] == end1[1]: isRow1 = True
		if start2[0] == end2[0]: isCol2 = True
		if start2[1] == end2[1]: isRow2 = True

		if (isRow1 and isRow2) or (isCol1 and isCol2):
			continue

		targetX = end2[0]
		targetY = end1[1]

		if targetX == x and targetY == y:
			raise Exception(f"{targetX} = {x} and/or {targetY} = {y} | i = {i}")
		
		#Find intersection of both ends
		if grid[targetX][targetY] == "_" and i in marksGrid[targetX][targetY]:
				marksGrid[targetX][targetY].remove(i)
	del box

validateGrid()
print("Starting grid:")
printGrid(False)
startTime = time.perf_counter()
for x in range(gridSize):
	for y in range(gridSize):
		if grid[x][y] == "_":

			#Mark current row
			currGroup = set()
			for x2 in range(gridSize):
				inspectedSpace = grid[x2][y]
				if inspectedSpace != "_":
					currGroup.add(inspectedSpace)
			marksGrid[x][y] = charSet - currGroup

			#Mark current column
			currGroup = set()
			for y2 in range(gridSize):
				inspectedSpace = grid[x][y2]
				if inspectedSpace != "_":
					currGroup.add(inspectedSpace)
			marksGrid[x][y] -= currGroup

			#Mark current box
			box = Box(x, y)
			currGroup = set()
			for y2 in range(box.lowerBound, box.upperBound):
				for x2 in range(box.leftBound, box.rightBound):
					inspectedSpace = grid[x2][y2]
					if inspectedSpace != "_":
						currGroup.add(inspectedSpace)
			marksGrid[x][y] -= currGroup
			del box
loopCt = 0
complete = False
while not complete:
	loopCt += 1
	print(f"Loop {loopCt}:")
	prevGrid = copy.deepcopy(grid)
	prevMarksGrid = copy.deepcopy(marksGrid)

	for x in range(gridSize):
		for y in range(gridSize):
			if grid[x][y] == "_":

				placeNumbers(x, y)

				if grid[x][y] in charSet:
					continue

				checkSubsets(x, y)
				checkBrokenSets(x, y)
				checkLockedCandidate1(x, y)
				checkLockedCandidate2(x, y)
				xWing(x, y)
				twoStringKite(x, y)

				if marksGrid[x][y] == set():
					print(f"Error: all marks removed from ({x}, {y}) on loop {loopCt}")
					print(f"Before: {prevMarksGrid[x][y]}\nAfter:  {marksGrid[x][y]}")
					quit()

	printGrid(False)
	validateGrid()
	printMarksGrid()
	print()

	if prevGrid == grid:
		print(f"\nPuzzle not solved ({loopCt} loops)")
		quit()

	#Check completion
	complete = True
	for x in range(gridSize):
		for y in range(gridSize):
			if grid[x][y] == "_":
				complete = False

endTime = time.perf_counter()

validateGrid()
printGrid(False)
print(f"Puzzle solved in {loopCt} loops")
print(f"Compute time: {((endTime - startTime) * 1000):.2f} ms ({((endTime - startTime)):.1f} sec)")