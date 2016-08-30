import os

def merge_files(file_class):
	files = os.listdir('.')
	oup = file(file_class + '.txt', 'w')

	first_file = True
	for file_name in files:
		if file_name[-len(file_class) : ] == file_class:
			inp = file(file_name, 'r')
			lines = inp.readlines()
			inp.close()
			os.remove(file_name)
			if first_file and len(lines) > 0:
				first_file = False
				oup.write(lines[0])
			for i in range(1, len(lines)):
				oup.write(lines[i])
	
	oup.close()

spec_files = ['rst']

files = os.listdir('.')

for file_name in files:
	tags = file_name.split('.')
	if len(tags) > 0 and tags[len(tags) - 1] == 'txt':
		flag = True
		for file_class in spec_files:
			if len(file_class) < len(file_name) and file_name[0 : len(file_class)] == file_class:
				flag = False
		if flag:
			print file_name
			os.system('python parser.py ' + '.'.join(tags[0 : len(tags) - 1]))

for file_class in spec_files:
	merge_files(file_class)
