def saveMap():
	import datetime
	current_time = datetime.datetime.now()
	filename = str(current_time.year) + '_' + str(current_time.month) + '_' + str(current_time.day) + ' ' + str(current_time.hour) + '_' + str(current_time.minute) + '_' + str(current_time.second) + '.js'
	print('Map saving...')

	#minimize hanging 0s in layers
	for x in range(0, len(landscape)):
		for y in range(0, len(landscape[0])):
			while landscape[x][y][len(landscape[x][y])-1] == 0:
				landscape[x][y].pop()

	output = []
	output.append('var landscape = [')
	for line in landscape:
		output.append(str(line) + ',')
	output[len(output)-1] = output[len(output)-1][:-1]
	output.append(']')

	output = '\n'.join(output)
	f = open(filename,'w')
	f.write(output)
	f.close()
	print('Map saved as: '+filename)

def drawMap():
	display.delete(tk.ALL)
	boxSize = int(boxSizeVar.get())
	boxCoordX = int(boxCoordVarX.get())
	boxCoordY = int(boxCoordVarY.get())
	boxNumber = int(displaySize / boxSize)
	layer = int(layerVar.get())
	for x in range(0, boxNumber):
		if x + boxCoordX >= len(landscape[0]):
			continue
		for y in range(0, boxNumber):
			if y + boxCoordY >= len(landscape):
				continue
			baseX = x * boxSize
			baseY = y * boxSize
			usingLayer = layer
			if layer >= len(landscape[boxCoordX+x][boxCoordY+y]):
				usingLayer = len(landscape[boxCoordX+x][boxCoordY+y]) - 1
			while landscape[boxCoordX+x][boxCoordY+y][usingLayer] == 0 and usingLayer > 0:
				usingLayer -= 1
			display.create_rectangle(baseX, baseY, baseX + boxSize, baseY + boxSize, fill='#' + landscape[boxCoordX+x][boxCoordY+y][usingLayer], width=1)

def paintTile(x, y):
	boxSize = int(boxSizeVar.get())
	boxCoordX = int(boxCoordVarX.get())
	boxCoordY = int(boxCoordVarY.get())
	boxClickedX = boxCoordX + int(x / boxSize)
	boxClickedY = boxCoordY + int(y / boxSize)
	layer = int(layerVar.get())
	paintingColor = currentPaintingEntryVar.get().upper()

	while len(landscape[boxClickedX][boxClickedY]) <= layer:
		landscape[boxClickedX][boxClickedY].append(0)

	if eraseVar.get():
		if layer != 0:
			landscape[boxClickedX][boxClickedY][layer] = 0
			drawMap()
		else:
			print('Cannot erase layer 0')
			return
	else:
		baseX = int(x / boxSize) * boxSize
		baseY = int(y / boxSize) * boxSize
		landscape[boxClickedX][boxClickedY][layer] = paintingColor
		display.create_rectangle(baseX, baseY, baseX + boxSize, baseY + boxSize, fill='#' + paintingColor, width=1)

isClicking = False
def enableClick(event):
	global isClicking
	isClicking = True
	paintTile(event.x, event.y)

def disableClick(event):
	global isClicking
	isClicking = False

def changeHover(event):
	boxSize = int(boxSizeVar.get())
	boxCoordX = int(boxCoordVarX.get())
	boxCoordY = int(boxCoordVarY.get())
	boxClickedX = boxCoordX + int(event.x / boxSize)
	boxClickedY = boxCoordY + int(event.y / boxSize)
	boxNumber = int(displaySize / boxSize)
	if boxClickedX >= len(landscape) or boxClickedY >= len(landscape[0]) or boxClickedX < 0 or boxClickedY < 0:
		return
	layer = int(layerVar.get())
	usingLayer = layer
	if layer >= len(landscape[boxClickedX][boxClickedY]):
		usingLayer = len(landscape[boxClickedX][boxClickedY]) - 1
	while landscape[boxClickedX][boxClickedY][usingLayer] == 0 and usingLayer > 0:
		usingLayer -= 1
	if boxClickedX < len(landscape[0]) and boxClickedY < len(landscape):
		hoveringLabelPos['text'] = str(boxClickedX) + ', ' + str(boxClickedY) + ', ' + str(usingLayer)
		hoveringLabelColor['text'] = landscape[boxClickedX][boxClickedY][usingLayer]
		if isClicking:
			paintTile(event.x, event.y)

