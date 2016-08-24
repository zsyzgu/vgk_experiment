MAXN = 10000;
import sys
import msd
import my_pos
file_name = sys.argv[1]
user_name = file_name.split('_')[0]
technique = file_name.split('_')[1]
session_index = 0

def get_time(i):
	return (float)(lines[i].split(' ')[0])

def get_cmd(i):
	return lines[i].split(' ')[1]

def get_result(i):
	tags = lines[i].split(' ')
	return ' '.join(tags[2 : len(tags)])

def write_undo():
	global undo_cnt
	for i in range(0, undo_cnt):
		woup.write(undo_buffer[i])
	undo_cnt = 0

def get_word_by_index(phrase, i):
	phrase_tags = phrase.split(' ')
	if i < len(phrase_tags):
		return phrase_tags[i]
	else:
		return ''

def word_output(i, std_word, word, is_undo):
	if std_word == word:
		correct = 'Yes'
	else:
		correct = 'No'
	if technique == 'normal':
		gesture_durations = gesture_end_time[i] - gesture_start_time[i]
		if select_word[i] == 1:
			word_class = 'Select'
			selection_durations = end_time[i] - gesture_end_time[i]
		else:
			word_class = 'Match'
			selection_durations = 0
		if is_undo == 1:
			word_class = 'Undo'
		sample_distance = my_pos.caln_sample_dist(gesture_pos[i], std_word)
		start_distance = my_pos.caln_dist(gesture_pos[i][0], my_pos.get_pos(std_word[0]))
		end_distance = my_pos.caln_dist(gesture_pos[i][len(gesture_pos[i]) - 1], my_pos.get_pos(std_word[len(std_word) - 1]))
		gesture_length = my_pos.caln_length(gesture_pos[i])
		gesture_speed = gesture_length / gesture_durations
		return user_name + ', ' + technique + ', ' + str(session_index) + ', ' + std_word + ', ' + str(len(std_word)) + ', ' + word_class + ', ' + correct + ', ' + str(gesture_durations) + ', ' + str(selection_durations) + ', ' + str(sample_distance) + ', ' + str(start_distance) + ', ' + str(end_distance) + ', ' + str(gesture_length) + ', ' + str(gesture_speed) + '\n'

inp = file(file_name + '.txt', 'r')
lines = inp.readlines()
inp.close()

oup = file('result_' + file_name + '.txt', 'w')
oup.write('user, technique, session, index, phrase, rate, error, undo\n')

if technique == 'normal':
	woup = file('gesture_' + file_name + '.txt', 'w')
	woup.write('user, technique, session, word, len, class, correct, gesture_durations, selection_durations, sample_distance, start_distance, end_distance, gesture_length, gesture_speed\n')

word_cnt = 0
undo_cnt = 0
curr_phrase_index = 0
session_start = [0 for i in range(0, MAXN)]
phrase_start = [0 for i in range(0, MAXN)]
phrase_undo = [0 for i in range(0, MAXN)]
select_word = [0 for i in range(0, MAXN)]
start_time = [-1 for i in range(0, MAXN)]
gesture_start_time = [-1 for i in range(0, MAXN)]
gesture_end_time = [-1 for i in range(0, MAXN)]
gesture_pos = [[] for i in range(0, MAXN)]
end_time = [-1 for i in range(0, MAXN)]
words = ['' for i in range(0, MAXN)]
phrases = ['' for i in range(0, MAXN)]
undo_buffer = ['' for i in range(0, MAXN)]

if technique == 'normal':
	for i in range(0, len(lines)):
		lines[i] = lines[i].replace('\n', '')

		if get_cmd(i) == 'session':
			session_index = session_index + 1
			session_start[word_cnt] = 1

		if get_cmd(i) == 'phrase':
			write_undo()
			phrase_start[word_cnt] = 1
			phrases[word_cnt] = get_result(i)
			curr_phrase_index = word_cnt

		if get_cmd(i) == 'gestureStart':
			if start_time[word_cnt] == -1 or phrase_start[word_cnt] == 1:
				start_time[word_cnt] = get_time(i)
			gesture_start_time[word_cnt] = get_time(i)
			gesture_end_time[word_cnt] = -1
			gesture_pos[word_cnt] = []
		
		if get_cmd(i) == 'pos':
			if gesture_end_time[word_cnt] == -1:
				gesture_pos[word_cnt].append(my_pos.ana_pos(get_result(i)))
		
		if get_cmd(i) == 'gestureEnd':
			gesture_end_time[word_cnt] = end_time[word_cnt] = get_time(i)
			words[word_cnt] = get_result(i)
			word_cnt = word_cnt + 1
		
		if get_cmd(i) == 'select':
			end_time[word_cnt - 1] = get_time(i)
			words[word_cnt - 1] = get_result(i)
			select_word[word_cnt - 1] = 1

		if get_cmd(i) == 'delete':
			if phrase_start[word_cnt] == 0:
				word_cnt = word_cnt - 1
				if phrase_start[word_cnt] == 1:
					undo_cnt = 0
					phrase_undo[word_cnt] = 1
				else:
					std_word = get_word_by_index(phrases[curr_phrase_index], word_cnt - curr_phrase_index)
					if std_word != '':
						undo_buffer[undo_cnt] = word_output(word_cnt, std_word, words[word_cnt], 1)
						undo_cnt = undo_cnt + 1
				select_word[word_cnt] = 0
				start_time[word_cnt] = -1
	write_undo()

