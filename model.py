from model_creator import token_generator
import random
from operator import itemgetter

class model:
	def __init__(self):
		self.t=token_generator()
		random.seed()	
		self.states = {'{{start}}':{'total':0}}

	
	def generate_model(self,order,filename):
		tokens=self.t.generate(filename)
		self.states={'{{start}}':{'total':0}}

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
			

			end_tuple = tuple([i[x] for x in xrange(j-order+1,len(i))])
			try:
				self.states[end_tuple]['{{end}}'] += 1;
				self.states[end_tuple]['total'] += 1;
			except:
				self.states[end_tuple]={'total':0}
				self.states[end_tuple]['{{end}}'] = 1;
				self.states[end_tuple]['total'] += 1;
						
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
			if i=='total' or i == None:
				continue		
			if U<temp:
				return i

		
			
	
	def generateSentence(self):
		sentence = []
		count = 0		
		next_state = '{{start}}'
		while next_state != ('{{end}}',):
			#print next_state
			if(next_state!='{{start}}'):
				sentence = sentence+list(next_state)
			try:
				next_state = self.inverseTransform(self.states[next_state])
			except:
				break
		return sentence
	
	def printSentence(self,sentence,order):
		#print sentence
		printSent=""
		for i in xrange(0,len(sentence),order-1):
			printSent=printSent+" "+sentence[i]
		printSent.strip('None')
		return printSent


if __name__=='__main__':
	m=model()
	m.generate_model(4,'data_cleaned.txt')
	print m.printSentence(m.generateSentence(),4)
