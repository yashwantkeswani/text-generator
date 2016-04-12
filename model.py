from model_creator import token_generator
import random
from operator import itemgetter
import sys

class model:
	def __init__(self):
		self.t=token_generator()
		random.seed()	
		self.states = {'{{start}}':{'total':0}}

	def return_states(self):
		return self.states	
		


	def generate_model(self,order,filename,flag):
		if(flag==1):
			tokens=self.t.generate(filename)
		else:
			print filename
			f=open(filename,'r')
			tokens=f.read().split('\n')
			for i in xrange(0,len(tokens)):
				tokens[i]=list(tokens[i])
		
		self.states={'{{start}}':{'total':0},'{{end}}':{'total':0},'total':{'{{end}}'}}
		#print tokens
		#print len(tokens)

		for i in tokens:

			if len(i)<order:
				continue

			init_tuple=tuple([i[x].lower() for x in xrange(1,order)])
			#print init_tuple
			try:
				self.states['{{start}}'][init_tuple]=self.states['{{start}}'][init_tuple]+1
				self.states['{{start}}']['total']+=1
			except Exception as e:
				self.states['{{start}}'][init_tuple]=1
				self.states['{{start}}']['total']+=1

			for j in xrange(1,len(i)-order+1):
				temp_tuple=tuple([i[x].lower() for x in xrange(j,j+order-1)])
				temp_tuple_2=tuple([i[x].lower() for x in xrange(j+1,j+order)])
				try:
					temp=self.states[temp_tuple]
					try:
						self.states[temp_tuple][temp_tuple_2]+=1
						self.states[temp_tuple]['total']+=1
					except:
						self.states[temp_tuple][temp_tuple_2]=1
						self.states[temp_tuple]['total']+=1				
				except:
					self.states[temp_tuple]={'total':0}
					self.states[temp_tuple][temp_tuple_2]=1
					self.states[temp_tuple]['total']+=1
			

			end_tuple = tuple([i[x] for x in xrange(len(i)-order+1,len(i))])
			try:
				self.states[end_tuple]['{{end}}'] += 1;
				self.states[end_tuple]['total'] += 1;
			except:
				self.states[end_tuple]={'total':0}
				self.states[end_tuple]['{{end}}'] = 1;
				self.states[end_tuple]['total'] += 1;
		#print self.states
		return self.states

	def inverseTransform(self, probable_states):
		U = random.random();		
		outlinks = probable_states['total']
		sorted_probable_states = dict(sorted(probable_states.items(), key=lambda x: x[1]))
		#print sorted_probable_states[0][1]
		#print type(sorted_probable_states)
		#print U
		temp = 0
		for i in sorted_probable_states:
			temp = temp + float(sorted_probable_states[i])/float(outlinks)
			if i=='total' or i == None :
				continue		
			if U<temp:
				return i

		
			
	
	def generateSentence(self,order,length):
		sentence = []
		count = 0		
		next_state = '{{start}}'
		while next_state != '{{end}}':
			#print sentence
			if(len(sentence)>=length*order):
				break
			#print next_state
			if(next_state!='{{start}}'):
				sentence = sentence+list(next_state)
			try:
				next_state = self.inverseTransform(self.states[next_state])
				while next_state[0]==',':
					next_state = self.inverseTransform(self.states[next_state])
			except Exception as e :
				
				if(len(sentence)<=length*order):
					next_state='{{start}}'
					continue
				#print e
				break
			if(next_state=='{{end}}' and len(sentence)<=length*order):
				next_state='{{start}}'
		#print sentence
		return sentence
	
	def printSentence(self,sentence,order,flag):
		
		printSent=""
		for i in xrange(0,len(sentence),order-1):
			if(sentence[i]==',' or sentence[i]=='.' or flag==0):
				printSent=printSent+sentence[i]
			else:
				printSent=printSent+" "+sentence[i]
		return str(unicode(printSent.strip(r'{.*').lstrip()).encode('utf-8'))


if __name__=='__main__':
	m=model()
	order=4
	flag=1 # 0 for alphabets 1 for words
	datafile='data_cleaned.txt'
	m.generate_model(order,datafile,flag)
	print m.printSentence(m.generateSentence(50,order),order,flag)
