import math
import time
import copy

#Test cases
#filename = "10 Apr 2026 4x4.txt"  #https://sudokubliss.com/5B10-4-2026-sudoku
#filename = "2 Nov 2025 Easy.txt" #https://sudokubliss.com/5E2-11-2025-sudoku
#filename = "2 Nov 2025 Hard.txt" #https://sudokubliss.com/5H2-11-2025-sudoku
#filename = "2 Nov 2025 Expert.txt" #https://sudokubliss.com/5V2-11-2025-sudoku
#filename = "12 Jul 2026 Evil.txt" #https://sudokubliss.com/5U12-7-2026-sudoku
filename = "9 Oct 2026 Evil.txt" #https://sudokubliss.com/U09-10-2026-sudoku
#filename = "10 Nov 2025 16x16.txt" #https://sudokubliss.com/5Y10-11-2025-sudoku

#Create grid + solution grid
with open(filename) as file:
	gridSize = int(file.readline())
	if math.sqrt(gridSize) != math.floor(math.sqrt(gridSize)):
		print("Error: grid size must be perfect square")
		quit()
	grid = [[] * gridSize for i in range(gridSize)]
	for y in range(gridSize):
		currLine = file.readline()
		if len(currLine) - 1 != gridSize:
			print("Error: row does not match grid size")
			quit()
		for x in range(len(currLine) - 1):
			grid[y].append(currLine[x])
	solutionGrid = [[] * gridSize for i in range(gridSize)]
	for y in range(gridSize):
		currLine = file.readline()
		for x in range(len(currLine) - 1):
			solutionGrid[y].append(currLine[x])
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
		self.position = (math.floor(y / boxSize)), (math.floor(x / boxSize))

		match(gridSize):
			case 4:
				match(self.position):
					case (0, 0): self.number = 1
					case (1, 0): self.number = 2
					case (0, 1): self.number = 3
					case (1, 1): self.number = 4
			case 9:
				match(self.position):
					case (0, 0): self.number = 1
					case (1, 0): self.number = 2
					case (2, 0): self.number = 3
					case (0, 1): self.number = 4
					case (1, 1): self.number = 5
					case (2, 1): self.number = 6
					case (0, 2): self.number = 7
					case (1, 2): self.number = 8
					case (2, 2): self.number = 9
			case 16:
				match(self.position):
					case (0, 0): self.number = 1
					case (1, 0): self.number = 2
					case (2, 0): self.number = 3
					case (3, 0): self.number = 4
					case (0, 1): self.number = 5
					case (1, 1): self.number = 6
					case (2, 1): self.number = 7
					case (3, 1): self.number = 8
					case (0, 2): self.number = 9
					case (1, 2): self.number = 10
					case (2, 2): self.number = 11
					case (3, 2): self.number = 12
					case (0, 3): self.number = 13
					case (1, 3): self.number = 14
					case (2, 3): self.number = 15
					case (3, 3): self.number = 16
			case 25:
				match(self.position):
					case (0, 0): self.number = 1
					case (1, 0): self.number = 2
					case (2, 0): self.number = 3
					case (3, 0): self.number = 4
					case (4, 0): self.number = 5
					case (0, 1): self.number = 6
					case (1, 1): self.number = 7
					case (2, 1): self.number = 8
					case (3, 1): self.number = 9
					case (4, 1): self.number = 10
					case (0, 2): self.number = 11
					case (1, 2): self.number = 12
					case (2, 2): self.number = 13
					case (3, 2): self.number = 14
					case (4, 2): self.number = 15
					case (0, 3): self.number = 16
					case (1, 3): self.number = 17
					case (2, 3): self.number = 18
					case (3, 3): self.number = 19
					case (4, 3): self.number = 20
					case (0, 4): self.number = 21
					case (1, 4): self.number = 22
					case (2, 4): self.number = 23
					case (3, 4): self.number = 24
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
	for y in range(gridSize):
		if y > 0 and y % boxSize == 0:
			print(borderGrid(2))
		for x in range(gridSize):
			if x % boxSize == 0:
				if x != 0:
					print(" ", end="")
				print("│ ", end="")
			else:
				print(" ", end="")
			print(solutionGrid[y][x] if isSolution else grid[y][x], end="")
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
	for y in range(gridSize * boxSize):
		if y > 0:
			if y % gridSize == 0:
				print(borderMarksGrid(3))
			elif y % boxSize == 0:
				print(borderMarksGrid(2))
		for x in range(gridSize * boxSize):
			if x % boxSize == 0:
				if x > 0:
					print(" ", end="")
				if x % gridSize == 0:
					print("║ ", end="")
				else:
					print("│ ", end="")
			else:
				print(" ", end="")
			currMark = markSpaces.get((y % boxSize, x % boxSize))
			if currMark in marksGrid[math.floor(y/boxSize)][math.floor(x/boxSize)]:
				print(currMark, end="")
			else:
				print(" ", end="")
		print(" ║")
	print(borderMarksGrid(4))

