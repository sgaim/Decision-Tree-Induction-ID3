from __future__ import division
import numpy as np
import math
import collections

import xml.etree.ElementTree as ET
from xml.dom import minidom



class Queue:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.insert(0,item)

    def dequeue(self):
        return self.items.pop()

class info_gain:
	def __init__(self, file_name, delimit = ',', names = True, skiprows=1, decision_column = -1):
		self.file_name = file_name
		self.delimit = delimit
		self.decision_column = decision_column  #usually the last column which contains what you want to induce

		self.my_data = np.genfromtxt(self.file_name, delimiter = self.delimit, names = True, dtype=None) #Delimiter using numpy
		self.column_names = self.my_data.dtype.names #all column names
		self.classify_name = self.column_names[self.decision_column]  #the column name to predict/classify

		self.q = Queue() #Queue Instance
		self.root = ET.Element('ROOT')

	def process(self):
		self.root.set('table', self.my_data)

		self.q.enqueue(self.root)
		counter = 0

		while True :
			current_tree_element = self.q.dequeue()  #the current XML (sub)element
			current_matrix = current_tree_element.get('table')  #the current matrix to be looked at
			current_tree_element.attrib.pop('table')
			temp_classify_array = current_matrix[self.classify_name]  # the last column usually which contains what we are trying to predict
			first_entropy = self.calculate_entropy(temp_classify_array)   #the entropy
			non_decision_column_names= tuple(list(current_matrix.dtype.names)[:-1])

			if first_entropy > 0:	#If the entropy is not zero then run
				gains = []

				#determine which column has the highest gain?
				for i in non_decision_column_names:
					gains.append(self.calculate_gain(current_matrix,i,first_entropy)) #append gains & rounding

				#this column index has the highest gain
				key = gains.index(max(gains))
				key_name = current_matrix.dtype.names[key]

				current_tree_element.set('column_split', key_name)#adding attribute column split by column with highest gain
				current_tree_element.set('gain',str(round(max(gains),4))) #gain tag

				#splits columns & enqueues new elements
				self.splitting_by_column(current_matrix, key_name, current_tree_element)

			#the entropy is zero
			else:
				current_tree_element.set('Entropy',str(1.0)) #gain tag
				solution = current_matrix[self.classify_name][0]
				temp_element = ET.SubElement(current_tree_element,"LEAF")
				temp_element.set('answer',str(solution))


			
			if self.q.isEmpty():
				break

	#calculate entropy
	def calculate_entropy(self,table):

		self.frequency = collections.Counter(table)#frequency of yes and no's (Dictionary)
		total = sum(self.frequency.values())#Total yes and no's from dictionary
		self.entropy = 0

		for keys in self.frequency: #loop through keys of frequency 
			p_i = self.frequency[keys]/total #probability
			self.entropy+= -1 * p_i * math.log(p_i,2) #entropy
		
		return self.entropy

	#info gained from splitting items 
	def calculate_gain(self,data_matrix,which_column,entropy_par_):#, column_number):
		frequency = collections.Counter(data_matrix[which_column])

		local_total = sum(frequency.values())
		sets = zip(data_matrix[which_column], data_matrix[self.classify_name])
		collect = collections.Counter(sets)
		
		local_info = 0 #initiating calculation for info_A

		for keys in frequency:
			denom = frequency[keys]   #denominator or total
			inside_parenthesis = 0 	 #to be added to

			for j in collect:
				if (j[0] == keys):
					temp_p_i = collect[j]/denom
					inside_parenthesis+= -1 * temp_p_i * math.log(temp_p_i,2)

			local_info += denom/local_total * inside_parenthesis

		return entropy_par_ - local_info

	#process the table and add vertices's for each splitting
	def splitting_by_column(self, t_table, temp_name, parent):
		temp_frequency = collections.Counter(t_table[temp_name])  #get frequency

		#Renaming Column Names by removing the column that will be removed
		new_names = list(t_table.dtype.names)
		new_names.remove(temp_name) #removing one column

		for keys in temp_frequency:	#creating sub_tables
			sub_table = t_table[np.where(t_table[temp_name] == keys)]
			
			sub_table = sub_table[new_names]

			new_sub = ET.SubElement(parent,'BRANCH')
			new_sub.set('value',str(keys))
			new_sub.set('table', sub_table)
			self.q.enqueue(new_sub) #enqueuing new subelement to further calculate later

	#Write out XML Tree
	def write_xml(self,new_file_name):
		s = ET.tostring(self.root) #convert XML to String
		f = open(new_file_name, 'w') #open file
		f.write(minidom.parseString(s).toprettyxml()) #write out to file
		f.close()

	#Bin specified rows into nominal data atributes
	def binning(self):
		'Will bin specified rows into numeric atributes'

	#Run the trained tree on test data set.
	def testing(self, test_data_file):
		accurate = 0
		incorrect = 0
		for row in test_data_file:
			'Do nothing'



def main():
	base = info_gain('iris_data.csv', delimit = ',', decision_column=4)
	base.process()
	base.write_xml('ID3.xml')
	#base.testing()
main()

