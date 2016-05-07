import sys, json

import pickle

from sklearn.feature_extraction import DictVectorizer

def get_features(para, max_count = None):
	result = []
	cands = para.strip().split('.')
	r = cands[0]
	for c in range(0, len(cands) - 1):
	# if not cands[c]:
	# 	continue
	# print len(cands[c])
	# print cands[c].strip()
	# print '---'

		cur = {}
		cur["prev_len"] = len(cands[c - 1])
		cur["starts_with_space"] = int(cands[c].startswith(' '))
		if len(cands) > c + 2:
			if cands[c + 1] == '.' and cands[c + 2] == '.':
				cur["is_elipsis"] = 1
			else:
				cur["is_elipsis"] = 0
		else:
			cur["is_elipsis"] = 0

		if len(cands) > c + 1 and cands[c + 1] and cands[c + 1][0].isupper():
			cur["next_is_upper"] = 1
		else:
			cur["next_is_upper"] = 0

		if c + 1 == len(cands):
			cur["is_end"] = 1
		else:
			cur["is_end"] = 0

		if c - 1 > 0 and cands[c - 1][-1]
		# cur["prec_words"] = len(cands[c].split(' '))




		cur["len"] = len(cands[c])
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
		print json.dumps(splitParagraph(s.strip()), ensure_ascii=False)

