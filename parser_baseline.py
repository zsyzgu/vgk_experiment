file_name = 'user1468092472_baseline_0.6_1'
MAXN = 10000

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
oup.write('word, len, time\n')

word_cnt = 0
letter_cnt = 0
delete_cnt = 0
delete_buff = 0
total_time = 0
word_time = 0
phrase_start = [0 for i in range(0, MAXN)]
start_time = [-1 for i in range(0, MAXN)]
end_time = [-1 for i in range(0, MAXN)]
words = ['' for i in range(0, MAXN)]

for i in range(0, len(lines)):
	lines[i] = lines[i].replace('\n', '')

	if (get_cmd(i) == 'letter' and get_result(i) == ' ') or (get_cmd(i) == 'phrase' and word_cnt != 0):
		end_time[word_cnt] = get_time(i)
		word_cnt = word_cnt + 1

	if get_cmd(i) == 'phrase':
		phrase_start[word_cnt] = 1
		delete_buff = 0

	if get_cmd(i) == 'letter' and get_result(i) != ' ':
		if words[word_cnt] == '':
			if start_time[word_cnt] == -1 or phrase_start[word_cnt] == 1:
				start_time[word_cnt] = get_time(i)
		words[word_cnt] = words[word_cnt] + get_result(i)
	
	if get_cmd(i) == 'delete':
		if words[word_cnt] == '':
			if phrase_start[word_cnt] == 0:
				delete_cnt = delete_cnt + len(words[word_cnt])
				delete_buff = delete_buff + len(words[word_cnt])
				word_cnt = word_cnt - 1
				words[word_cnt] = ''
			if phrase_start[word_cnt] == 1:
				delete_cnt = delete_cnt - delete_buff
				delete_buff = 0
		else:
			delete_cnt = delete_cnt + 1
			delete_buff = delete_buff + 1
			words[word_cnt] = words[word_cnt][0 : len(words[word_cnt]) - 1]

end_time[word_cnt] = get_time(len(lines) - 1)
word_cnt = word_cnt + 1

for i in range(0, word_cnt):
	word = words[i]
	word_len = len(word)
	if phrase_start[i] == 1 or i == 0:
		word_time = end_time[i] - start_time[i]
	else:
		word_time = end_time[i] - end_time[i - 1]
	
	oup.write(word + ', ' + str(word_len) + ', ' + str(word_time) + '\n')
	letter_cnt = letter_cnt + word_len
	total_time = total_time + word_time

rate = letter_cnt / total_time * 12
err = float(delete_cnt) / letter_cnt
oup.write('rate=' + str(rate) + ', err=' + str(err) + '\n')
oup.close()

print 'rate=' + str(rate) + ', err' + str(err) + '\n'