def validateGrid():
	for y in range(gridSize):
		numbers = []
		for x in range(gridSize):
			if grid[y][x] != "_":
				numbers.append(grid[y][x])
		if len(numbers) >= 2:
			numbers.sort()
			for i in range(len(numbers) - 1):
				if numbers[i] == numbers[i + 1]:
					print(f"Error: duplicates in column {x}")
					print(numbers)
					quit()

	for x in range(gridSize):
		numbers = []
		for y in range(gridSize):
			if grid[y][x] != "_":
				numbers.append((grid[y][x]))
		if len(numbers) >= 2:
			numbers.sort()
			for i in range(len(numbers) - 1):
				if numbers[i] == numbers[i + 1]:
					print(f"Error: duplicates in row {y}")
					print(numbers)
					quit()

	for box in range(boxSize):
		numbers = []
		for y in range(boxSize):
			for x in range(boxSize):
				if grid[y][x] != "_":
					numbers.append((grid[y][x]))
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
		if i in marksGrid[j][x]:
			marksGrid[j][x].remove(i)
		if i in marksGrid[y][j]:
			marksGrid[y][j].remove(i)

	for x2 in range(box.leftBound, box.rightBound):
		for y2 in range(box.lowerBound, box.upperBound):
			if i in marksGrid[y2][x2]:
				marksGrid[y2][x2].remove(i)

	marksGrid[y][x].clear()

def checkPlacement(x, y, i, loopCt):
	if grid[y][x] != solutionGrid[y][x]:
		grid[y][x] = "X"
		printMarksGrid()
		printGrid(False)
		sortedMarks = list(marksGrid[y][x])
		sortedMarks.sort()
		print(f"Error: tried to place incorrect {i} at {x, y} on loop {loopCt}")
		print(f"Marks: {sortedMarks}")
		quit()

