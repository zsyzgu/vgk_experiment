import os

files = os.listdir('.')

for file_name in files:
	tags = file_name.split('.')
	if len(tags) > 0 and tags[len(tags) - 1] == 'txt' and file_name[0 : 6] != 'result':
		print file_name
		os.system('python parser.py ' + '.'.join(tags[0 : len(tags) - 1]))

oup = file('result.txt', 'w')

first_file = True
for file_name in files:
	if file_name[0 : 6] == 'result':
		inp = file(file_name, 'r')
		lines = inp.readlines()
		inp.close()
		if first_file and len(lines) > 0:
			lines[0] = lines[0].replace('\n', '')
			oup.write(lines[0] + '\n')
			first_file = False
		for i in range(1, len(lines)):
			lines[i] = lines[i].replace('\n', '')
			oup.write(lines[i] + '\n')

oup.close()
