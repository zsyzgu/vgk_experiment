import sys
file_name = sys.argv[1]
MAXN = 50000

def get_time(i):
	return (float)(lines[i].split(' ')[0])

def get_cmd(i):
	return lines[i].split(' ')[1]

def get_result(i):
	tags = lines[i].split(' ')
	return ' '.join(tags[2 : len(tags)])

inp = file(file_name + '.txt', 'r')
lines = inp.readlines()
inp.close()

oup = file(file_name + '_result.txt', 'w')
oup.write('letter, x0, y0, x, y\n')

letter_cnt = 0
phrase_start = [0 for i in range(0, MAXN)]
letters = ['' for i in range(0, MAXN)]
letterPos = ['' for i in range(0, MAXN)]
tapPos = ['' for i in range(0, MAXN)]

for i in range(0, len(lines)):
	lines[i] = lines[i].replace('\n', '')

	if get_cmd(i) == 'phrase':
		phrase_start[letter_cnt] = 1
		result = get_result(i)
		for j in range(0, len(result)):
			letters[letter_cnt + j] = result[j]

	if get_cmd(i) == 'letter':
		#letters[letter_cnt] = get_result(i)
		letter_cnt = letter_cnt + 1

	if get_cmd(i) == 'letterPos':
		letterPos[letter_cnt - 1] = ', '.join(get_result(i).split(' '))
	
	if get_cmd(i) == 'pos':
		tapPos[letter_cnt - 1] = ', '.join(get_result(i).split(' '))
	
	if get_cmd(i) == 'delete':
		if phrase_start[letter_cnt] == 0:
			if letters[letter_cnt - 1] == ' ':
				while True:
					letter_cnt = letter_cnt - 1
					if phrase_start[letter_cnt] == 1 or letters[letter_cnt - 1] == ' ':
						break
			else:
				letter_cnt = letter_cnt - 1

for i in range(0, letter_cnt):
	if (len(letterPos[i]) > 2 and len(tapPos[i]) > 2):
		oup.write(letters[i] + ', ' + letterPos[i] + ', ' + tapPos[i] + '\n')
