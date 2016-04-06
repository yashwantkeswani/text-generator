import nltk
sent_tokenize = nltk.data.load('tokenizers/punkt/english.pickle')

import re
html_escape_table = {
	"&": "&amp;",
	'"': "&quot;",
	"'": "&apos;",
	">": "&gt;",
	"<": "&lt;"
	}

def html_escape(text):
	for i in html_escape_table:	
		text = re.sub(html_escape_table[i], i, text)
	return text





f = open("data_cleaned.txt", "r").readlines()

list_sentences = []
temp = []
for j in f:
	tokens2 = nltk.word_tokenize(j.strip())	
	tokens = []
	for i in tokens2:
		if i.lower() == 'ca':
			tokens.append(i+'n')
		elif i.lower() == "n't":
			tokens.append("not")
		else:
			tokens.append(i)
	temp = temp + tokens	
	if tokens[-1] in [".", "?", "!"]:
		temp = temp + ["{{end}}"]
		list_sentences.append(temp)
		temp = []

for i in list_sentences:
	print i
	print "**********"
