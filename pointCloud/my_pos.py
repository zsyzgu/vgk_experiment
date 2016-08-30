METRIC_SAMPLE = 50
import math

def get_pos(letter):
	if letter == 'q': return (0.05, 0.6)
	if letter == 'w': return (0.15, 0.6)
	if letter == 'e': return (0.25, 0.6)
	if letter == 'r': return (0.35, 0.6)
	if letter == 't': return (0.45, 0.6)
	if letter == 'y': return (0.55, 0.6)
	if letter == 'u': return (0.65, 0.6)
	if letter == 'i': return (0.75, 0.6)
	if letter == 'o': return (0.85, 0.6)
	if letter == 'p': return (0.95, 0.6)
	if letter == 'a': return (0.1, 0.5)
	if letter == 's': return (0.2, 0.5)
	if letter == 'd': return (0.3, 0.5)
	if letter == 'f': return (0.4, 0.5)
	if letter == 'g': return (0.5, 0.5)
	if letter == 'h': return (0.6, 0.5)
	if letter == 'j': return (0.7, 0.5)
	if letter == 'k': return (0.8, 0.5)
	if letter == 'l': return (0.9, 0.5)
	if letter == 'z': return (0.15, 0.4)
	if letter == 'x': return (0.25, 0.4)
	if letter == 'c': return (0.35, 0.4)
	if letter == 'v': return (0.45, 0.4)
	if letter == 'b': return (0.55, 0.4)
	if letter == 'n': return (0.65, 0.4)
	if letter == 'm': return (0.75, 0.4)
	return (0, 0)

def ana_pos(str):
	tags = str.split(' ')
	return ((float)(tags[0]), (float)(tags[1]))

def caln_dist(A, B):
	return math.sqrt((A[0] - B[0]) * (A[0] - B[0]) + (A[1] - B[1]) * (A[1] - B[1])) * 10

def caln_length(pos_list):
	length = 0
	for i in range(0, len(pos_list) - 1):
		length = length + caln_dist(pos_list[i], pos_list[i + 1])
	return length

def caln_sample_dist(pos_list, str):
	word_pos_list = []
	for i in range(0, len(str)):
		word_pos_list.append(get_pos(str[i]))

	pos_list = sample_pos(pos_list)
	word_pos_list = sample_pos(word_pos_list)

	length = 0
	for i in range(0, len(pos_list)):
		length = length + caln_dist(pos_list[i], word_pos_list[i])
	length = length / len(pos_list)

	return length

def sample_pos(pos_list):
	sample_list = []

	length = caln_length(pos_list) / (METRIC_SAMPLE - 1)

	u = 0
	left = 0
	for i in range(0, METRIC_SAMPLE):
		while u + 1 < len(pos_list) and caln_dist(pos_list[u], pos_list[u + 1]) <= left:
			left = left - caln_dist(pos_list[u], pos_list[u + 1])
			u = u + 1
		if u + 1 < len(pos_list):
			k = left / caln_dist(pos_list[u], pos_list[u + 1])
			pos = (pos_list[u][0] + (pos_list[u + 1][0] - pos_list[u][0]) * k, pos_list[u][1] + (pos_list[u + 1][1] - pos_list[u][1]) * k)
		else:
			pos = pos_list[u]
		sample_list.append(pos)
		left = left + length
	
	return sample_list
