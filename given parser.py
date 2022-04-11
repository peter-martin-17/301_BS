import ply.lex as lex
import ply.yacc as yacc
import re
import argparse

#global variable that stores every distinct quoted string each line of the file
pastQuotedStrings = list()

class ClifLexer():
	ops_count=0
	names_count=0

	# CONSTRUCTOR
	def __init__(self):
		print('Lexer constructor called.')
		self.lexer = lex.lex(module=self)
		# start in the (standard) initial state
		self.lexer.begin('INITIAL')

	# DESTRUCTOR
	def __del__(self):
		print('Lexer destructor called.')

	reserved_bool = {
		'and': 'AND',
		'or': 'OR',
		'not': 'NOT'
	}

	reserved_if = {
		'if': 'IF',
		'iff': 'IFF'
	}

	reserved_comment = {
		'cl:comment': 'CL:COMMENT'
	}


	tokens = ['OPEN', 'CLOSE', 'QUOTEDSTRING', 'RESERVEDELEMENT', 'NUMERAL', 'COMMENT']

	tokens += reserved_bool.values()
	tokens += reserved_if.values()


	t_ignore = '\t\r\n\f\v '

	def t_NEWLINE(self,t):
		r'\n+'
		t.lexer.lineno += len(t.value)


	def t_error(self,t):
		print("Lexing error: Unknown character \"{}\" at line {}".format(t.value[0], t.lexer.lineno))
		t.lexer.skip(1)

	# token specification as a string (no regular expression)

	t_OPEN= '\('
	t_CLOSE= '\)'

	def t_NUMERAL(self, t):
		r'\d+'
		return t

	def t_QUOTEDSTRING(self, t):
		#Original
		#r"\'[\w?~!\#$%^&*_+{}|=:\"<>\|,./\[\]\;\-]+\'"
		#EC 
		r"\'[\w?~!#$%^&*_+{}\=:<>\|,./\[\]\;\-\|\"\|\']+\'"

		#Casts 't' as a string and stores it in 'currentQuotedString'
		currentQuotedString = str(t)

		#This will store the quoted string
		substring = ""

		#This stores the first character after ',' in 'currentQuotedString' Example: LexToken(QUOTEDSTRING,<<<<HERE>>>>"'TODAY=03/26/22'",1,10) 
		firstChar = ""

		#Stores two possible firstChar depending on if the quoted string has a name quote or not
		if (str(currentQuotedString[22]) == '\''):
			firstChar = '\''
		else:
			firstChar = '"'

		substring += currentQuotedString[22]
		
		for i in range(23, len(currentQuotedString)):

			#Special cases for each quoted string
			if (firstChar == '\'' and i > 23 and str(currentQuotedString[i]) == '\\'):
				substring += '\\\'\''
				break
			
			elif (firstChar == '"' and str(currentQuotedString[i]) == '"'):
				substring += '"'
				break
			
			#else just add to substring
			else:
				substring += currentQuotedString[i]

		#if its the first quoted string lexed, just add it and don't check for distinctiveness
		if (len(pastQuotedStrings) == 0):
			pastQuotedStrings.append(substring)
			ClifLexer.names_count+=1

		#Check if the new quoted string is equal to any past quoted strings
		else:
			isUnique = True
			for names in pastQuotedStrings:

				if (str(names) == str(substring)):
					isUnique = False
			
			#if the quoted string is distinct, the names_count is added and append the quoted string to distinct quoted strings list
			if (isUnique):
				pastQuotedStrings.append(substring)
				ClifLexer.names_count+=1

		return t
	

	def t_RESERVEDELEMENT(self, t):
		# here we use a regular expression to say what matches this particular token:
		# any sequence of standard characters of length 1 or greater
		# but this does not yet cover all reservedelements
		r'[\:\w]+'
		if t.value in self.reserved_bool:
			t.type = self.reserved_bool[t.value]
			#print("Boolean reserved word: " + t.value)
			ClifLexer.ops_count=ClifLexer.ops_count+1
			return t

		elif t.value in self.reserved_if:
			t.type = self.reserved_if[t.value]
			#print("Boolean reserved word: " + t.value)

			return t

		elif t.value in self.reserved_comment:
			t.type = 'COMMENT'
			#print("Boolean reserved word: " + t.value)
			return t

		else:
			pass


	'''t_NAMEQUOTE = r'[\"]'
	t_STRINGQUOTE = r'[\']'
	t_DIGIT = r'[\d]'
	t_CHAR =  r'[\w?~!#$%^&*_+{}|=:<>\|,./\[\]\;\-]'''


	def lex(self, input_string):
		self.lexer.input(input_string)
		while True:
			tok = self.lexer.token()
			if not tok:
				break
			print(tok)