rightClicks = ['NONE', 'NONE']
def rightClickSet(event):
	global rightClicks
	boxSize = int(boxSizeVar.get())
	boxCoordX = int(boxCoordVarX.get())
	boxCoordY = int(boxCoordVarY.get())
	boxClickedX = boxCoordX + int(event.x / boxSize)
	boxClickedY = boxCoordY + int(event.y / boxSize)
	if rightClicks[0] == 'NONE':
		rightClicks[0] = [boxClickedX, boxClickedY]
		rightClickLabel1['text'] = rightClicks[0]
	elif rightClicks[1] == 'NONE':
		rightClicks[1] = [boxClickedX, boxClickedY]
		rightClickLabel2['text'] = rightClicks[1]

		lowX = min(rightClicks[0][0], rightClicks[1][0])
		highX = max(rightClicks[0][0], rightClicks[1][0])
		lowY = min(rightClicks[0][1], rightClicks[1][1])
		highY = max(rightClicks[0][1], rightClicks[1][1])

		paintingColor = currentPaintingEntryVar.get().upper()
		layer = int(layerVar.get())
		if eraseVar.get():
			if layer != 0:
				paintingColor = 0
			else:
				print('Cannot erase layer 0')
				rightClicks = ['NONE', 'NONE']
				rightClickLabel1['text'] = rightClicks[0]
				rightClickLabel2['text'] = rightClicks[1]
				return

		for x in range(lowX, highX+1):
			for y in range(lowY, highY+1):
				while len(landscape[x][y]) <= layer:
					landscape[x][y].append(0)
				landscape[x][y][layer] = paintingColor

		drawMap()
		rightClicks = ['NONE', 'NONE']
		rightClickLabel1['text'] = rightClicks[0]
		rightClickLabel2['text'] = rightClicks[1]

def maskDraw(falseArgument=False):
	drawMap()
	print('Map redrawn')

#load initial map
print('Loading Map...')
while True:
	try:
		with open(input('Map Filename: ')) as f:
			landscape = f.readlines()
			break
	except:
		print('No such file')
print('Map read...')
landscape.pop(0)
landscape.pop(len(landscape)-1)
print('Map processing...')
for index, item in enumerate(landscape):
	item = item.rstrip()
	landscape[index] = item
landscape = eval(''.join(landscape)) #okay, yes, evals are evil. But it works.
print('Map loaded')

print('Building interface...')
import tkinter as tk

#make window
root = tk.Tk()
root.wm_title = 'World Builder'
root.resizable(0,0)

displaySize = 900
display = tk.Canvas(root, width=displaySize, height=displaySize)
display.bind('<ButtonPress-1>', enableClick)
display.bind('<ButtonRelease-1>', disableClick)
display.bind('<ButtonPress-3>', rightClickSet)
display.bind('<Motion>', changeHover)
display.grid(row=0, column=0, rowspan=100)
tk.Button(root, text='Save Map', fg='red', command=saveMap).grid(row=0, column=1, sticky=tk.NW)
tk.Button(root, text='Draw Map', command=drawMap).grid(row=0, column=2, sticky=tk.NW)
tk.Label(root, text=' ').grid(row=1, column=1)
tk.Label(root, text='Top-Left Box Coords:').grid(row=2, column=1, columnspan=2, sticky=tk.NW)

boxCoordVarX = tk.StringVar()
boxCoordVarX.set(0)
boxCoordEntryX = tk.Entry(root, textvariable=boxCoordVarX, width=10)
boxCoordEntryX.bind('<Return>', maskDraw)
boxCoordEntryX.grid(row=3, column=1, sticky=tk.NW)

boxCoordVarY = tk.StringVar()
boxCoordVarY.set(0)
boxCoordEntryY = tk.Entry(root, textvariable=boxCoordVarY, width=10)
boxCoordEntryY.bind('<Return>', maskDraw)
boxCoordEntryY.grid(row=3, column=2, sticky=tk.NW)

tk.Label(root, text='Box Size:').grid(row=4, column=1, sticky=tk.NW)
boxSizeVar = tk.StringVar()
boxSizeEntry = tk.Entry(root, textvariable=boxSizeVar, width=10)
boxSizeEntry.bind('<Return>', maskDraw)
boxSizeEntry.grid(row=4, column=2, sticky=tk.NW)
boxSizeVar.set(15)

tk.Label(root, text='Layer:').grid(row=5, column=1, sticky=tk.NW)
layerVar = tk.StringVar()
layerEntry = tk.Entry(root, textvariable=layerVar, width=10)
layerEntry.bind('<Return>', maskDraw)
layerEntry.grid(row=5, column=2, sticky=tk.NW)
layerVar.set(0)

tk.Label(root, text=' ').grid(row=6, column=1)

tk.Label(root, text='Currently Painting:').grid(row=7, column=1, columnspan=2, sticky=tk.NW)
currentPaintingEntryVar = tk.StringVar()
currentPaintingEntry = tk.Entry(root, width=20, textvariable=currentPaintingEntryVar)
currentPaintingEntry.grid(row=8, column=1, columnspan=2, sticky=tk.NW)
currentPaintingEntryVar.set('000000')

