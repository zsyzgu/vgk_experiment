MAXN = 10000;
import sys
import msd
file_name = sys.argv[1]
userName = file_name.split('_')[0]
technique = file_name.split('_')[1]

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

oup = file('result_' + file_name + '.txt', 'w')
oup.write('user, technique, session, index, phrase, rate, error\n')

word_cnt = 0
session_start = [0 for i in range(0, MAXN)]
phrase_start = [0 for i in range(0, MAXN)]
start_time = [-1 for i in range(0, MAXN)]
end_time = [-1 for i in range(0, MAXN)]
words = ['' for i in range(0, MAXN)]
phrases = ['' for i in range(0, MAXN)]

if technique == 'normal':
	for i in range(0, len(lines)):
		lines[i] = lines[i].replace('\n', '')

		if get_cmd(i) == 'session':
			session_start[word_cnt] = 1

		if get_cmd(i) == 'phrase':
			phrase_start[word_cnt] = 1
			phrases[word_cnt] = get_result(i)

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

if technique == 'headOnly':
	for i in range(0, len(lines)):
		lines[i] = lines[i].replace('\n', '')
		
		if get_cmd(i) == 'session':
			session_start[word_cnt] = 1

		if get_cmd(i) == 'phrase':
			phrase_start[word_cnt] = 1
			phrases[word_cnt] = get_result(i)

		if get_cmd(i) == 'gestureStart':
			if start_time[word_cnt] == -1 or phrase_start[word_cnt] == 1:
				start_time[word_cnt] = get_time(i)
		
		if get_cmd(i) == 'select':
			end_time[word_cnt] = get_time(i)
			words[word_cnt] = get_result(i)
			word_cnt = word_cnt + 1

		if get_cmd(i) == 'delete':
			if phrase_start[word_cnt] == 0:
				word_cnt = word_cnt - 1

if technique == 'baseline' or technique == 'dwell':
	for i in range(0, len(lines)):
		lines[i] = lines[i].replace('\n', '')

		if get_cmd(i) == 'session':
			if words[word_cnt] != '':
				end_time[word_cnt] = get_time(i)
				word_cnt = word_cnt + 1
			session_start[word_cnt] = 1

		if get_cmd(i) == 'phrase':
			if words[word_cnt] != '':
				end_time[word_cnt] = get_time(i)
				word_cnt = word_cnt + 1
			phrase_start[word_cnt] = 1
			phrases[word_cnt] = get_result(i)

		if get_cmd(i) == 'letter' and get_result(i) == ' ':
			end_time[word_cnt] = get_time(i)
			word_cnt = word_cnt + 1

		if get_cmd(i) == 'select':
			words[word_cnt] = get_result(i)
			end_time[word_cnt] = get_time(i)
			word_cnt = word_cnt + 1

		if get_cmd(i) == 'letter' and get_result(i) != ' ':
			if words[word_cnt] == '':
				if start_time[word_cnt] == -1 or phrase_start[word_cnt] == 1:
					start_time[word_cnt] = get_time(i)
			words[word_cnt] = words[word_cnt] + get_result(i)
		
		if get_cmd(i) == 'delete':
			if words[word_cnt] == '':
				if phrase_start[word_cnt] == 0:
					word_cnt = word_cnt - 1
					words[word_cnt] = ''
			else:
				words[word_cnt] = words[word_cnt][0 : len(words[word_cnt]) - 1]
	end_time[word_cnt] = get_time(len(lines) - 1)
	word_cnt = word_cnt + 1

letter_cnt = 0
total_time = 0
phrase = ''
std_phrase = ''
session_index = 0
phrase_index = 0
for i in range(0, word_cnt):
	if session_start[i] == 1:
		session_index = session_index + 1
		phrase_index = 0

	word = words[i]
	word_len = len(word)
	if phrase_start[i] == 1:
		std_phrase = phrases[i]
		word_time = end_time[i] - start_time[i]
		phrase_index = phrase_index + 1
	else:
		word_time = end_time[i] - end_time[i - 1]

	letter_cnt = letter_cnt + word_len
	total_time = total_time + word_time
	if phrase == '':
		phrase = word
	else:
		phrase = phrase + ' ' + word
	
	if i == word_cnt - 1 or phrase_start[i + 1] == 1:
		rate = letter_cnt / total_time * 12
		err = msd.msd(phrase, std_phrase)
		oup.write(userName + ', ' + technique + ', ' + str(session_index) + ', ' + str(phrase_index) + ', ' + phrase + ', ' + str(rate) + ', ' + str(err) + '\n')
		letter_cnt = 0
		total_time = 0
		phrase = ''

oup.close()
