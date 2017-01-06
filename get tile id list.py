with open(input('Map Filename: ')) as f:
	landscape = f.readlines()
print('Map read...')
landscape.pop(0)
landscape.pop(len(landscape)-1)
print('Map processing...')
for index, item in enumerate(landscape):
	item = item.rstrip()
	if item[len(item)-1] == ',':
		item = item[:-1]
	item = item[2:]
	item = item[:-2]
	item = item.split('\', \'')
	landscape[index] = item
print('Finding tiles...')
tiles = []
for x in range(0, len(landscape[0])):
	for y in range(0, len(landscape)):
		if landscape[x][y] not in tiles:
			tiles.append(landscape[x][y])

output = '\n'.join(tiles)
f = open('tile list.txt','w')
f.write(output)
f.close()
input('Done')