def paintEntry1Set(falseArgument=False):
	currentPaintingEntryVar.set(paintEntryVar1.get())
	paintEntry1['bg'] = '#' + paintEntryVar1.get()
paintEntryVar1 = tk.StringVar()
paintEntry1 = tk.Entry(root, width=10, textvariable=paintEntryVar1)
paintEntry1.bind('<Return>', paintEntry1Set)
paintEntry1.grid(row=9, column=1, sticky=tk.NW)
tk.Button(text='Set', command=paintEntry1Set).grid(row=9, column=2, sticky=tk.NW)

def paintEntry2Set(falseArgument=False):
	currentPaintingEntryVar.set(paintEntryVar2.get())
	paintEntry2['bg'] = '#' + paintEntryVar2.get()
paintEntryVar2 = tk.StringVar()
paintEntry2 = tk.Entry(root, width=10, textvariable=paintEntryVar2)
paintEntry2.bind('<Return>', paintEntry2Set)
paintEntry2.grid(row=10, column=1, sticky=tk.NW)
tk.Button(text='Set', command=paintEntry2Set).grid(row=10, column=2, sticky=tk.NW)

def paintEntry3Set(falseArgument=False):
	currentPaintingEntryVar.set(paintEntryVar3.get())
	paintEntry3['bg'] = '#' + paintEntryVar3.get()
paintEntryVar3 = tk.StringVar()
paintEntry3 = tk.Entry(root, width=10, textvariable=paintEntryVar3)
paintEntry3.bind('<Return>', paintEntry3Set)
paintEntry3.grid(row=11, column=1, sticky=tk.NW)
tk.Button(text='Set', command=paintEntry3Set).grid(row=11, column=2, sticky=tk.NW)

def paintEntry4Set(falseArgument=False):
	currentPaintingEntryVar.set(paintEntryVar4.get())
	paintEntry4['bg'] = '#' + paintEntryVar4.get()
paintEntryVar4 = tk.StringVar()
paintEntry4 = tk.Entry(root, width=10, textvariable=paintEntryVar4)
paintEntry4.bind('<Return>', paintEntry4Set)
paintEntry4.grid(row=12, column=1, sticky=tk.NW)
tk.Button(text='Set', command=paintEntry4Set).grid(row=12, column=2, sticky=tk.NW)

def paintEntry5Set(falseArgument=False):
	currentPaintingEntryVar.set(paintEntryVar5.get())
	paintEntry5['bg'] = '#' + paintEntryVar5.get()
paintEntryVar5 = tk.StringVar()
paintEntry5 = tk.Entry(root, width=10, textvariable=paintEntryVar5)
paintEntry5.bind('<Return>', paintEntry5Set)
paintEntry5.grid(row=13, column=1, sticky=tk.NW)
tk.Button(text='Set', command=paintEntry5Set).grid(row=13, column=2, sticky=tk.NW)

def paintEntry6Set(falseArgument=False):
	currentPaintingEntryVar.set(paintEntryVar6.get())
	paintEntry6['bg'] = '#' + paintEntryVar6.get()
paintEntryVar6 = tk.StringVar()
paintEntry6 = tk.Entry(root, width=10, textvariable=paintEntryVar6)
paintEntry6.bind('<Return>', paintEntry6Set)
paintEntry6.grid(row=14, column=1, sticky=tk.NW)
tk.Button(text='Set', command=paintEntry6Set).grid(row=14, column=2, sticky=tk.NW)

def paintEntry7Set(falseArgument=False):
	currentPaintingEntryVar.set(paintEntryVar7.get())
	paintEntry7['bg'] = '#' + paintEntryVar7.get()
paintEntryVar7 = tk.StringVar()
paintEntry7 = tk.Entry(root, width=10, textvariable=paintEntryVar7)
paintEntry7.bind('<Return>', paintEntry7Set)
paintEntry7.grid(row=15, column=1, sticky=tk.NW)
tk.Button(text='Set', command=paintEntry7Set).grid(row=15, column=2, sticky=tk.NW)

def paintEntry8Set(falseArgument=False):
	currentPaintingEntryVar.set(paintEntryVar8.get())
	paintEntry8['bg'] = '#' + paintEntryVar8.get()
paintEntryVar8 = tk.StringVar()
paintEntry8 = tk.Entry(root, width=10, textvariable=paintEntryVar8)
paintEntry8.bind('<Return>', paintEntry8Set)
paintEntry8.grid(row=16, column=1, sticky=tk.NW)
tk.Button(text='Set', command=paintEntry8Set).grid(row=16, column=2, sticky=tk.NW)

def paintEntry9Set(falseArgument=False):
	currentPaintingEntryVar.set(paintEntryVar9.get())
	paintEntry9['bg'] = '#' + paintEntryVar9.get()
