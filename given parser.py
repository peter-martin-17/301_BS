import ply.lex as lex
import ply.yacc as yacc
import re


class ClifLexer():

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
		# This is not yet correct: you need to complete the lexing of quotedstring
		#r'[t_STRINGQUOTE&t_CHAR|t_NAMEQUOTEt_STRINGQUOTE]'
		#r"\'\w+\'"
		r"\'[\w?~!\#$%^&*_+{}|=:<>\|,./\[\]\;\-]+\' | \'[\"]+\'"  
		return t
	

	def t_RESERVEDELEMENT(self, t):
		# here we use a regular expression to say what matches this particular token:
		# any sequence of standard characters of length 1 or greater
		# but this does not yet cover all reservedelements
		r'[\:\w]+'
		if t.value in self.reserved_bool:
			t.type = self.reserved_bool[t.value]
			#print("Boolean reserved word: " + t.value)
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
		print("Starting the parsing process.")
		pass

	def p_sentence(self, p):
		"""
		sentence : atomsent
				| boolsent
		"""

	def p_atomsent(self, p):
		"""
		atomsent : OPEN predicate termseq CLOSE
		"""
	def p_boolsent(self, p):
		"""
		boolsent : OPEN AND starter CLOSE
				| OPEN OR starter CLOSE
				| OPEN IFF sentence sentence CLOSE 
				| OPEN IF sentence sentence CLOSE 
				| OPEN NOT sentence CLOSE
		"""

	def p_termseq(self, p):
		"""
		termseq : interpretedname
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



myPars = ClifParser()
 

parser = myPars.parser

myFile = open("a3-valid-clif1-v2.txt",'r')
#parser.parse(myFile.read())

for line in myFile:
	print("Parsing: "+ line)
	parser.parse(line)
		

