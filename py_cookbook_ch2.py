# 2.1. Splitting strings on any of multiple delimiters
line = 'asdf fkdk; afed, fjek,asdf,    foo'
import re
re.split(r'[;,\s]\s*', line)
#上述式子的输出是 ['asdf', 'fkdk', 'afed', 'fjek', 'asdf', 'foo']

# regular expression pattern involves a capture group enclosed in parentheses.
fields = re.split(r'(;|,|\s)\s*', line)
#上述式子的输出是 ['asdf', ' ', 'fkdk', ';', 'afed', ',', 'fjek', ',', 'asdf', ',', 'foo']，把delimiter也单列出来了

values = fields[::2]
delimiters = fields[1::2] + ['']
# Reform the line using the same delimiters
''.join(v+d for v, d in zip(values, delimiters))

#如果想要使用（）但是不用capture group，就需要使用noncapture group, specified as (?:...)
re.split(r'(?:,|;|\s)\s*', line)


#2.2 Matching text at the start or end of string
#Use str.startswith() or str.endswith() methods
filename = 'spam.txt'
filename.endswith('.txt') # gives True

import os
filenames = os.listdir('.')  # What's the use of '.' ?
filenames # gives all the filenames under current working directory
[name for name in filenames if name.endswith(('.c', '.h'))] # Provide a tuple for multiple choices
any(name.endswith('.py') for name in filenames)  # gives True; any takes a tuple comprehension as input

from urllib.request import urlopen
def read_data(name):
    if name.startswith(('http:', 'https:', 'ftp:')):
        return urlopen(name).read()
    else:
        with open(name) as f:
            return f.read()

#Perform basic prefix and suffix check with slices
filename = 'spam.txt'
filename[-4:]  == '.txt'

#Use regular expressions as an alternative
import re
url = 'http://www.python.org'
re.match('http:|https:|ftp:', url)



#2.3. Matching strings using shell wildcard patters wildcard:通配符
from fnmatch import fnmatch, fnmatchcase
fnmatch('foo.txt', '*.txt')  # gives True
fnmatch('foo.txt', '?oo,txt') # gives True
fnmatch('Dat45.csv', 'Dat[0-9]*') # gives True
names = ['Dat1.csv', 'Dat2.csv','config.ini', 'foo.py']
[name for name in names if fnmatch(name, 'Dat*.csv')]  #gives ['Dat1.csv', 'Dat2.csv']

fnmatchcase('foo.txt', '*.TXT') #gives False, case sensitive

#Use for data processing with nonfilename strings
addresses = [
'5412 N CLARK ST',
'1060 W ADDISON ST',
'1039 W GRANVILLE AVE',
'2122 N CLARK ST',
'4802 N BROADWAY',
]
from fnmatch import fnmatchcase
[addr for addr in addresses if fnmatchcase(addr, '*ST')]  # gives addresses with ST
[addr for addr in addresses if fnmatchcase(addr, '54[0-9][0-9] *CLARK*')]

# *用于字符串的省略时，前后都没有空格，前后都代表了；前有空格，仅代表后面的内容；后有空格，仅代表前面的内容
# [0-9]代表着0到9中任一个数字，既包括0也包括9



#2.4. Matching and searching for text patterns
#If the text trying to match is a simple literal, use str.find(), str.endswith() and str.startswith()
text = 'yeah, but no, but yeah, but no, but yeah'
text.find('no')  # gives 10

#For more complicated matching, use regular expression and the re module
text1 = '11/27/2012'
text2 = 'Nov 27, 2012'
import re
if re.match(r'\d+/\d+/\d+', text1):  # \d+ means match one or more digits
    print ('yes')
else:
    print ('no')  #gives yes

if re.match(r'\d+/\d+/\d+', text2):
    print ('yes')
else:
    print ('no')  # gives no
#如果想要测试match多组，最好先precompile the regular expression pattern into a pattern object
datepat = re.compile(r'\d+/\d+/\d+')
if datepat.match(text1):
    print('yes')
else:
    print('no')  #gives yes

