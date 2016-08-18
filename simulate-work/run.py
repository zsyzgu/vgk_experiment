import os

def merge_files(file_class):
	files = os.listdir('.')
	oup = file(file_class + '.txt', 'w')

	first_file = True
	for file_name in files:
		if len(file_class) < len(file_name) and file_name[0 : len(file_class)] == file_class and file_name[len(file_class)] == '_':
			inp = file(file_name, 'r')
			lines = inp.readlines()
			inp.close()
			os.remove(file_name)
			if first_file and len(lines) > 0:
				lines[0] = lines[0].replace('\n', '')
				oup.write(lines[0] + '\n')
				first_file = False
			for i in range(1, len(lines)):
				lines[i] = lines[i].replace('\n', '')
				oup.write(lines[i] + '\n')

	oup.close()

files = os.listdir('.')

for file_name in files:
	tags = file_name.split('.')
	if len(tags) > 0 and tags[len(tags) - 1] == 'txt' and file_name[0 : 7] != 'lexicon' and file_name[0 : 8] != 'simulate' and file_name[0 : 8] != 'position':
		print file_name
		os.system('python parser.py ' + '.'.join(tags[0 : len(tags) - 1]))

merge_files('simulate')
