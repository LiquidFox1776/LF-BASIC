'''
Copyright 2018 LiquidFox1776 LiquidFox1776@gmail.com
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Python Version:    3.x
License:           MIT
'''
from parse import parse
from .print_system import Print_System
import math
import random
import time

def SQR(x) :
	return math.sqrt(x)

def ABS(x) :
	return abs(x)

def ATN(x) :
	return math.atan(x)
	
def COS(x) :
	return math.cos(x)

def EXP(x) :
	return math.exp(x)

def INT(x) :
	return math.floor(x) 

def LOG(x) :
	return math.log(x)

def SGN(x) :
	pass

def SIN(x) :
	return math.sin(x)

def SGN(x) :
	return -1 if x < 0 else 0 if x == 0 else 1

def TAN(x) :
	return math.tan(x)

def TAB(x) :
	'''
	Moves the print cursor to a new col with the use of spaces
	'''
	if x >= 1 :
		return ' ' * x
	else :
		return ' '
def RND() :
		return random.random()

def CLK(x) : # added to play 1978 Oregon Trail
	return time.monotonic()
	
class Machine :
	BUILT_IN = True # Built in function constant
	USER_DEFINED = False # User defined function constant 
	MAXIMUM_DIM_SIZE = 10 # Used to limit array size, TODO implement 
	

	def __init__(self) :
		self.goto_flag = False
		self.program_counter = 0
		self.call_stack = [] # used to hold line numbers for gosub calls, this list will be treated like a stack
		self.for_stack = [] # this will be used for the for and next statements
		self.instructions = [] #holds program instructions
		self.data = [] # used for the data statement
		self.data_pointer = 0 # used to keep track of pointer when using read and restore
		self.basic_print = Print_System()
		self.eval_value = None
		self.var_scratch_pad = []
		
		self.function_table = { # 'FNA' : [['X'],self.USER_DEFINED,"X *2 + 1"],
'ABS' : [['X'],self.BUILT_IN,''],
'ATN' : [['X'],self.BUILT_IN,''],
'COS' : [['X'],self.BUILT_IN,''],
'EXP' : [['X'],self.BUILT_IN,''],
'INT' : [['X'],self.BUILT_IN,''],
'LOG' : [['X'],self.BUILT_IN,''],
'RND' : [[],self.BUILT_IN,''],
'SGN' : [['X'],self.BUILT_IN,''],
'SIN' : [['X'],self.BUILT_IN,''],
'SQR' : [['X'],self.BUILT_IN,''],
'TAN' : [['X'],self.BUILT_IN,''],
'TAB' : [['X'],self.BUILT_IN,'']}

		self.variable_table = {'TESTVAR' : ['STRING',"hello world"]}
		
	def set_variable(self, variable_name, variable_type,value) :
		'''
		Adds or modifies a new variable
		TODO This function name and behavior will change at a later date
		'''
		self.variable_table.update({variable_name : [variable_type,value]})

	def get_variable_type(self,variable_name) :
		if variable_name in self.variable_table :
			return self.variable_table.get(variable_name)[0]
		else : #TODO ERROR HANDLING 
			self.error(error_message = "Runtime Error, variable not found", position = 0, fatal = True)

	def does_variable_exist(self,variable_name) :
		'''
		Returns true if a variable exists
		false if it doe snot exist
		'''
		if variable_name in self.variable_table :
			return True
		else :
			return False

	def get_array_value(self,variable_name, index) :
		'''
		gets the value of a string array or numeric array element
		this function will most likely change at a later date
		'''		
		try :
			if variable_name in self.variable_table :
				return eval('self.variable_table.get("' + variable_name + '")[1]' + str(index)) # don't like using exec but it will do for now
			else :
				self.error(error_message = "Runtime Error, variable not found", position = 0, fatal = True)
		except :
			self.error()
	def delete_variable(self, variable_name) :
		'''
		deletes a variable
		TODO add checks to determine if var exists
		'''
		del self.variable_table[variable_name]
		
	def set_array_value(self,variable_name, index, value) :
		'''
		sets the value of a string array or numeric array element
		this function will most likely change at a later date
		'''
		if variable_name in self.variable_table :
			exec('self.variable_table["' + variable_name + '"][1]' + str(index) + '=' +  str(value)) # don't like using exec but it will do for now
		else :
			print(self.instructions[self.program_counter])
			print(variable_name + "VARIABLE NOT FOUND")
			return None
			
	def get_variable_value(self,variable_name) :
		'''
		gets the value of a simple numeric or string variable
		'''
		if variable_name in self.variable_table :
			return self.variable_table.get(variable_name)[1]
		else :
			print("PROGRAM COUNTER ", self.program_counter)
			print(self.instructions[self.program_counter])
			print(variable_name + "VARIABLE NOT FOUND")
			return None

	def add_function_to_table(self,func_name, func_argument_list, func_body) :
		'''
		self.function_table = {'FNA' : [['X'],self.USER_DEFINED,"X *2 + 1"],
		'''
		self.function_table.update({func_name : [func_argument_list, self.USER_DEFINED, func_body]})

	def get_function(self,func_name) :
		
		if func_name in self.function_table :
			#print("FOUND FUNCTION")
			return self.function_table[func_name][0], self.function_table[func_name][1],self.function_table[func_name][2] # param_list, user_Defined/built_in, function_body
		else : # FATAL ERROR can't find function
			self.error(error_message = "Runtime Error, function not found", position = 0, fatal = True)
			
	def eval_randomize(self) :
		random.seed()
		
	def execute_built_in_function(self,func_name, built_in, argument) :
		if argument is not None :
			return globals()[func_name](argument)
		else :
			return globals()[func_name]()
			
	def eval_function(self,func_name, built_in, argument) : #TODO REFACTOR
		'''
		evaluates user and built in functions
		'''
		tmp_destroy = False
		
		if built_in == True : # we are working with a built in funciton
			return self.execute_built_in_function(func_name, built_in, argument)
						
		else : # we are dealing with user defined functions

			parameter,built_in,function_body = self.get_function(func_name)
			if len(parameter) > 0 :
				parameter = parameter[0].strip()

			if argument == None :
				eval_lexer = parse.lexer.clone() # needed to clone so we can evaluate expressions without destroying the rest of the original input
				parse.parser.parse('0 ' +  'EVAL' + function_body,lexer=eval_lexer)
				return self.eval_value
				
			else : # we need to replace argument with every occurrence of the parameter int the function body

				if self.does_variable_exist(parameter) == True : # if true save the value of the existing variable
					self.var_scratch_pad.append([parameter,self.get_variable_value(parameter)])
					self.set_variable(parameter, 'INTEGER' ,argument)
									
				else : #VARIABLE DOES NOT EXIST
					self.set_variable(parameter, 'INTEGER' ,argument)
					#print(self.variable_table)
					tmp_destroy = True 
				eval_lexer = parse.lexer.clone() # needed to clone so we can evaluate expressions without destroying the rest of the original input
				parse.parser.parse('0 ' +  'EVAL' + function_body,lexer=eval_lexer)
				
				if self.var_scratch_pad != [] : # if not none restore value of variable
					self.set_variable(self.var_scratch_pad[-1][0], 'INTEGER' ,self.var_scratch_pad[-1][1])
					self.var_scratch_pad.pop()	
				
				if tmp_destroy == True :
					self.delete_variable(parameter)


				return self.eval_value			
			

	def convert_tuple_tree_to_list(self,tree) :
		'''
		Converts a tree into a list of expressions that can be processed by various functions
		example of an input tree ('HELLO ', [2], ('WORLD', [2], 'I AM A TUPLE TREE'))
		another example ('HELLO ', [2], ('WORLD ', [2], ('I AM A TUPLE TREE', [2], (' WITH ', [2], ('EVEN', [2], ('MORE', [2], 'ITEMS'))))))
		outputs a list in the form of [exp1,exp2,exp3...]
		'''
		tmp_list = []
		if tree is None : #this can only apply to eval_print, the other eval functions cannot be none due to the specified parser grammar
			return ''
		
		if type(tree).__name__ == 'tuple' : # if true walk tuple tree
			while type(tree).__name__ == 'tuple' :
				for node in tree : # get all of the nodes at the cuurent level
					if (type(node).__name__ != 'tuple') and (node != None):
						tmp_list.append(node) # append the node to the output list
				tree = node # update the parent node in the tree
		else : # if not a tuple we only have 1 expression/node to deal with
			return [tree]
		
		return tmp_list

	def eval_if(self,p) :
		'''
		Examples
		IF expression LT GT expression THEN INTEGER
		IF expression GT expression THEN INTEGER
		'''
		line_number = 0
		result = False
		if(len(p) == 5) : # if true we are working with single relational
			exp1 = p[1]
			operator = p[2]
			exp2 = p[3]
			line_number = p[4]
		else : # we are working with multi relational
			exp1 = p[1]
			operator = p[2] + p[3]
			exp2 = p[4]
			line_number = p[5]
		try :
			if(operator == ">") :
				result = exp1 > exp2
			elif(operator == "<") :
				result = exp1 < exp2
			elif(operator == "=") :
				result = exp1 == exp2
			elif(operator == "<>") :
				result = exp1 != exp2
			elif(operator == "<=") :
				result = exp1 <= exp2
			elif(operator == ">=") :
				result = exp1 >= exp2
		except TypeError:
			print("Cannot compare incompatible data types")
			result = False

		if result : 
			self.goto(line_number)

	def eval_print(self,print_list) :
		print_list = self.convert_tuple_tree_to_list(print_list)
		self.basic_print.print_list(print_list)

	def eval_input(self,prompt_string, variable) :

		variable_type = self.get_variable_type(variable)
		while True :
			try :
				if variable_type == 'STRING' :
					self.set_variable(variable , 'STRING', '"' + input(prompt_string) + '"')
				elif variable_type == 'INTEGER' :
					self.set_variable( variable, 'INTEGER', int(input(prompt_string)))
				elif variable_type == 'FLOAT' :
					self.set_variable( variable, 'FLOAT', float(input(prompt_string)))
				break
			except :
				print('INVALID INPUT')
		
		self.basic_print.line_position = 1# need to reset the print position
	def eval_on(self,number, list_of_line_numbers) :
		if number is not None :
			number = int(number)

			tmp_line_numbers = self.convert_tuple_tree_to_list(list_of_line_numbers) # convert tree to list [1,2,3,...]

			if (number < 1) or ((number) > len(tmp_line_numbers)) : # if true a fatal exception should occur
				self.error(error_message = "Runtime Error, line label not found", position = 0, fatal = True)
			else :
				self.goto(tmp_line_numbers[number - 1])
		
	def eval_data_list(self,data_list) :
			tmp_data_list = self.convert_tuple_tree_to_list(data_list) # convert tree to list [1,2,3,...]
			self.append_to_data(tmp_data_list)
			
	def eval_read_list(self,read_list) :

			tmp_read_list = self.convert_tuple_tree_to_list(read_list) # convert tree to list [1,2,3,...]
			self.read_data(tmp_read_list)

	def eval_dim(self,variable_name,variable_type, bounds_list) :
		if self.does_variable_exist(variable_name) == False : # if statement is true we can create the variable
			if len(bounds_list) == 1 :
				tmp_array = [None for x in range(0,bounds_list[0])] # populate a list with None
			else : #For now this will only equal 2
				tmp_array = [[None for x in range(0,bounds_list[0])] for y in range(0,bounds_list[1])] # creates an array using nested lists in the form of [[],[],[],[],[],[]] filled with None

			self.set_variable(variable_name, variable_type, tmp_array)
		else :
			self.error(error_message = "Runtime Error, array already declared", position = 0, fatal = True)

	def goto(self,line_number) :
		'''
		Modifies the program counter
		'''
		for i in range(0, len(self.instructions)) :
			if line_number == self.instructions[i][0] :
				self.program_counter = i
				self.goto_flag = True
				return

		if self.goto_flag == False :
			self.error(error_message = "Runtime Error, cannot find line label", position = 0, fatal = True)

	def gosub(self,line_number) :
		'''
		Modifies the program counter and modifies call stack
		'''
		
		self.call_stack.insert(0, self.program_counter) #push current instruction number onto stack
		
		for i in range(0, len(self.instructions)) :
			if line_number == self.instructions[i][0] :
				self.program_counter = i
				self.goto_flag = True
				return

		if self.goto_flag == False :
			self.error(error_message = "Runtime Error, cannot find line label", position = 0, fatal = True)

	def gosub_return(self) :
		'''
		returns from a gosub
		modifies call_stack
		'''
		if len(self.call_stack) >= 1 :
			self.program_counter = self.call_stack[0] + 1 # return to the point after gosub was called
			del self.call_stack[0] #pop the top of the stack
			self.goto_flag = True
		else : # if true we have an empty stack
			print("OUT OF PLACES TO GO")
			pass #ignore for now

	def data_restore(self) :
		'''
		resets the data pointer
		'''
		self.data_pointer = 0

	def append_to_data(self,data_list) :
		'''
		appends data to the data variable
		'''
		for datum in data_list :
			self.data.append(datum)

	def read_data(self,read_list) :
		'''
		reads data from data_list into a list of variables
		and advances the data pointer
		'''

		for variable in read_list :
			if self.data_pointer > (len(self.data) -1) : #FATAL EXCEPTION TODO ERROR HANDLING
				self.error(error_message = "Runtime Error, out of data", position = 0, fatal = True)

			var_type = self.get_variable_type(variable)
			if var_type is not None :
				if type(self.data[self.data_pointer]).__name__ == 'str':
					if var_type != 'STRING' : #data type mismatch move to set_Variable
						self.error(error_message = "Runtime Error, data mismatch", position = 0, fatal = True)
					else : # assign the string
						self.set_variable(variable, 'STRING','"' + self.data[self.data_pointer] + '"')
						self.data_pointer += 1 # advance the data pointer
				elif (type(self.data[self.data_pointer]).__name__ == 'int') or (type(self.data[self.data_pointer]).__name__ == 'float'):
					if var_type == 'STRING' : #data type mismatch move to set_Variable
						self.error(error_message = "Runtime Error, data mismatch", position = 0, fatal = True)
					else : # assign the value
						self.set_variable(variable, 
						(type(self.data[self.data_pointer]).__name__).upper(), # variable type
						self.data[self.data_pointer])	# the actual data
						self.data_pointer += 1 # advance the data pointer
				
			else : #var does not exist
				self.error(error_message = "Runtime Error, variable does not exist", position = 0, fatal = True)
	def push_for(self, variable_name, init_value, end_value,step=1) :
		'''
		Pushes for data to the for_stack
		for_stack:
		[instruction_start, variable_to_advance,end_value, step_value]
		This function will create a variable if it does not exist
		'''
		self.for_stack.append([self.program_counter + 1, variable_name, end_value, step])
		self.set_variable(variable_name, 'INTEGER', init_value)
		
	def next(self, variable_name) :
		'''
		the heart of the for statement
		this function does most of the work
		'''
		if len(self.for_stack) == 0 : #if true we are dealing with a fatal error
			self.error(error_message = 'Runtime Error NEXT without FOR', fatal=True,verbose=False)
	
		tmp_line_number = self.for_stack[-1][0]	
		tmp_variable_name = self.for_stack[-1][1]
		tmp_end_value = self.for_stack[-1][2]
		tmp_step_value = self.for_stack[-1][3]
		tmp_var_value = self.get_variable_value(tmp_variable_name) 
		tmp_var_value += tmp_step_value
		
		if tmp_variable_name != variable_name : # if true we are dealing with a for without next which is fatal
			self.error('Bad control variable {} should be {}'.format(variable_name, tmp_variable_name), 
			fatal=True, position = 8, verbose=False)
			
		if (tmp_var_value-tmp_end_value) * SGN(tmp_step_value) > 0: # if we have reached the end value and need to terminate the loop
			self.set_variable(variable_name, 'INTEGER',tmp_var_value )
			self.for_stack.pop()
		else : # increment or decrement the variable
			self.set_variable(variable_name, 'INTEGER', tmp_var_value)
			self.program_counter = tmp_line_number
			self.goto_flag = True
					
		
	def error(self, error_message='',position=0, fatal=False, verbose=True,debug=False) :
		'''
		TODO this function will change behavior at a later date 
		for right now it dumps program line, and program counter
		'''
		if debug == False :
			position = position - len(str(self.instructions[self.program_counter][0]))
			if position < 0 :
				position = 0
			print (error_message + ' at line label ' + str(self.instructions[self.program_counter][0]))
			print(self.instructions[self.program_counter][1] + ' starting at position ' +
			str(position))
			print(' ' * (position -1) + '^')
		else :
			print(str(self.instructions[self.program_counter][0]) + ' ' + self.instructions[self.program_counter][1])
		
		if verbose == True :
			print('PROGRAM COUNTER', self.program_counter)
			print('FUNCTION TABLE\n: ', self.function_table)
			print('VARTABLE TABLE\n: ',self.variable_table )
			print('DATA\n: ', self.data)

		input("paused press enter to continue...")
		
		if fatal == True :
			exit()
	
	def pre_process(self) :
		'''
		TODO This function might be expanded upon later
		'''
		for i in self.instructions : #looks for data keywords to build up data for use with DATA statement
			tmp_instruct = i[1].split()
			if len(tmp_instruct) > 0 :
				if tmp_instruct[0] == 'DATA' :
					parse.parser.parse(str(i[0]) + ' ' + str(i[1]))
					i[1] = '' # if data was found erase the instruction so it does not get processed twice

	def run(self, debug=False) :
		'''
		instructions is a list of instructions [[line_number, 'instructions']]
		runs the instructions
		'''
		self.pre_process()
		self.program_counter = 0 # a reset function might be added at a later date to reset function and vartable as well
		
		while self.program_counter < len(self.instructions) : # loop through instructions
			if debug == True :
				self.error(error_message='DEBUG MODE', debug=True)
				
			r = parse.parser.parse(str(self.instructions[self.program_counter][0]) + ' ' + 
			self.instructions[self.program_counter][1])
	
			if self.goto_flag == False : # if false we can just increment pc by 1 
				self.program_counter += 1
			
			self.goto_flag = False # reset goto flag
		

machine = Machine()