#Use findall() method to search all occurences of a patterns
text = 'Today is 11/27/2012. PyCon starts 3/13/2013.'
datepat.findall(text)
#Regular Expressions 常用格式
datepat = re.compile(r'(\d+)/(\d+)/(\d+)')

#Capture groups simplify subsequent processing of the matched text because the contents of each group can be extracted individually
m = datepat.match('11/27/2012')
m.group(0) #gives '11/27/2012'
m.group(1) #gives'11'
m.groups() #gives a tuple ('11', '27', '2012')   This might be only for python 2.x version
month, day, year = m.groups()
datepat.findall(text)  # gives a list of two tuples [('11','27','2012'),('3','13','2013')]
for month, day, year in datepat.findall(text):
    print ('{}-{}-{}'.format(year, month, day)) #gives 2012-11-27 /n 2013-3-13
#findall() method returns a list, finditer() returns tuples iteratively
for m in datepat.finditer(text):
    print (m.groups()) #m 是储存的位置

# match() method only checks the beginning of a string
m = datepat.match('11/27/2012asdf')
m.group() #gives '11/27/2012'  和m.group(0)的return一样

# if you want an exact match, make sure the pattern includes the end-marker($)
datepat = re.compile(r'(\d+)/(\d+)/(\d+)$')
datepat.match('11/27/2012asdf')
datepat.match('11/27/2012')

#Use module-level functions in the re module to skip compilation step for simple text matching/searching
re.findall(r'(\d+)/(\d+)/(\d+)', text) #gives [('11','27','2012'), ('3', '13', '2013')]




# 2.5. Searching and replacing text
# For simple literal patterns, use str.replace() methods
text = 'yeah, but no, but yeah, but no, but yeah'
text.replace('yeah', 'yep')
# For more complicated patterns, use the sub() functions/methods in re module
text = 'Today is 11/27/2012. PyCon starts 3/13/2013'
import re
re.sub(r'(\d+)/(\d+)/(\d+)', r'\3-\1-\2', text)

datepat = re.compile(r'(\d+)/(\d+)/(\d+)')
datepat.sub(r'\3-\1-\2', text)

# For more complicated substitutions, it's possible to specify a substitution callback function
from calendar import month_abbr
def change_date(m):
    mon_name = month_abbr[int(m.group(1))]
    return '{} {} {}'.format(m.group(2), mon_name, m.group(3))
datepat.sub(change_date, text) #gives 'Today is 27 Nov 2012. PyCon starts 13 Mar 2013'

#re.subn() return两个值，一个sub,一个数目
newtext, n = datepat.subn(r'\3-\1-\2', text)
newnext # gives substitute result
n # gives how many substitutions made




#2.6. Searching and replacing case-insensitive text
#use the re module and supply the re.IGNORECASE flag to various operations
text = 'UPPER PYTHON, lower python, Mixed Python'
re.findall('python', text, flags = re.IGNORECASE)
re.sub('python', 'snake', text, flags = re.IGNORECASE)

#let the replacing text match the case of the matched text, by using a support function
def matchcase(word):
	def replace(m):
		text = m.group()
		if text.isupper():
			return word.upper()
		elif text.islower():
			return word.lower()
		elif text[0].isupper():
			return word.capitalize()
		else:
			return word
	return replace
re.sub('python', matchcase('snake'), text, flags = re.IGNORECASE)



#2.7. Specifying a regular expression for the shortest match
str_pat = re.compile(r'\"(.*)\"')
text1 = 'Computer says "no."'
str_pat.findall(text1) #gives ['no.']
text2 = 'Computer says "no." Phone says "yes."'
str_pat.findall(text2) #gives ['no." Phones says "yes.'] 找出了最长的match since * is greedy
#Use ? modifier after * operator in the pattern to fix this
str_pat = re.compile(r'\"(.*?)\"')
str_pat.findall(text2) # gives ['no.', 'yes.']




#2.8. Writing a regular expression for multiple patterns
# dot(.) can match any character but cannot match newlines
comment = re.compile(r'/\*(.*?)\*/')
text1 = '/* this is a comment */'
text2 = '''/* this is a
              multiline comment */
        '''
