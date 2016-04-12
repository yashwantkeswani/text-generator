import model
import glob
import nltk
import codecs
import re
import os
import math
def createAverage(listOfModels):
	new_dic = {'{{start}}':{'total':0},'{{end}}':{'total':0},'total':{'{{end}}'}}
	master_set = set()
	for i in listOfModels:
		master_set = master_set | set(i.iterkeys())
	# print master_set
	# for i in master_set:
	# 	print i
	
	for i in master_set:
		# print i
		for b in listOfModels:
			if i in b:
				if isinstance(b[i], set):
					continue
				if i not in new_dic:
					new_dic[i] = {}
				for c in b[i]:
					if c in new_dic[i]:
						new_dic[i][c] = new_dic[i][c] + b[i][c]
					else:
						new_dic[i][c] = b[i][c]

	# for i in litsOfModels[1:]:
	# 	for j in i:
	# 		if j not in new_dic:
	# 			for m in i[j]:
	# 				new_dic[j][m] = i[j][m]
	# 			continue
	# 		for k in j:
	# 			if k == 'total':
	# 				continue
	# 			if k in new_dic[j]:
	# 				new_dic[j][k] = new_dic[j][k] + i[j][k]
	# 			else:
	# 				new_dic[j][k] = i[j][k]

	# l = len(listOfModels)
	# print "This Completed"
	# for i in new_dic:
	# 	count = 0
	# 	for j in i:
	# 		count = count + new_dic[i][j]
	# 	new_dic[i]['total'] = count*l

	return new_dic

def generateModelAuthors(rootDirectory, order, flag):
	numberOfAuthors = len(glob.glob(rootDirectory))
	modelsOfEachAuthor = {}
	for z in glob.glob(rootDirectory):
		modelsOfEachAuthor[z] = None

	allAuthors = glob.glob(rootDirectory)
	for i in allAuthors:
		if flag==0:
			print "Creating model for author", i
			all_files = glob.glob(i+"/*")
			training = []
			new_file = open(i+"temp.txt", "w")
			# new_file.write("{{start}}")
			for j in all_files:
				print "\t Reading file ", j
				content_to_be_passed = ""
				content = codecs.open(j,'r',encoding='utf8').read()
				sentences = nltk.tokenize.sent_tokenize(content)
				for k in sentences:
					m = nltk.pos_tag(nltk.tokenize.word_tokenize(re.sub("[\"\,\;\:\']","",k)))
					content_to_be_passed = content_to_be_passed + \
					" ".join([c[0].lower() for c in m  if c[1] not in ["NNP", "."] ])
				new_file.write(str(unicode(content_to_be_passed).encode('utf8')))
				# training.append(temp_model.return_states())
			# new_file.write(" {{end}}")
			new_file.close()
		temp_model = model.model()
		all_files = glob.glob(i+"/*")
		temp_model.generate_model(order,all_files[0],0)
			# print 
		modelsOfEachAuthor[i] =  temp_model
		# os.remove(i+"temp.txt")
		# print modelsOfEachAuthor[i]
	return modelsOfEachAuthor


def assign_author(testFile, modelAuthors, flag):
	content_to_be_compared = ""
	if flag==0:
		content = codecs.open(testFile,'r',encoding='utf8').read()
		sentences = nltk.tokenize.sent_tokenize(content)
		for k in sentences:
			m = nltk.pos_tag(nltk.tokenize.word_tokenize(re.sub("[\,\;\:\']","",k)))
			content_to_be_compared = content_to_be_compared + \
			" ".join([c[0].lower() for c in m  if c[1] not in ["NNP", "."] ])
	else:
		content_to_be_compared = open(testFile, 'r').read()
		# content_to_be_compared = codecs.open(testFile,'r',encoding='utf8').read()

	score = {}
	start_state = (content_to_be_compared[0], content_to_be_compared[1])
	for i in modelAuthors:
		# print "Started testing for author ", i
		score_i = 0
		prev_state = start_state
		s = modelAuthors[i].return_states()
		for j in range(2,len(content_to_be_compared)-2):
			new_state = (content_to_be_compared[j], content_to_be_compared[j+1])
			if prev_state in s:
				if new_state in s[prev_state]:
					# print s[prev_state]['total']
					score_i = score_i + math.log(float(s[prev_state][new_state])/s[prev_state]['total'])
			prev_state = new_state
		score[i] = score_i;
	return score

x = generateModelAuthors("./testDirectory/*", 3, 1)
m = glob.glob("./test/*formatted")
for i in m:
	print i
	y = assign_author(i, x , 1)
	max1 = -9999999999
	max_pos = 'l'
	print y
	for l in y:
		if y[l] > max1:
			max1= y[l]
			max_pos = l
	print max_pos

	print "***********************"