def placeNumbers(x, y):
	box = Box(x, y)

	# Place number if it's the only mark in the space
	if len(marksGrid[y][x]) == 1:
		for i in list(marksGrid[y][x]):
			grid[y][x] = i
			checkPlacement(x, y, i, loopCt)
			clearMarks(x, y, box, i)

	# Place number if it's only marked once in any group
	else:
		for i in list(marksGrid[y][x]):

			#Row
			currGroup = set()
			for x2 in range(gridSize):
				if grid[y][x2] == "_" and x2 != x:
					currGroup.update(marksGrid[y][x2])
					if i in currGroup:
						break
			if i not in currGroup:
				grid[y][x] = i
				checkPlacement(x, y, i, loopCt)
				clearMarks(x, y, box, i)

			#Column
			currGroup = set()
			for y2 in range(gridSize):
				if grid[y2][x] == "_" and y2 != y:
					currGroup.update(marksGrid[y2][x])
					if i in currGroup:
						break
			if i not in currGroup:
				grid[y][x] = i
				checkPlacement(x, y, i, loopCt)
				clearMarks(x, y, box, i)

			#Box
			currGroup = set()
			breakLoop = False
			for x2 in range(box.leftBound, box.rightBound):
				for y2 in range(box.lowerBound, box.upperBound):
					if grid[y2][x2] == "_" and (x2 != x or y2 != y):
						currGroup.update(marksGrid[y2][x2])
						if i in currGroup:
							breakLoop = True
							break
				if breakLoop:
					break
			if i not in currGroup:
				grid[y][x] = i
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
		if grid[y][x2] == "_" and marksGrid[y][x2].issubset(marksGrid[y][x]):
			subsetIndices.add(x2)
	if len(subsetIndices) == len(marksGrid[y][x]):
		for x2 in range(gridSize):
			if x2 not in subsetIndices:
				marksGrid[y][x2] -= marksGrid[y][x]

	#Column
	subsetIndices = set()
	for y2 in range(gridSize):
		if grid[y2][x] == "_" and marksGrid[y2][x].issubset(marksGrid[y][x]):
			subsetIndices.add(y2)
	if len(subsetIndices) == len(marksGrid[y][x]):
		for y2 in range(gridSize):
			if y2 not in subsetIndices:
				marksGrid[y2][x] -= marksGrid[y][x]

	#Box
	subsetIndices = set()
	for x2 in range(box.leftBound, box.rightBound):
		for y2 in range(box.lowerBound, box.upperBound):
			if grid[y2][x2] == "_" and marksGrid[y2][x2].issubset(marksGrid[y][x]):
				subsetIndices.add((y2, x2))
	if len(subsetIndices) == len(marksGrid[y][x]):
		for x2 in range(box.leftBound, box.rightBound):
			for y2 in range(box.lowerBound, box.upperBound):
				if (y2, x2) not in subsetIndices:
					marksGrid[y2][x2] -= marksGrid[y][x]
	del box