if technique == 'baseline' or technique == 'dwell':
	for i in range(0, len(lines)):
		lines[i] = lines[i].replace('\n', '')

		if get_cmd(i) == 'session':
			if words[word_cnt] != '':
				end_time[word_cnt] = get_time(i - 1)
				word_cnt = word_cnt + 1
			session_start[word_cnt] = 1

		if get_cmd(i) == 'phrase':
			write_undo()
			if words[word_cnt] != '':
				end_time[word_cnt] = get_time(i - 1)
				word_cnt = word_cnt + 1
			phrase_start[word_cnt] = 1
			phrases[word_cnt] = get_result(i)
			curr_phrase_index = word_cnt

		if get_cmd(i) == 'letter' and get_result(i) == ' ':
			end_time[word_cnt] = get_time(i)
			word_cnt = word_cnt + 1

		if get_cmd(i) == 'select':
			words[word_cnt] = get_result(i)
			end_time[word_cnt] = get_time(i)
			select_word[word_cnt] = 1
			word_cnt = word_cnt + 1

		if get_cmd(i) == 'letter' and get_result(i) != ' ':
			if words[word_cnt] == '':
				if start_time[word_cnt] == -1 or phrase_start[word_cnt] == 1:
					start_time[word_cnt] = get_time(i)
				gesture_pos[word_cnt] = []
			words[word_cnt] = words[word_cnt] + get_result(i)
			gesture_end_time[word_cnt] = get_time(i)
		
		if get_cmd(i) == 'pos':
			if i > 0 and get_cmd(i - 1) == 'letter':
				gesture_pos[word_cnt].append(my_pos.ana_pos(get_result(i)))

		if get_cmd(i) == 'delete':
			if words[word_cnt] == '':
				if phrase_start[word_cnt] == 0:
					word_cnt = word_cnt - 1
					if phrase_start[word_cnt] == 1:
						undo_cnt = 0
						phrase_undo[word_cnt] = 1
					else:
						std_word = get_word_by_index(phrases[curr_phrase_index], word_cnt - curr_phrase_index)
						if std_word != '':
							undo_buffer[undo_cnt] = word_output(word_cnt, std_word, words[word_cnt], 1)
							undo_cnt = undo_cnt + 1
					words[word_cnt] = ''
					select_word[word_cnt] = 0
					start_time[word_cnt] = -1
			else:
				words[word_cnt] = words[word_cnt][0 : len(words[word_cnt]) - 1]
				gesture_pos[word_cnt] = gesture_pos[word_cnt][0 : len(gesture_pos[word_cnt]) - 1]
	if words[word_cnt] != '':
		end_time[word_cnt] = get_time(len(lines) - 1)
		word_cnt = word_cnt + 1
	write_undo()

letter_cnt = 0
total_time = 0
phrase = ''
std_phrase = ''
session_index = 0
phrase_index = 0
word_index = 0
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
		word_index = 0
		if phrase_undo[i] == 1:
			is_undo = 'Yes'
		else:
			is_undo = 'No'
	else:
		word_time = end_time[i] - end_time[i - 1]

	letter_cnt = letter_cnt + word_len
	total_time = total_time + word_time
	if phrase == '':
		phrase = word
	else:
		phrase = phrase + ' ' + word

	std_word = get_word_by_index(std_phrase, word_index)
	woup.write(word_output(i, std_word, word, 0))
	
	if i == word_cnt - 1 or phrase_start[i + 1] == 1:
		rate = letter_cnt / total_time * 12
		err = msd.msd(phrase, std_phrase)
		oup.write(user_name + ', ' + technique + ', ' + str(session_index) + ', ' + str(phrase_index) + ', ' + phrase + ', ' + str(rate) + ', ' + str(err) + ', ' + is_undo + '\n')
		letter_cnt = 0
		total_time = 0
		phrase = ''
	
	word_index = word_index + 1

oup.close()
woup.close()
