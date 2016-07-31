import sys
file_name = sys.argv[1]

inp = file(file_name + '.txt', 'r')
lines = inp.readlines()
inp.close()

oup = file(file_name + '_simp.txt', 'w')

def get_cmd(i):
	return lines[i].split(' ')[1]

for i in range(0, len(lines)):
	lines[i] = lines[i].replace('\n', '')
	
	if get_cmd(i) != 'pos':
		oup.write(lines[i] + '\n')