#Handle cases like {1, 2}, {2, 3}, {1, 3} and remove those marks from rest of group
def checkBrokenSets(x, y):
	box = Box(x, y)

	#If n spaces have a set n long, remove those numbers' marks from rest of the row
	subsetIndices = {x}
	superSet = copy.deepcopy(marksGrid[y][x])
	for x2 in range(gridSize):
		if grid[y][x2] == "_" and not marksGrid[y][x2].issubset(marksGrid[y][x]) and len(
				marksGrid[y][x2]) == len(marksGrid[y][x]) and not marksGrid[y][x2].isdisjoint(
				marksGrid[y][x]):
			subsetIndices.add(x2)
			superSet.update(marksGrid[y][x2])
	if len(superSet) == len(subsetIndices) and len(subsetIndices) > 1:
		for x2 in range(gridSize):
			if x2 not in subsetIndices and grid[y][x2] == "_":
				marksGrid[y][x2] -= superSet

	# If n spaces have a set n long, remove those numbers' marks from rest of the column
	subsetIndices = {y}
	superSet = copy.deepcopy(marksGrid[y][x])
	for y2 in range(gridSize):
		if grid[y2][x] == "_" and not marksGrid[y2][x].issubset(marksGrid[y][x]) and len(
				marksGrid[y2][x]) == len(marksGrid[y][x]) and not marksGrid[y2][x].isdisjoint(
				marksGrid[y][x]):
			subsetIndices.add(y2)
			superSet.update(marksGrid[y2][x])
	if len(subsetIndices) == len(superSet) and len(subsetIndices) > 1:
		for y2 in range(gridSize):
			if y2 not in subsetIndices and grid[y2][x] == "_":
				marksGrid[y2][x] -= superSet

	# If n spaces have a set n long, remove those numbers' marks from rest of the box
	subsetIndices = {(x, y)}
	superSet = copy.deepcopy(marksGrid[y][x])
	for x2 in range(box.leftBound, box.rightBound):
		for y2 in range(box.lowerBound, box.upperBound):
			if grid[y2][x2] == "_" and not marksGrid[y2][x2].issubset(marksGrid[y][x]) and len(
					marksGrid[y2][x2]) == len(marksGrid[y][x]) and not marksGrid[y2][x2].isdisjoint(
					marksGrid[y][x]):
				subsetIndices.add((x2, y2))
				superSet.update(marksGrid[y2][x2])
	if len(subsetIndices) == len(superSet) and len(subsetIndices) > 1:
		for x2 in range(box.leftBound, box.rightBound):
			for y2 in range(box.lowerBound, box.upperBound):
				if (x2, y2) not in subsetIndices:
					marksGrid[y2][x2] -= superSet
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
	for i in marksGrid[y][x]:
		#Row
		candidate = False
		for x2 in range(box.leftBound, box.rightBound):
			breakLoop = False
			for y2 in range(box.lowerBound, box.upperBound):
				if x2 == x and y2 == y:
					continue
				if grid[y2][x2] == "_" and i in marksGrid[y2][x2]:
					if x2 != x and y2 == y:
						candidate = True
					elif i in marksGrid[y2][x2]:
						candidate = False
						breakLoop = True
						break
			if breakLoop:
				break
		if candidate:
			rowCandidates.add(i)

		#Column
		candidate = False
		for x2 in range(box.leftBound, box.rightBound):
			breakLoop = False
			for y2 in range(box.lowerBound, box.upperBound):
				if x2 == x and y2 == y:
					continue
				if grid[y2][x2] == "_" and i in marksGrid[y2][x2]:
					if x2 == x and y2 != y:
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
		for x2 in range(gridSize):
			if grid[y][x2] == "_" and not box.leftBound <= x2 < box.rightBound:
				marksGrid[y][x2] -= rowCandidates

	if len(colCandidates) > 0:
		for y2 in range(gridSize):
			if grid[y2][x] == "_" and not box.lowerBound <= y2 < box.upperBound:
				marksGrid[y2][x] -= colCandidates
	del box

#If number can only be in one box in row/col, remove mark in box outside row/col
# ┌───────┬───────┬───────┐		┌───────┬───────┬───────┐
# │ X     │ X     │       │	->	│ X     │       │       │
# │       │ X X X │       │		│       │ X X X │       │
# │       │     X │     X │	->	│       │       │     X │
# └───────┴───────┴───────┘		└───────┴───────┴───────┘
def checkLockedCandidate2(x, y):
	box = Box(x, y)

	for i in marksGrid[y][x]:
		#Row
		for x2 in range(gridSize):
			candidate = True
			if grid[y][x2] == "_" and not box.leftBound <= x2 < box.rightBound and i in marksGrid[y][x2]:
				candidate = False
				break
		if candidate:
			for y2 in range(box.lowerBound, box.upperBound):
				for x2 in range(box.leftBound, box.rightBound):
					if y2 != y and i in marksGrid[y2][x2]:
						marksGrid[y2][x2].remove(i)
		#Column
		for y2 in range(gridSize):
			candidate = True
			if grid[y2][x] == "_" and not box.lowerBound <= y2 < box.upperBound and i in marksGrid[y2][x]:
				candidate = False
				break
		if candidate:
			for y2 in range(box.lowerBound, box.upperBound):
				for x2 in range(box.leftBound, box.rightBound):
					if x2 != x and i in marksGrid[y2][x2]:
						marksGrid[y2][x2].remove(i)
	del box

