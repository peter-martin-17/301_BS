import ply.lex as lex
import re

myFile = open("lexer_output.txt", 'w')

class ClifLexer():

	# CONSTRUCTOR
	def __init__(self):
		print('Lexer constructor called.')
		myFile.write('Lexer constructor called.' + '\n')
		self.lexer = lex.lex(module=self)
		# start in the (standard) initial state
		self.lexer.begin('INITIAL')

	# DESTRUCTOR
	def __del__(self):
		print('Lexer destructor called.')
		#myFile.write('Lexer destructor called.' + '\n')

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


	tokens = ['OPEN', 'CLOSE', 'QUOTEDSTRING', 'RESERVEDELEMENT', 'NUMERAL', 'LEXICALTOKEN', 'COMMENT']

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

	def t_QUOTEDSTRING(self, t):
		# This is not yet correct: you need to complete the lexing of quotedstring
		#r'[t_STRINGQUOTE&t_CHAR|t_NAMEQUOTEt_STRINGQUOTE]'
		#r"\'\w+\'"
		#r"\'[\w?~!\#$%^&*_+{}|=:<>\|,./\[\]\;\-]+\' | \'[\"]+\'"
		r"\'[\w?~!\#$%^&*_+{}|=:\"<>\|,./\[\]\;\-]+\'"
		return t

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
			myFile.write(str(tok) + '\n')



lex = ClifLexer()
s = "(and ('B' 'C') (or ('C' 'D')) (or ('FuncB') ('Func' 100 'A') ('something')))"
print('\n' + 'Lexing '+s)
myFile.write('\n' + 'Lexing '+s + '\n')
lex.lex(s)

s = "(and ('B' 'C') (or ('C' 'D'))))"
print('Lexing '+s)
myFile.write('\n' + 'Lexing '+s + '\n')
lex.lex(s)

# the following is currently not working but should be accepted because ? is in the set char
s = "('who' 'is' '?')"
print('Lexing '+s)
myFile.write('\n' + 'Lexing '+s + '\n')
lex.lex(s)

s = "('A1:\"A_comment_inside\"' 'COMMENT:B100%')"
print('Lexing '+s)
myFile.write('\n' + 'Lexing '+s + '\n')
lex.lex(s)

myFile.write('\n' + 'Lexer destructor called.')
myFile.close()
