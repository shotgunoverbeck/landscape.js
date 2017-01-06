size = str(input('Dimensions: ')).split(' ')
tile = str(input('Default Tile: '))

import datetime
current_time = datetime.datetime.now()
filename = str(current_time.year) + '_' + str(current_time.month) + '_' + str(current_time.day) + ' ' + str(current_time.hour) + '_' + str(current_time.minute) + '_' + str(current_time.second) + ' BLANK.js'

output = []
output.append('var landscape = [\n')

standardLine = '['
for x in range(0, int(size[0])-1):
	standardLine += '[\''+tile+'\'], '
standardLine += '[\''+tile+'\']]'

for y in range(0, int(size[1])-1):
	output.append(standardLine + ',\n')
output.append(standardLine + '\n];')

output = ''.join(output)
f = open(filename,'w')
f.write(output)
f.close()
input('Done')