#If a mark appears in exactly 4 corners across two rows/cols, clear mark from those corners' cols/rows aside from the corners themselves
def xWing(x, y):
	for i in marksGrid[y][x]:
		#Scan rows
		corners = []
		for x2 in range(gridSize):
			if x2 == x:
				continue
			for y2 in range(gridSize):
				if (i not in marksGrid[y2][x] and i in marksGrid[y2][x2]) or (i in marksGrid[y2][x] and i not in marksGrid[y2][x2]):
					corners.clear()
					break
				if i in marksGrid[y2][x] and i in marksGrid[y2][x2]:
					corners.append((x, y2))
					corners.append((x2, y2))
			if len(corners) == 4:
				break
			corners.clear()
		if len(corners) == 4:
			for x2 in range(gridSize):
				if x2 == corners[0][0] or x2 == corners[1][0]:
					continue
				marksGrid[corners[0][1]][x2].discard(i)
				marksGrid[corners[2][1]][x2].discard(i)

		#Scan columns	
		corners = []
		for y2 in range(gridSize):
			if y2 == y:
				continue
			for x2 in range(gridSize):
				if (i not in marksGrid[y][x2] and i in marksGrid[y2][x2]) or (i in marksGrid[y][x2] and i not in marksGrid[y2][x2]):
					corners.clear()
					break
				if i in marksGrid[y][x2] and i in marksGrid[y2][x2]:
					corners.append((x2, y))
					corners.append((x2, y2))
			if len(corners) == 4:
				break
			corners.clear()
		if len(corners) == 4:
			for y2 in range(gridSize):
				if y2 == corners[0][1] or y2 == corners[1][1]:
					continue
				marksGrid[y2][corners[0][0]].discard(i)
				marksGrid[y2][corners[2][0]].discard(i)