comment.findall(text1) #gives ['this is a comment']
comment.findall(text2) #gives []
#To fix this problem, add support for newlines
comment = re.compile(r'/\*((?:.|\n)*?)\*/')
comment.findall(text2) #gives [' this is a\n              multiline comment ']

#In re.compile(), use a flag called re.DOTALL. It makes '.' in a regular expression match all characters, including newlines
comment = re.compile(r'/\*(.*?)\*/', re.DOTALL)
comment.findall(text2) # gives [' this is a\n              multiline comment ']




#2.9. Normalizing Unicode textr to a standard representation
s1 = 'Spicy Jalape\u00f1o' #gives 'Spicy Jalapeño'
s2 = 'Spicy Jalapen\u0303o' #gives 'Spicy Jalapeño'
s1 == s2 # gives False
len(s1) #gives 14
len(s2) #gives 15

#Having multiple representations is a problem for strings compraration.
#Normalize the text into a standard representation using the unicodedata module
import unicodedata
t1 = unicodedata.normalize('NFC', s1)
t2 = unicodedata.normalize('NFC', s2)
t1 == t2 # gives True
print (ascii(t1)) # gives 'Spicy Jalape\xf1o'
t3 = unicodedata.normalize('NFD', s1)
t4 = unicodedata.normalize('NFD', s2)
t3 == t4 #gives True
print (ascii(t3)) # gives 'Spicy Jalapen\u0303o'



#2.10. Working with Unicode characters in regular expressions
import re
num = re.compile('\d+')
num.match('123') #gives <_sre.SRE_Match object; span=(0, 3), match='123'>
num.match('\u0661\u0662\u0663') #gives <_sre.SRE_Match object; span=(0, 3), match='١٢٣'>




#2.11. Stripping unwanted characters from strings
#Whitespace Stripping
s = '    hello world   \n'
s.strip()  #gives 'hello world'
s.lstrip() #gives 'hello world   \n'
s.rstrip() #gives '    hello world'
t = '-----hello====='
t.lstrip('-')
t.strip('-=') #gives 'hello'

#the strip does not apply to any text in the middle of a string
s = ' hello     world   \n'
s.strip() #gives 'hello     world'
#Use replace() method or a regular expression to the inner space
s.replace(' ', '') #gives 'helloworld\n'
import re
re.sub('\s+', '', s) #gives 'helloworld'

#combine string stripping with other iterative processing, using generator expression
with open(filename) as f:
    lines = (line.strip() for line in f) #efficient, because this doesn't creat any temp list
    for line in lines:
        ...




#2.12. Sanitizing and cleaning up text
s = 'pýtĥöñ\fis\tawesome\r\n'
#step1:clean up the Whitespace by making a small translation table and use translate()
remap = {
    ord('\t') : ' ',
    ord('\f') : ' ',
    ord('\r') : None    #Deleted
}
a = s.translate(remap) #gives pýtĥöñ is awesome\n'

#remove all combining characters
import unicodedata
import sys
cmb_chrs = dict.fromkeys(c for c in range(sys.maxunicode) if unicodedata.combining(chr(c)))
b = unicodedata.normalize('NFD', a)
b #gives 'pýtĥöñ is awesome\n'
b.translate(cmb_chrs) #gives 'python is awesome\n'

#Another example, a translation table that maps all Unicode decimal digit characters to their equivalent in ASCII
digitmap = {c: ord('0') + unicodedata.digit(chr(c)) for c in range(sys.maxunicode) if unicodedata.category(chr(c)) == 'Nd'}
len(digitmap) #gives 580

x = '\u0661\u0662\u0663'
x.translate(digitmap) #gives '123'

#I/O decoding and encoding
a = 'pýtĥöñ is awesome\n'
b = unicodedata.normalize('NFD', a)
b.encode('ascii', 'ignore').decode('ascii') #gives 'python is awesome\n'
#??( b.encode('ascii', 'ignore').decode('ascii') ) will give 'pt is awesome\n'  WHY?



