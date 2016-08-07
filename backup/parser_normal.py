import sys
file_name = sys.argv[1]
MAXN = 10000;

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
oup.write('session, phrase, word, len, perform_time, total_time\n')

word_cnt = 0
letter_cnt = 0
total_time = 0
session_start = [0 for i in range(0, MAXN)]
phrase_start = [0 for i in range(0, MAXN)]
start_time = [-1 for i in range(0, MAXN)]
end_time = [-1 for i in range(0, MAXN)]
words = ['' for i in range(0, MAXN)]
phrases = ['' for i in range(0, MAXN)]

for i in range(0, len(lines)):
	lines[i] = lines[i].replace('\n', '')

	if get_cmd(i) == 'phrase':
		phrase_start[word_cnt] = 1
		phrases[word_cnt] = get_result(i)
	
	if get_cmd(i) == 'session':
		session_start[word_cnt] = 1

	if get_cmd(i) == 'gestureStart':
		if start_time[word_cnt] == -1 or phrase_start[word_cnt] == 1:
			start_time[word_cnt] = get_time(i)
	
	if get_cmd(i) == 'gestureEnd':
		end_time[word_cnt] = get_time(i)
		words[word_cnt] = get_result(i)
		word_cnt = word_cnt + 1
	
	if get_cmd(i) == 'select':
		end_time[word_cnt - 1] = get_time(i)
		words[word_cnt - 1] = get_result(i)

	if get_cmd(i) == 'delete':
		if phrase_start[word_cnt] == 0:
			word_cnt = word_cnt - 1

session_index = 0
phrase_index = 0
for i in range(0, word_cnt):
	if i == word_cnt - 1 or session_start[i + 1] == 1:
		rate = letter_cnt / total_time * 12
		err = 0
		print 'rate=' + str(rate) + ', err=' + str(err)
		letter_cnt = 0
		total_time = 0

	if session_start[i] == 1:
		session_index = session_index + 1
		phrase_index = 0
	if phrase_start[i] == 1:
		phrase_index = phrase_index + 1

	word = words[i]
	word_len = len(word)
	perform_time = end_time[i] - start_time[i]
	if phrase_start[i] == 1 or i == 0:
		word_time = end_time[i] - start_time[i]
	else:
		word_time = end_time[i] - end_time[i - 1]

	oup.write(str(session_index) + ', ' + str(phrase_index) + ', ' + word + ', ' + str(word_len) + ', ' + str(perform_time) + ', ' + str(word_time) + '\n')
	letter_cnt = letter_cnt + word_len
	total_time = total_time + word_time

oup.close()