#Check two pincers from a pivot and clear that number's mark from spaces that see both of them
prevPivots = []
def yWing(x, y):
	if (x, y) in prevPivots:
		return
	box = Box(x, y)
	pivot = (x, y)
	pincer1 = None
	pincer1Type = None
	pincer2 = None
	pincer2Type = None
	marks = marksGrid[y][x].copy()
	rowMarks = marksGrid[y][x].copy()
	colMarks = marksGrid[y][x].copy()
	boxMarks = marksGrid[y][x].copy()
	finalMarks = []
	pincerCandidatesRow = []
	pincerCandidatesCol = []
	pincerCandidatesBox = []

	#Scan for pincer in row
	for x2 in range(gridSize):
		if len(marksGrid[y][x2]) == 2 and not marksGrid[y][x].isdisjoint(marksGrid[y][x2]) and x2 != x:
			if marksGrid[y][x2] == marksGrid[y][x]:
				return
			pincerCandidatesRow.append((x2, y))
			rowMarks.update(marksGrid[y][x2])
			marks.update(marksGrid[y][x2])
	
	#Scan for pincer in col
	for y2 in range(gridSize):
		if len(marksGrid[y2][x]) == 2 and not marksGrid[y][x].isdisjoint(marksGrid[y2][x]) and y2 != y:
			if marksGrid[y2][x] == marksGrid[y][x]:
				return
			pincerCandidatesCol.append((x, y2))
			colMarks.update(marksGrid[y2][x])
			marks.update(marksGrid[y2][x])
	
	#Scan for pincer in box
	for y2 in range(box.lowerBound, box.upperBound):
		for x2 in range(box.leftBound, box.rightBound):
			if len(marksGrid[y2][x2]) == 2 and not marksGrid[y][x].isdisjoint(marksGrid[y2][x2]) and (x2 != x or y2 != y):
				if marksGrid[y2][x2] == marksGrid[y][x]:
					return
				pincerCandidatesBox.append((x2, y2))
				boxMarks.update(marksGrid[y2][x2])
				marks.update(marksGrid[y2][x2])
	
	if len(marks) < 3:
		return

	#check if any three spaces are {a, b}, {b, c}, {a, c}
	if len(pincerCandidatesBox) > 0:
		for boxCan in pincerCandidatesBox:
			if len(pincerCandidatesRow) > 0:
				for rowCan in pincerCandidatesRow:
					rowCanBox = Box(rowCan[0], rowCan[1])
					if rowCanBox.position == box.position:
						continue
					currMarks = marksGrid[y][x].copy()
					currMarks.update(marksGrid[boxCan[1]][boxCan[0]])
					currMarks.update(marksGrid[rowCan[1]][rowCan[0]])
					if len(currMarks) != 3:
						continue
					finalMarks = currMarks.copy()
					pincer1 = rowCan
					pincer1Type = "row"
					pincer2 = boxCan
					pincer2Type = "box"
					del rowCanBox
			if len(pincerCandidatesCol) > 0:
				for colCan in pincerCandidatesCol:
					colCanBox = Box(colCan[0], colCan[1])
					if colCanBox.position == box.position:
						continue
					currMarks = marksGrid[y][x].copy()
					currMarks.update(marksGrid[boxCan[1]][boxCan[0]])
					currMarks.update(marksGrid[colCan[1]][colCan[0]])
					if len(currMarks) != 3:
						continue
					finalMarks = currMarks.copy()
					pincer1 = colCan
					pincer1Type = "col"
					pincer2 = boxCan
					pincer2Type = "box"
					del colCanBox
	if len(pincerCandidatesRow) > 0:
		for rowCan in pincerCandidatesRow:
			rowCanBox = Box(rowCan[0], rowCan[1])
			if rowCanBox.position == box.position:
				continue
			if len(pincerCandidatesCol) > 0:
				for colCan in pincerCandidatesCol:
					colCanBox = Box(colCan[0], colCan[1])
					if colCanBox.position == box.position:
						continue
					currMarks = marksGrid[y][x].copy()
					currMarks.update(marksGrid[rowCan[1]][rowCan[0]])
					currMarks.update(marksGrid[colCan[1]][colCan[0]])
					if len(currMarks) != 3:
						continue
					finalMarks = currMarks.copy()
					pincer1 = rowCan
					pincer1Type = "row"
					pincer2 = colCan
					pincer2Type = "col"
					del colCanBox
			del rowCanBox
	del box

	if (not pincer1 or not pincer2
		or pincer1[0] == pincer2[0] or pincer1[1] == pincer2[1]
		or marksGrid[pincer1[1]][pincer1[0]] == marksGrid[pincer2[1]][pincer2[0]]
		or marksGrid[pivot[1]][pivot[0]] == marksGrid[pincer1[1]][pincer1[0]]
		or marksGrid[pivot[1]][pivot[0]] == marksGrid[pincer2[1]][pincer2[0]]):
		return
	
	if pincer1Type == "row" and pincer2Type == "col":
		if grid[pincer1[1]][pincer2[0]] == "_":
			for i in finalMarks:
				if i not in marksGrid[y][x]:
					marksGrid[pincer1[1]][pincer2[0]].discard(i)
	elif pincer1Type == "row" and pincer2Type == "box":
		targetBox = Box(pincer1[0], pincer1[1])
		for x2 in range(targetBox.leftBound, targetBox.rightBound):
			if grid[pincer2[1]][x2] == "_":
				for i in finalMarks:
					if i not in marksGrid[y][x]:
						marksGrid[pincer2[1]][x2].discard(i)
		del targetBox
	elif pincer1Type == "col" and pincer2Type == "box":
		targetBox = Box(pincer1[0], pincer1[1])
		for y2 in range(targetBox.lowerBound, targetBox.upperBound):
			if grid[y2][pincer2[0]] == "_":
				for i in finalMarks:
					if i not in marksGrid[y][x]:
						marksGrid[y2][pincer2[0]].discard(i)
		del targetBox

	prevPivots.append(pivot)

