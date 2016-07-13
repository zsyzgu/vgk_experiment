file_name = 'user1468283398_normal_0.8_1'
inp = file(file_name + '.txt', 'r')
lines = inp.readlines()
inp.close()

def get_cmd(i):
	return lines[i].split(' ')[1]

for i in range(0, len(lines)):
	lines[i] = lines[i].replace('\n', '')
	
	if get_cmd(i) != 'pos':
		print lines[i]
