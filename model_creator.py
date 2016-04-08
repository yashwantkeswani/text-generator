import nltk
import re
import codecs

class token_generator:

	
	html_escape_table = {
		"&": "&amp;",
		'"': "&quot;",
		"'": "&apos;",
		">": "&gt;",
		"<": "&lt;"
		}

	def html_escape(self,text):
		for i in self.html_escape_table:	
			text = re.sub(self.html_escape_table[i], i, text)
		return text




	def generate(self,filename):
		f = codecs.open(filename,'r',encoding='utf8').readlines()

		list_sentences = []
		temp = []
		for j in f:
			if j.strip()=="":
				continue
			tokens2 = nltk.word_tokenize(j.strip())	
			tokens = []
			for i in tokens2:
				if i.lower() == 'ca':
					tokens.append(i+'n')
				elif i.lower() == "n't":
					tokens.append("not")
				elif i.lower() == "'re":
					tokens.append("are")
				elif i.lower() == "'ve":
					tokens.append("have")
				elif i.lower() == "'ll":
					tokens.append("will")
				elif i.lower() =="'m":
					tokens.append("am")
				elif i.lower() == "'s":
					tokens.append("is")
				elif i.lower() in ['(',')']:
					pass
				else:
					tokens.append(i)
			temp = temp + tokens
				
			if tokens[-1] in [".", "?", "!"]:
				temp = temp + ["{{end}}"]
				list_sentences.append(temp)
				temp = []

		
		return list_sentences
