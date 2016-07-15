import os

files = os.listdir('.')

for file_name in files:
	tags = file_name.split('.')
	if len(tags) > 0 and tags[len(tags) - 1] == 'txt':
		print file_name
		os.system('python parser.py ' + '.'.join(tags[0 : len(tags) - 1]))