def skyscraper(x, y):
	for i in marksGrid[y][x]:
		#colIndex = None
		rowCandidates = 0 # H pattern
		colCandidates = 0 # I pattern
		#rowCandidates2 = 0
		colcandidates2 = []
		corner1 = (x, y)
		corner2 = None
		corner3 = None
		corner4 = None

		#Check first row/col of H or I
		for j in range(gridSize):
			if i in marksGrid[j][x]:
				rowCandidates += 1
			if i in marksGrid[y][j]:
				colCandidates += 1
		
		if rowCandidates != 2 and colCandidates != 2 or rowCandidates == colCandidates:
			continue
		
		#Go along middle path of H or I
		if rowCandidates == 2:
			row = None
			for x2 in range(gridSize):
				if i in marksGrid[y][x2]:
					rowCandidates2 = 0
					for y2 in range(gridSize):
						if i in marksGrid[y2][x2]:
							rowCandidates2 += 1
					if rowCandidates2 == 2:
						row = x2
						break
			#print(f"Row {row}: {rowCandidates2}")
			# for y2 in range(gridSize):
			# 	if i in marksGrid[y2][row]:
			# 		print(f"{x, y}, {row, y}, {row, y2}, {x, y2}")


		# if rowCandidates == 2:
		# 	for x2 in range(gridSize):
		# 		if i in marksGrid[y][x2]:
		# 			rowCandidatesList = []
		# 			for y2 in range(gridSize):
		# 				if i in marksGrid[y2][x2]:
		# 					if x == x2 and y != y2: corner2 = (x, y2)
		# 					if x != x2 and y != y2: corner3 = (x2, y2)
		# 					if x != x2 and y == y2: corner4 = (x2, y)
		# 					rowCandidatesList.append(y2)
		# 					if len(rowCandidatesList) > 2:
		# 						break
		# 			if len(rowCandidatesList) != 2:
		# 				continue
					#print(f"Candidate Y values for x = {x2} for mark {i}: {rowCandidatesList}")
					#corner3 = (x2, y)
					#corner4 = (x2, y2)
			#print(f"{corner1}, {corner2}, {corner3}, {corner4}\n")
		
		if colCandidates == 2:
			for y2 in range(gridSize):
				if i in marksGrid[y2][x] and y2 != y:
					corner2 = (x, y2)
		


		#breakJloop = False
		# for j in range(gridSize):
		# 	if i in marksGrid[y][j]:
		# 		colCandidates = 0
		# 		for y2 in range(gridSize):
		# 			if i not in marksGrid[y2][j]:
		# 				continue
		# 			colCandidates += 1
		# 			if colCandidates > 2:
		# 				break
		# 			if j == x and y2 != y:
		# 				corner3 = (j, y2)
		# 			else:
		# 			#corner2 = (j, y)
		# 			#corner4 = (x, y2)
		# 			colcandidates2.append(y2)
		# 		if len(colcandidates2) != 2:
		# 	if i in marksGrid[j][x]:
		# 		rowCandidates = 0
		# 		for x2 in range(gridSize):
		# 			if i in marksGrid[j][x2]:
		# 				rowCandidates += 1
		# 				if rowCandidates > 2:
		# 					break
		# 		if rowCandidates == 2:
		# 			corner2 = (x, j)
		# 			corner3 = (x2, j)
		# 			corner4 = (x2, y)
		
		#print(f"Vague possibility for {i} at {corner1}, {corner2}, {corner3}, {corner4}")

		if(rowCandidates != 2 and colCandidates != 2
		or not (corner1 and corner2 and corner3 and corner4)
		or corner1 == corner2
		or corner1 == corner3
		or corner1 == corner4
		or corner2 == corner3
		or corner2 == corner4
		or corner3 == corner4
		or grid[corner2[1]][corner2[0]] != "_"
		or grid[corner3[1]][corner3[0]] != "_"
		or grid[corner4[1]][corner4[0]] != "_"):
			continue

		#print(f"Possibility for {i} at {corner1}, {corner2}, {corner3}, {corner4}")

		#Check for roof of skyscraper
		straightSides = 0
		if colCandidates == 2:
			if corner1[1] == corner2[1]: straightSides += 1
			if corner1[0] == corner4[0]: straightSides += 1
			if corner2[0] == corner3[0]: straightSides += 1
			if corner3[1] == corner4[1]: straightSides += 1
		if rowCandidates == 2:
			if corner1[0] == corner2[0]: straightSides += 1
			if corner1[1] == corner4[1]: straightSides += 1
			if corner2[1] == corner3[1]: straightSides += 1
			if corner3[0] == corner4[0]: straightSides += 1
		
		if straightSides != 3:
			continue
		
		#print(f"Skyscraper for {i} at {corner1}, {corner2}, {corner3}, {corner4}")

		if rowCandidates == 2:
			pass

