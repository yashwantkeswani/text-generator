import multiprocessing

import glob
import nltk
import codecs
import re
import os
import math
def format(testFiles):
	for testFile in testFiles:
		print testFile
		content_to_be_compared = ""
		content = codecs.open(testFile,'r',encoding='utf8').read()
		sentences = nltk.tokenize.sent_tokenize(content)
		for k in sentences:
			m = nltk.pos_tag(nltk.tokenize.word_tokenize(re.sub("[\,\;\:\']","",k)))
			content_to_be_compared = content_to_be_compared + \
			" ".join([c[0].lower() for c in m  if c[1] not in ["NNP", "."] ])
		content2 = codecs.open(testFile+'formatted','w',encoding='utf8')
		content2.write(content_to_be_compared)


cores = 4
m = glob.glob("/home/yashwant/Downloads/semester6/Stochaistic/text-generator/1/*")
print m
x = os.getcwd()
# m = ["/1/acd1.txt", "/1/cd1.txt", "/1/mt1.txt", "/1/ow2.txt"]
if __name__ == '__main__':
	jobs = []
	for i in range(cores):
		# p = multiprocessing.Process(target=format, args=(m[4*(i-1):min(len(m),4*i)],))
		p = multiprocessing.Process(target=format, args=([m[i]],))

		jobs.append(p)
		p.start()