class ClifParser(object):

	tokens = ClifLexer.tokens
	ops_count=0
	sentenceType = ""
	# CONSTRUCTOR
	def __init__(self):
		print('Parser constructor called.')
		
		self.lexer = ClifLexer()
		self.parser = yacc.yacc(module=self)
		tokens = ClifLexer.tokens


	def p_starter(self, p):
		"""
		starter : sentence
				| sentence starter
				|
		"""
		#print("Starting the parsing process.")
		
		pass

	def p_sentence(self, p):
		"""
		sentence : atomsent
				| boolsent
				| commentsent
		"""

	def p_atomsent(self, p):
		"""
		atomsent : OPEN termseq CLOSE
				| OPEN predicate CLOSE
		"""

		ClifParser.sentenceType = "Atomic: "


	def p_boolsent(self, p):
		"""
		boolsent :  OPEN AND starter CLOSE
				| OPEN OR starter CLOSE
				|  OPEN IFF sentence sentence CLOSE 
				|  OPEN IF sentence sentence CLOSE 
				|  OPEN NOT sentence CLOSE 
		"""

		ClifParser.sentenceType = "Boolean: "
		
	def p_commentsent(self, p):
		"""
		commentsent : OPEN COMMENT QUOTEDSTRING sentence CLOSE
		"""

	def p_termseq(self, p):
		"""
		termseq :  interpretedname
				| interpretedname termseq
				|
		"""

	def p_predicate(self, p):
		"""
		predicate : interpretedname
		"""

	def p_interpretedname(self, p):
		"""
		interpretedname : NUMERAL 
				| QUOTEDSTRING
		"""	
	def p_error(self, p):

		if p is None:
			raise TypeError("Unexpectedly reached end of file (EOF)")

		# Note the location of the error before trying to lookahead
		error_pos = p.lexpos

		# Reading the symbols from the Parser stack
		stack = [symbol for symbol in self.parser.symstack][1:]

		print("Parsing error;" + str(error_pos) + " current stack: " + str(stack))


	def parse(self, input_string):
		# initialize the parser
		#parser = yacc.yacc(module=self)
	
		self.parser.parse(input_string)

def main():

	takeIn = argparse.ArgumentParser(
		description="my arg parser"
	)

	takeIn.add_argument('txtName', help="Text File Name", type=str)
	takeIn.add_argument('parseOrLex', help="Parse or Lex", type=int)

	args = takeIn.parse_args()

	print(args.parseOrLex)


	if (args.parseOrLex):
		myPars = ClifParser()
		parser = myPars.parser

		myFile = open(args.txtName,'r')

		lineCount = 0
		for line in myFile:
			parser.parse(line)
			print(ClifParser.sentenceType + line[:-1]+": ops="+str(ClifLexer.ops_count)+", names="+str(ClifLexer.names_count)+"\n")
			ClifLexer.ops_count=0
			ClifLexer.names_count=0
			pastQuotedStrings.clear()
			ClifParser.sentenceType = ""
			lineCount += 1

		print(str(lineCount)+ " sentences")

	elif (not(args.parseOrLex)):

		myFile = open(args.txtName,'r')

		lex = ClifLexer()
		for line in myFile:
			print('Lexing '+line)
			lex.lex(line)



main()
