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
    	print cands[c].strip()
    	print '---'

        cur = {}
        cur["prev_len"] = len(cands[c - 1])
        cur["starts_with_space"] = int(cands[c].startswith(' '))
        cur["len"] = len(cands[c])
        result.append(cur)

        if max_count is not None and c >= max_count - 1:
        	break
        
    return result

def should_split(cands, position):
	current = cands[position]
	if len(current) > 10 and current.startswith(' '):
		return True
	return False

def splitParagraph(para):
	res = []

	cands = para.split('.')
	r = cands[0]
	for c in range(1, len(cands)):
		if should_split(cands, c):
			res.append(r + '.')
			r = cands[c]
		else:
			r += '.' + cands[c]
	res.append(r)

	return {'Paragraph': para, 'Sentences': res}


for s in sys.stdin:
	print json.dumps(splitParagraph(s.strip()), ensure_ascii=False)