paintEntryVar9 = tk.StringVar()
paintEntry9 = tk.Entry(root, width=10, textvariable=paintEntryVar9)
paintEntry9.bind('<Return>', paintEntry9Set)
paintEntry9.grid(row=17, column=1, sticky=tk.NW)
tk.Button(text='Set', command=paintEntry9Set).grid(row=17, column=2, sticky=tk.NW)

def paintEntry10Set(falseArgument=False):
	currentPaintingEntryVar.set(paintEntryVar10.get())
	paintEntry10['bg'] = '#' + paintEntryVar10.get()
paintEntryVar10 = tk.StringVar()
paintEntry10 = tk.Entry(root, width=10, textvariable=paintEntryVar10)
paintEntry10.bind('<Return>', paintEntry10Set)
paintEntry10.grid(row=18, column=1, sticky=tk.NW)
tk.Button(text='Set', command=paintEntry10Set).grid(row=18, column=2, sticky=tk.NW)

def populatePalette():
	tiles = []
	scores = []
	boxSize = int(boxSizeVar.get())
	boxCoordX = int(boxCoordVarX.get())
	boxCoordY = int(boxCoordVarY.get())
	boxNumber = int(displaySize / boxSize)
	for x in range(0, boxNumber):
		if x + boxCoordX >= len(landscape[0]):
			continue
		for y in range(0, boxNumber):
			if y + boxCoordY >= len(landscape):
				continue
			for item in landscape[boxCoordX+x][boxCoordY+y]:
				tile = item
				if tile not in tiles:
					tiles.append(tile)
					scores.append(1)
				else:
					scores[tiles.index(tile)] += 1
	scores, tiles = (list(t) for t in zip(*sorted(zip(scores, tiles))))
	tiles = tiles[::-1]
	if len(tiles) >= 1:
		paintEntryVar1.set(tiles[0])
		paintEntry1['bg'] = '#' + paintEntryVar1.get()
	if len(tiles) >= 2:
		paintEntryVar2.set(tiles[1])
		paintEntry2['bg'] = '#' + paintEntryVar2.get()
	if len(tiles) >= 3:
		paintEntryVar3.set(tiles[2])
		paintEntry3['bg'] = '#' + paintEntryVar3.get()
	if len(tiles) >= 4:
		paintEntryVar4.set(tiles[3])
		paintEntry4['bg'] = '#' + paintEntryVar4.get()
	if len(tiles) >= 5:
		paintEntryVar5.set(tiles[4])
		paintEntry5['bg'] = '#' + paintEntryVar5.get()
	if len(tiles) >= 6:
		paintEntryVar6.set(tiles[5])
		paintEntry6['bg'] = '#' + paintEntryVar6.get()
	if len(tiles) >= 7:
		paintEntryVar7.set(tiles[6])
		paintEntry7['bg'] = '#' + paintEntryVar7.get()
	if len(tiles) >= 8:
		paintEntryVar8.set(tiles[7])
		paintEntry8['bg'] = '#' + paintEntryVar8.get()
	if len(tiles) >= 9:
		paintEntryVar9.set(tiles[8])
		paintEntry9['bg'] = '#' + paintEntryVar9.get()
	if len(tiles) >= 10:
		paintEntryVar10.set(tiles[9])
		paintEntry10['bg'] = '#' + paintEntryVar10.get()
eraseVar = tk.IntVar()
tk.Label(root, text='Erase:').grid(row=19, column=1, sticky=tk.NW)
tk.Checkbutton(root, variable=eraseVar).grid(row=19, column=2, sticky=tk.NW)
tk.Button(text='Populate Palette', command=populatePalette).grid(row=20, column=1, columnspan=2, sticky=tk.NW)

tk.Label(root, text=' ').grid(row=21, column=1)
tk.Label(root, text='Hovering Over:').grid(row=22, column=1, columnspan=2, sticky=tk.NW)
hoveringLabelColor = tk.Label(root, text='NONE')
hoveringLabelColor.grid(row=23, column=1, columnspan=2, sticky=tk.NW)
hoveringLabelPos = tk.Label(root, text='NONE')
hoveringLabelPos.grid(row=24, column=1, columnspan=2, sticky=tk.NW)

tk.Label(root, text=' ').grid(row=25, column=1)
tk.Label(root, text='Right-Clicks:').grid(row=26, column=1, columnspan=2, sticky=tk.NW)
rightClickLabel1 = tk.Label(root, text='NONE')
rightClickLabel1.grid(row=27, column=1, sticky=tk.NW)
rightClickLabel2 = tk.Label(root, text='NONE')
rightClickLabel2.grid(row=27, column=2, sticky=tk.NW)

print('Interface built')
print('Drawing map...')
drawMap()
print('Map drawn')
root.mainloop()