#2.13. Aligning text strings
text = 'hello world'
text.ljust(20) #gives 'hello world         '
text.rjust(20) #gives '         hello world'
text.center(20) #gives '    hello world     '
text.center(20, '=') #gives '====hello world====='
text.rjust(20,'=') #gives '=========hello world'
format(text, '>20') #gives '         hello world'
format(text, '<20') #gives 'hello world         '
format(text, '^20') #gives '    hello world     '
format(text, '=>20s') #gives '=========hello world'

#Use format codes in the format() methods when foematting multiple values
'{:>10s} {:>10s}'.format('hello', 'world') #gives '     hello      world'

#format() is not specific to strings
x = 1.2345
format(x, '>10') #gives '    1.2345'
format(x, '10.2f') #gives '      1.23'
#format function & format method 对任何都管用， ljust(), rjust(), center()只对string管用




#2.14. Combining and concatenating strings
#combine many small strings into a larger string
parts = ['Is', 'Chicago', 'Not', 'Chicago']
' '.join(parts)
''.join(parts)

a = 'hello' 'world' #gives  'helloworld'

data = ['ACME', 50, 91.1]
','.join(str(d) for d in data)

print(a, b, c, sep = ':')

#building output from lots of strings, write the code as generator function, use yield to emit fragments
def sample():
    yield 'Is'
    yield 'Chicago'
    yield 'Not'
    yield 'Chicago?'
#simply join the fragments
text = ''.join(sample())
#redirect the fragmens to I/O
for part in sample():
    f.write(part)
#Hybrid Scheme that's smart about combining I/O operations
def combine(source, maxsize):
    parts = []
    size = 0
    for part in source:
        parts.append(part)
        size += len(part)
        if size > maxsize:
            yield ''.join(parts)
            parts = []
            size = 0
        yield ''.join(parts)
for part in combine(sample(), 32768):
    f.write(part)




#2.15. Interpolating variables in strings
#by using format() method of strings
s = '{name} has {n} messages.'
s.format(name = 'Guido', n = 37) # gives 'Guido has 37 messages.'

#if the value are found in variables, use combination of format_map() and vars()
name = 'Guido'
n = 37
s.format_map(vars()) #gives 'Guido has 37 messages.'

# vars() also works with instances
class Info:
    def __init__(self, name, n):
        self.name = name
        self.n = n
a = Info('Guido', 37)
s.format_map(vars(a)) #gives 'Guido has 37 messages.'

#vars 的缺点是如果没有n，name也就不能用了，用dictionary class来解决
class safesub(dict):
    def __missing__(self, key):
        return '{' + key + '}'
del n
s.format_map(safesub(vars())) #gives 'Guido has {n} messages.'

#常用的话，hide the variable substitution process behind a small utility function that employs a so-called 'frame hack'
import sys
def sub(text):
    return text.format_map(safesub(sys._getframe(1).f_locals))
#然后就可以做如下操作：
name = 'Guido'
n = 37
print (sub('Hello {name}'))
print (sub('You have {n} messages'))
print (sub('Your favorite color is {color}'))




#2.16. Reformatting text to a fixed number of columns
# use the textwrap module to reformat text for output.
s = "Look into my eyes, look into my eyes, the eyes, the eyes, \
the eyes, not around the eyes, don't look around the eyes, \
look into my eyes, you're under."
import textwrap
print (textwrap.fill(s, 70))
#gives
'''
Look into my eyes, look into my eyes, the eyes, the eyes, the eyes,
not around the eyes, don't look around the eyes, look into my eyes,
you're under.
'''
print (textwrap.fill(s, 40))
#gives
'''
Look into my eyes, look into my eyes,
the eyes, the eyes, the eyes, not around
the eyes, don't look around the eyes,
look into my eyes, you're under.
'''
print (textwrap.fill(s, 40, initial_indent = '    '))
#gives
'''
    Look into my eyes, look into my
eyes, the eyes, the eyes, the eyes, not
around the eyes, don't look around the
eyes, look into my eyes, you're under.
'''
print (textwrap.fill(s, 40, subsequent_indent = '    '))
'''
Look into my eyes, look into my eyes,
    the eyes, the eyes, the eyes, not
    around the eyes, don't look around
    the eyes, look into my eyes, you're
    under.
'''
#用来fit terminal 的size
import os    #获取terminal的size
os.get_terminal_size().columns
