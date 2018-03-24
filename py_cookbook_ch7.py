#CH7

#7.1. Writing functions that accept any numbers of arguments
# use * argument to accept any number positional arguments
def avg(first, *rest):
    return (first + sum(rest))/(1+len(rest))
avg(1,2) #gives 1.5
avg(1,2,3,4) # gives 2.5
# use ** to accept any number of keyward arguments
import html
def make_element(name, value, **attrs):
    keyvals = [' %s="%s"' % item for item in attrs.items()]
    attr_str = ''.join(keyvals)
    element = '<{name}{attrs}>{value}</{name}>'.format(name=name,attrs=attr_str,value=html.escape(value))
    return element
# Creates '<item size="large" quantity="6">Albatross</item>'
make_element('item', 'Albatross', size='large', quantity=6) #gives '<item size=large" quantity=6">Albatross</item>'
# Creates '<p>&lt;spam&gt;</p>'
make_element('p', '<spam>') # gives '<p>&lt;spam&gt;</p>'




# 7.2. Writing functions that only accept keyward arguments
#want a function to only accept certain arguments by keyward
#place the keyward arguments after a * argument or a single unnamed *
def recv(maxsize, *, block):
    'Receives a message'
    pass

recv(1024, True) #TypeError: recv() takes 1 positional argument but 2 were given
recv(1024, block = True)

def minimum(*values, clip=None):
    m = min(values)
    if clip is not None:
        m = clip if clip > m else m
    return m
minimum(1,5,2,-5,10)
minimum(1,5,2,-5,0,clip=0)




#7.3. Attaching Informational Metadata to function arguments
#function arguments annotations
#annotated function example
def add(x:int, y:int) -> int:
    return x + y



#7.4. Returning multiple values from a function
#simply return a tuple
def myfun():
    return 1, 2, 3
a,b,c = myfun() #gives a1 b2 c3



#7.5. Defining functions with default arguments
#define a function or method where one or more of the arguments are optional and have a default value
def spam(a, b=42):
    print (a,b)
spam(1) #a=1, b=42
smap(1, 2) #a=1 b=2

#if the default value is a mutable container, use None as the default and write code like this
#using a list as a default value
def spam(a, b=None):
    if b is None:
        b=[]
    print(a,b)

_no_value = object()
def spam(a, b=_no_value):
    if b is _no_value:
        print ('No b value supplied')
    print(a,b)

#never use a empty list as a default value
def spam(a, b=[]):
    print (b)
    return b
x = spam(1) # x gives []
x.append(99)
x.append('Yow!')
spam(1) #x gives [99,'Yow']

#use 'if b is None' to check the default value
def spam(a, b=None):
    if not b:
        b = []
    print(b)
    return b




#7.6. Defining anonymous or inline functions
#uusing lambda expression
add = lambda x, y: x + y
add(2, 3) #gives 5
add('hello','world') # gives 'helloworld'
#typically, lambda is used in the context of some other operation, such as sorting or a data reduction
names = ['David Beazley', 'Brian Jones', 'Raymond Hetinger', 'Ned Batchelder']
sorted(names, key = lambda name: name.split()[-1].lower())
['Ned Batchelder', 'David Beazley', 'Raymond Hetinger', 'Brian Jones']




#7.7. Capturing variables in anonymous functions
#you've defined an anonymous function using lambda, but you also need to capture the values of certain variables at the time of definition
x = 10
a = lambda y: x + y
a(10) # gives 20
x = 20
a = lambda y: x + y
a(10) #gives 30

#to avoid this and fix x, include the value of x as a default value
x = 10
a = lambda y, x=x: x + y
a(10) #gives 20
x = 20
b = lambda y, x=x: x + y
a(10) #gives 20
b(10) #gives 30

#expect the lambda functions to remember the iteration variable at the time of deifinition
funcs = [lambda x: x+n for n in range(5)] # funcs is a list
for f in funcs:
    print(f(0))
'''
4
4
4;am
4
4
'''
funcs = [lambda x, n=n: x+n for n in range(5)]
for f in funcs:
    print(f(0))
'''
0
1
2
3
4
'''




#7.8.Making an N-arguments callable work as a callable with fewer arguments
# a callable used with some other python code, possibly as a callback function or handler, but it takes too many arguments and causes an exception when called
#to reduce the number of args to a function, use functools.partial()
def spam(a,b,c,d):
    print (a,b,c,d)
#use partial() to fix certain arguments values
from functools import partial
s1 = partial(spam,1)
s1(2,3,4) #gives 1,2,3,4
s2 = partial(spam,d=42)
s2(1,2,3) #gives 1,2,3,42
s3 = partial(spam, 1, 2, d=42)
s3(3) # gives 1,2,4,42

