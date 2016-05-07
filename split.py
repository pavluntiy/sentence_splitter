import sys, json
import re

import pickle

from sklearn.feature_extraction import DictVectorizer

def get_features(para, max_count = None):
	para = para.strip()
	result = []

	# print para.__class__
	# cands = para.strip().split('.')

	positions = [m.start() for m in re.finditer(r'\.', para, re.UNICODE)]
	# r = cands[0]
	# print len(para)
	# print positions
	# raise ValueError()
	for idx, cur_pos in enumerate(positions):
	# if not cands[c]:
	# 	continue
	# print len(cands[c])
	# print cands[c].strip()
	# print '---'

		cur = {}
		if idx > 0 :
			cur["prev_len"] = cur_pos - positions[idx - 1]
			cur["prec_words"] = len(para[positions[idx - 1]: cur_pos].split(' '))
			cur["last_word_len"] = len(para[positions[idx - 1]: cur_pos].strip().split(' ')[-1])
		else:
			cur["prev_len"] = 0
			cur["prec_words"] = 0
			cur["last_word_len"] = 0

		# print cur["last_word_len"]


		cur["prev_is_brace"] = cur_pos > 1 and para[cur_pos] == ')'
		cur["prev_is_quote"] = cur_pos > 1 and para[cur_pos] == '"'
	
		
		cur["starts_with_space"] = cur_pos + 1 < len(para) and para[cur_pos + 1] == ' '


		# if idx + 1 < len(positions):


		tmp = para[cur_pos + 1:].strip()

		# print tmp.__class__

		# if tmp and tmp[0].isupper():
		# 	cur["next_is_upper"] = 1
		# else:
		# 	cur["next_is_upper"] = 0


		cur["next_is_upper"] = tmp and tmp[0].isupper()

		cur["is_elipsis"]  =  cur_pos + 2 < len(para) and para[cur_pos + 1] == '.' and para[cur_pos + 2] == '.'

		

		if cur_pos + 1 == len(para):
			cur["is_end"] = 1
		else:
			cur["is_end"] = 0

		# if c - 1 > 0 and cands[c - 1][-1]
		# cur["prec_words"] = len(cands[c].split(' '))



		if idx + 1 < len(positions):
			cur["len"] = positions[idx + 1] - cur_pos
		else:
			cur["len"] = len(para) - cur_pos

		result.append(cur)

		if max_count is not None and c >= max_count - 1:
			break

	return result



def should_split(para, cands, position):
	# current = cands[position]
	# if len(current) > 10 and current.startswith(' '):
	# 	return True
	# return False

	# print cands[position]

	# print para.__class__

	x = vectorizer.transform(get_features(para))
	result = model.predict(x)

	return result[position - 1]
	# return False

def splitParagraph(para):

	res = []



	cands = para.split('.')
	r = cands[0]
	for c in range(1, len(cands)):
		if should_split(para, cands, c):
			res.append(r + '.')
			r = cands[c]
		else:
			r += '.' + cands[c]
	res.append(r)

	return {'Paragraph': para, 'Sentences': res}




if __name__ == "__main__":
	model = pickle.load(open("model.pickle"))
	vectorizer = pickle.load(open("vectorizer.pickle"))

	for s in sys.stdin:
		result = splitParagraph(s.decode('utf-8').strip())
		print json.dumps(result)