#If row and col both have two of a number, remove number from intersection
def twoStringKite(x, y):
	box = Box(x, y)
	for i in marksGrid[y][x]:
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
			if i in marksGrid[y][j]:
				horizCt += 1
				if j != x:
					horizEnd = (j, y)
			if i in marksGrid[j][x]:
				vertCt += 1
				if j != y:
					vertEnd = (x, j)
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
				if i in marksGrid[y2][x2]:
					start2 = (x2, y2)
					for j in range(gridSize):
						if i in marksGrid[y2][j] and firstIsHorizontal and not firstIsVertical:
							horizCt2 += 1
							if j != x2:
								horizEnd = (j, y2)
						if i in marksGrid[j][x2] and firstIsVertical and not firstIsHorizontal:
							vertCt2 += 1
							if j != y2:
								vertEnd = (x2, j)
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
		if grid[targetY][targetX] == "_" and i in marksGrid[targetY][targetX]:
				marksGrid[targetY][targetX].remove(i)
	del box

validateGrid()
print("Starting grid:")
printGrid(False)
startTime = time.perf_counter()
for x in range(gridSize):
	for y in range(gridSize):
		if grid[y][x] == "_":

			#Mark current row
			currGroup = set()
			for x2 in range(gridSize):
				inspectedSpace = grid[y][x2]
				if inspectedSpace != "_":
					currGroup.add(inspectedSpace)
			marksGrid[y][x] = charSet - currGroup

			#Mark current column
			currGroup = set()
			for y2 in range(gridSize):
				inspectedSpace = grid[y2][x]
				if inspectedSpace != "_":
					currGroup.add(inspectedSpace)
			marksGrid[y][x] -= currGroup

			#Mark current box
			box = Box(x, y)
			currGroup = set()
			for x2 in range(box.leftBound, box.rightBound):
				for y2 in range(box.lowerBound, box.upperBound):
					inspectedSpace = grid[y2][x2]
					if inspectedSpace != "_":
						currGroup.add(inspectedSpace)
			marksGrid[y][x] -= currGroup
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
			if grid[y][x] == "_":

				placeNumbers(x, y)

				if grid[y][x] in charSet:
					continue

				checkSubsets(x, y)
				checkBrokenSets(x, y)
				checkLockedCandidate1(x, y)
				checkLockedCandidate2(x, y)
				xWing(x, y)
				if len(marksGrid[y][x]) == 2:
					yWing(x, y)
				skyscraper(x, y)
				twoStringKite(x, y)

				if marksGrid[y][x] == set():
					print(f"Error: all marks removed from {x, y} on loop {loopCt}")
					print(f"Before: {prevMarksGrid[y][x]}\nAfter:  {marksGrid[y][x]}")
					quit()

	printGrid(False)
	validateGrid()
	printMarksGrid()
	print()

	if prevGrid == grid and prevMarksGrid == marksGrid:
		print(f"\nPuzzle not solved ({loopCt} loops)")
		quit()

	#Check completion
	complete = True
	for x in range(gridSize):
		for y in range(gridSize):
			if grid[y][x] == "_":
				complete = False

endTime = time.perf_counter()

validateGrid()
printGrid(False)
print(f"Puzzle solved in {loopCt} loops")
print(f"Compute time: {((endTime - startTime) * 1000):.2f} ms ({((endTime - startTime)):.1f} sec)")