#making seemingly incompatible bits of code work together
points = [(1,2), (3,4), (5,6), (7,8)]
import math
def distance(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return math.hypot(x2-x1, y2-y1)

pt = (4, 3)
points.sort(key=partial(distance, pt))
points #gives [(3, 4), (1, 2), (5, 6), (7, 8)]

#Use partial() function to tweak the argument signatures of callback functions used in other libraries
def output_result(result, log=None):
    if log is not None:
        log.debug('Got:%r', result)
#a simple function
def add(x, y):
    return x + y

if __name__ == '__main__':
    import logging
    from multiprocessing import Pool
    from functools import partial

    logging.basicConfig(level=logging.DEBUG)
    log = logging.getLogger('test')

    p = Pool()
    p.apply_async(add, (3, 4), callback=partial(output_result, log=log))
    p.close()
    p.join()




#7.9. Replacing single method classes with functions
#example: used to fetch URLs using a kind of templating scheme
from urllib.request import urlopen
class UrlTemplate:
    def __init__(self, template):
        self.template = template
    def open(self, **kwargs):
        return urlopen(self.template.format_map(kwargs))
#example use. Download stock data from yahoo
yahoo = UrlTemplate('http://finance.yahoo.com/d/quotes.csv?s={names}&f={fields}')
for line in yahoo.open(names='IBM, APPL, FB', fields='sl1c1v'):
    print (line.decode('utf-8'))

#This class could be replaced with a much simpler function
def urltemplate(template):
    def opener(**kwargs):
        return urlopen(template.format_map(kwargs))
    return opener
#example use
yahoo =urltemplate('http://finance.yahoo.com/d/quotes.csv?s={names}&f={fields}')
for line in yahoo(names = 'IBM, APPL, FB', fields = 'sl1c1v'):
    print (line.decode('utf-8'))



#7.10 Carrying extra state with callback functions
#want the callback function carry extra state for use inside the callback function
def apply_async(func, args, *, callback):
    #compute the result
    result = func(*args)
    #invoke the callback with the result
    callback(result)
#example
def print_result(result):
    print('Got:', result)
def add(x, y):
    return x + y
apply_async(add, (2, 3), callback=print_result) # gives Got: 5
apply_async(add, ('hello', 'world'), callback=print_result) #gives Got: helloworld

#carry extra information in a callback, use a bound-method instead of a simple function
#example: this class keeps an internal sequence number that is incremented every time a result is received:
class ResultHandler:
    def __init__(self):
        self.sequence = 0
    def handler(self, result):
        self.sequence += 1
        print ('[{}] Got: {}'.format(self.sequence, result))
#to use this class, create an instance and use the bound method handler as the callback
r = ResultHandler()
apply_async(add, (2,3), callback=r.handler) #gives [1] Got: 5
apply_async(add, ('hello','world'), callback=r.handler) #gives [2] Got: helloworld

#use closure to capture state instead
def make_handler():
    sequence = 0
    def handler(result):
        nonlocal sequence
        sequence += 1
        print ('[{}] Got: {}'.format(sequence, result))
    return handler
#to use this
handler = make_handler()
apply_async(add, (2,3), callback=handler)
apply_async(add, ('hello', 'world', callback=handler))

#use coroutine
def make_handler():
    sequence = 0
    while True:
        result = yield
        sequence += 1
        print ('[{}] Got: {}'.format(sequence, result))
#for a coroutine, use its send() method as the callback
handler = make_handler()
next(handler) #Advance to yield
apply_async(add,(2,3),callback=handler.send)

#use an extra argument and partial function to carry state into a callback
class SequenceNo:
    def __init__(self):
        self.sequence = 0
def handler(result, seq):
    seq.sequence +=1
    print ('[{}] Got: {}'.format(seq.sequence, result))
seq = SequenceNo()
from functools import partial
apply_async(add, (2,3), callback=partial(handler, seq=seq))
#using lambda to replace partial()
apply_async(add, (2,3), callback=lambda r: handler(r, seq))









#7.11. Inlining callback function
def apply_async(func, args, *, callback):
    result = func(*args)
    callback(result)

#these two fragments will allow you to inline the callback steps using yield statements
from queue import Queue
from functools import wraps
class Async:
    def __init__(self, func, args):
        self.func = func
        self.args = args
def inlined_async(func):
    @wraps(func)
    def wrapper(*args):
        f = func(*args)
        result_queue = Queue()
        result_queue.put(None)
        while True:
            result = result_queue.get()
            try:
                a = f.send(result)
                apply_async(a.func, a.args, callback=result_queue.put())
            except StopIteration:
                break
        return wrapper

def add(x,y):
    return x + y

@inlined_async
def test():
    r = yield Async(add, (2,3))
    print(r)
    r = yield Async(add, ('hello','world'))
    print(r)
    for n in range(10):
        r = yield Async(add, (n,n))
        print r
    print('Goodbye')




#7.12. Accessing variables defined inside a closure
#make inner variables of a closure accessible by writing accessor functions and attaching them to the closure as function attributes
def sample():
    n = 0
    #closure function
    def func():
        print ('n=', n)
    #Accessor method for n
    def get_n():
        return n
    def set_n():
        nonlocal n
        n = value

    #Attach as function attributes
    func.get_n = get_n
    func.set_n = set_n
    return func

#example
f = sample()
f() #gives n= 0
f.set_n(10)
f() #gives n= 10
f.get_n() #gives 10
