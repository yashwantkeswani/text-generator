from model_creator import token_generator
from copy import deepcopy
class model:
	t=token_generator()
	
	def generate_model(self,order,filename):
		tokens=self.t.generate(filename)
		states={'{{start}}':{'total':0}}

		for i in tokens:

			init_tuple=tuple([i[x] for x in xrange(1,order)])
			print init_tuple
			try:
				states['{{start}}'][init_tuple]=states['{{start}}'][init_tuple]+1
				states['{{start}}']['total']+=1
			except Exception as e:
				states['{{start}}'][init_tuple]=1
				states['{{start}}']['total']+=1

			for j in xrange(1,len(i)-order+1):
				temp_tuple=tuple([i[x] for x in xrange(j,j+order-1)])
				temp_tuple_2=tuple([i[x] for x in xrange(j+1,j+order)])
				try:
					temp=states[temp_tuple]
					try:
						states[temp_tuple][temp_tuple_2]+=1
						states[temp_tuple]['total']+=1
					except:
						states[temp_tuple][temp_tuple_2]=1
						states[temp_tuple]['total']+=1				
				except:
					states[temp_tuple]={'total':0}
					states[temp_tuple][temp_tuple_2]=1
					states[temp_tuple]['total']+=1
		return states

	

if __name__=='__main__':
	m=model()
	print m.generate_model(2,'data_cleaned.txt')
