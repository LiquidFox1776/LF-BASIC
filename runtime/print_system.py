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

Print system based on 80 character wide lines
segmented into 5 print zones
'''
class Print_System :
	def __init__(self) :
		self.line_width = 80 # might change later, using 80 because that is a typical number for character width for a line on old style displays
		self.line_position = 1 # holds col numbers
		
	def advance_print_zone(self) :
		'''
		ECMA-55 states that print zones on a typical terminal might be split up of 5 zones 15 characters each
		Microsoft's Quick BASIC uses 5 print zones 14 characters each 
		we will use 15 characters with 5 zones
		1   Start of print zone 1
		16  Start of print zone 2
		31  Start of print zone 3
		46  Start of print zone 4
		61  Start of print zone 5
		75  Last Character of print Zone
		76  No zone space
		80  Last line character
		'''
		if self.line_position >= 61 :
			self.line_position = 1
			print()
			return
		
		while (self.line_position % 15) != 0 :
			print(' ', end='')
			self.line_position += 1
		
		print(' ', end='')
		self.line_position += 1
		
	def print(self, s) :
		'''
		prints an element of a print list and changes the line_position variable as needed
		'''
		s = str(s)
		if self.line_position > 80 : # 80 chars is the max line width, if over reset
			self.line_position = 1
			print()
			
		if (self.line_position + len(s)) <= self.line_width : #if what we are printing is before or equal to the end of the line print it
			print(s,end='')
			self.line_position += len(s)
			return
			
		for c in s : # if we are here we are printing on multiple lines
			if self.line_position > self.line_width :
				print()
				print(c,end='')	
				self.line_position = 1
			
			elif c == '\n' :
				self.line_position = 1
				print()
			else :
				print(c,end='')	
				self.line_position +=1
		
	def print_list(self, plist) :
		'''
			prints a print list
			['ITEM1',NUMBER1,[2]] [2] means do not print new line once the end of the list is reached
			['ITEM1',[1], 'ITEM2'] [1] means move to the next print zone
		'''
		new_line = True
		
		if type(plist[-1]).__name__ == 'list' :
			if plist[-1][0] == 2 : #if the last print item is a semi colon we wont print a new line at end of list
				new_line = False
				
		for item in plist : # iterate the print items
			if type(item).__name__ == 'str' :
				self.print(item)
			elif type(item).__name__ == 'int' :
				self.print(item)
			elif type(item).__name__ == 'float' :
				self.print(item)
			elif type(item).__name__ == 'list' : #if we have a list we are not dealing with a literal print item
				if item[0] == 1 :  # if true move to next print zone
					self.advance_print_zone()
		if new_line == True :
			print()
			self.line_position = 1