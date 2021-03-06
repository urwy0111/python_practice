#CH4 Iterators and Generators

#4.1. Manually consuming an Iterator
with open ('/etc/passwd') as f:
    try:
        while True:
            line = next(f)
            print (line, end = '')
    except StopIteration:
        pass

with open('etc/passwd') as f:
    while True:
        line = next(f, None)
        if line is None:
            break
        print (line, end = '')

items = [1, 2, 3]
it = iter(items)
next(it) #gives 1
next(it) #gives 2
next(it) #gives 3
next(it) #gives error: StopIteration



#Delegating StopIteration
class Node:
    def __init__(self, value):
        self._value = value
        self._children = []
    def __repr__(self):
        return 'Node({!r})'.format(self._value)
    def add_child(self, node):
        self._children.append(node)
    def __iter__(self):
        return iter(self._children)   #Return了children,就是在children这个list中迭代

#Example
if __name__ == '__main__':
    root = Node(0)
    child1 = Node(1)
    child2 = Node(2)
    root.add_child(child1)
    root.add_child(child2)
    for ch in root:
        print(ch)
    #Outputs Node(1), Node(2)




#4.3. Creating new iteration patterns with Generators
# A custom iteration pattern that's different than the usual built-in functions(e.g. range(), reversed(), etc.)
# Define a new kind of iteration pattern using generator function
def frange(start, stop, increment):
    x = start
    while x < stop:
        yield x  #方程中使用yield可以获得多个itorator的返回值
        x += increment

for n in frange(0, 4, 0.5):
    print (n)

#gives
'''0.5
1.0
1.5
2.0
2.5
3.0
3.5
'''

list(frange(0, 1, 0.125)) # gives [0, 0.125, 0.25, 0.375, 0.5, 0.625, 0.75, 0.875]

# yield statement in a function turns it into a generator, a generator function only runs in response to iteration

def countdown(n) :
    print ('Starting to count from', n)
    while n > 0:
        yield n
        n -= 1
    print ('Done!')

c = countdown(3) #gives <generator object countdown at 0x05B61060>
next(c) #gives Starting to count from 3 \n 3
next(c) #gives 2
next(c) #gives 1
next(c) #gives Done! \n
#  File "<pyshell#71>", line 1, in <module>
#    next(c)
#StopIteration     一旦generator function returns, iteration就结束了




#4.4. Implementing the iteration protocol
class Node:
    def __init__(self, value):
        self._value = value
        self._children = []
    def __repr__(self):
        return 'Node({!r})'.format(self._value)
    def add_child(self, node):
        self._children.append(node)
    def __iter__(self):
        return iter(self._children)
    def depth_first(self):
        yield self
        for c in self:
            yield from c.depth_first()
# Example
if __name__ == '__main__':
    root = Node(0)
    child1 = Node(1)
    child2 = Node(2)
    root.add_child(child1)
    root.add_child(child2)
    child1.add_child(Node(3))
    child1.add_child(Node(4))
    child2.add_child(Node(5))

    for ch in root.depth_first():
        print(ch)
#Outputs:
'''
Node(0)
Node(1)
Node(3)
Node(4)
Node(2)
Node(5)
'''

#分析
list(root.depth_first()) #gives [Node(0), Node(1), Node(3), Node(4), Node(2), Node(5)]
root._children == [Node(1), Node(2)]
child1._children == [Node(3), Node(4)]
child2._children == [Node(5)]
list(child1.depth_first()) == [Node(1), Node(3), Node(4)]
list(child2.depth_first()) == [Node(2), Node(5)]





# Iterating in reverse
#Use the built-in reversed() function
a = [1, 2, 3, 4]
for x in reversed(a):
    print x
# gives 4 \n 3 \n 2 \n 1
# reversed() 只适用于1. size can be determined; 2. the object implements the __reversed__() special method
#例如 print a file backwards
f = open('somefile')
for line in reversed(list(f)):
    print (line, end='')   #Turning an iterable into a list could consume a lot of memory if it's large

#The reversed iteration can be customized on user-defined classes if implementing the __reversed__() method
class Countdown:
    def __init__(self, start):
        self.start = start

    #Forward iterator
    def __iter__(self):
        n = self.start
        while n > 0:
            yield n
            n -= 1
    #Reverse iterator
    def __reversed__(self):
        n = 1
        while n <= self.start:
            yield n
            n += 1




#4.6. Defining generator functions with extra state
#Easily implement it as a class, putting the generator function code in the __iter__() method
from collections import deque
class linehistory:
    def __init__(self, lines, histlen = 3):
        self.lines = lines
        self.history = deque(maxlen = histlen)

    def __iter__(self):
        for lineno, line in enumerate(self.lines, 1):
            self.history.append((lineno, line))
            yield line

    def clear(self):
        self.history.clear()

with open('haha.txt') as f:
    lines = linehistory(f)
    for line in lines:
        if 'python' in line:
            for lineno, hline in lines.history:
                print('{}:{}'.format(lineno, hline), end = '')




#4.7. Taking a slice of an iterator
def count(n):
    while True:
        yield n
        n += 1

c = count(0)
import itertools
for x in itertools.islice(c, 10, 20):
    print x
'''gives
10
11
12
13
14
15
16
17
18
19
'''
#无论是list(iterator)还是islice(iterator)，都会导致iterator前面的内容被consume了，无法再返回。要用西安转换成list的办法才能go back




#4.8. Skipping the first part of an iterable
#skip the first items according to a test function
from itertools import dropwhile
with open('/etc/passwd') as f:
    for line in dropwhile(lambda line: line.startswith('#'), f):
        print (line, end = '') # 只跳过最开始的'#'的注释部分，后面的就不跳过了

#If happen to know the exact number of items you want to skip, use itertools.islice()
from itertools import islice
items = ['a','b','c',1,4,10,15]
for x in islice(items, 3, None):
    print x

#繁琐的只跳过开头'#'注释部分
with open('/etc/passwd') as f:
# Skip over initial comments
while True:
    line = next(f, '')
    if not line.startswith('#'):
        break
# Process remaining lines
while line:
# Replace with useful processing
    print(line, end='')
    line = next(f, None)

#繁琐的跳过所有'#'注释部分
with open('/etc/passwd') as f:
    lines = (line for line in f if not line.startswith('#'))
    for line in lines:
        print(line, end='')




#4.9. Iterating over all possible combinations or permutations
items = ['a', 'b', 'c']
from itertools import permutations
for p in permutations(items):
    print (p)

for p in permutations(items, 2):
    print (p)

from itertools import combinations
for c in combinations(items, 3):
    print c

for c in combinations(items, 2):
    print c

for c in combinations(items, 1):
    print c

#可重复选取的组合
for c in combinations_with_replacement(items, 3):
    print (c)




#4.10. Iterating over the index-value pairs of a sequence
my_list = ['a', 'b', 'c']
for idx, val in enumerate(my_list):
    print(idx, val)
#gives
#0 a
#1 b
#2 c
for idx, val in enumerate(my_list, 1):
    print(idx, val)
#gives
#1 a
#2 b
#3 c

#This case is especially useful for tracking line numbers in files should you want to use a line number in an error message:
def parse_data(filename):   #这方程是干什么用的？
    with open(filename, 'rt') as f:
        for lineno, line in enumerate(f, 1):
            fields = line.split()
            try:
                count = int(fields[1])
            except ValueError as e:
                print ('Line {}: Parse error: {}'.format(lineno, e))


#generate a dictionary called word_summary, the key is the word and the value is the lineno where it appears, can be multiple times in the same line
from collections import defaultdict
word_summary = defaultdict(list)
with open('myfile.txt', 'r') as f:
    lines = f.readlines()
for idx, line in enumerate(lines):
    #create a list of words in current line
    words = [w.strip().lower() for w in line.split()]
    for word in words:
        word_summary[word].append(idx)




#4.11. Iterating over multiple sequences simultaneously
xpts = [1, 5, 4, 2, 10, 7]
ypts = [101, 78, 37, 15, 62, 99]
for x, y in zip(xpts, ypts):
    print(x, y) #the rest '99' is neglected

a = [1, 2, 3]
b = ['w', 'x', 'y', 'z']
for i in zip(a, b):
    print(i)

from itertools import zip_longest# izip_longest in python 2.0
for i in zip_longest(a, b):
    print (i)

for i in zip_longest(a, b, fillvalue = 'eshaha')
    print (i)

headers = ['name', 'shares', 'price']
values = ['ACME', 100, 490.1]
s = dict(zip(headers, values))  # to combine column headers and column values

for name, val in zip(headers, values):
    print (name, '=', val)  # to produce output

zip(a, b) #return a list of tuple pairs in py2, return an iterator(zip object)




#4.12. Iterating on items in separate containers
from itertools import chain
a = [1, 2, 3, 4]
b = ['x', 'y', 'z']
for x in chain(a, b):
    print (x)

#perform certain operations on all of the items at once but the items are pooled in different working sets
#various working sets of items
active_items = set()
inactive_items = set()
#iterate over all items
for item in chain(active_items, inactive_items):
    #process item




#4.13. Creating data processing pipelines




#4.14. Flattinng a nested sequence
#flattening a nested sequence into a single list of values, by writing a recursive generator function including a yield from statement

from collections import Iterable

def flatten(items, ignore_types = (str, bytes)):   #isinstance(x, )在此处判断的是x元素的特性，items包括3个数字，一个子大list
    for x in items:
        if isinstance(x, Iterable) and not isinstance(x, ignore_types):
            yield from flatten(x) #only for python 3
        else:
            yield x

items = [1, 2, [3, 4, [5, 6], 7], 8]

for x in flatten(items):
    print(x)    #produces 1 2 3 4 5 6 7 8

items2 = ['Dave', 'Paula', ['Thomas', 'Lewis']]
for x in flatten(items):
    print (x)    #produces Dave Paula Thomas Lewis

# the yield from statement is a nice shortcut to write generators to call other generators as subroutines. Without using it, we need to use an extra loop
def flaten(items, ignore_types=(str, bytes)):
    for x in items:
        if isinstance(x, Iterable) and not isinstance(x, ignore_types):
            for i in flatten(x):
                yield i
            else:
                yield x




#4.15. Iterating in sorted order over merged sorted iterables
import heapq
a = [1,4,7,10]
b = [2,5,6,11]
for c in heapq.merge(a, b):
    print (c)   # gives 1 2 4 5 6 7 10 11   merged and sorted result

heapq.merge(a, b)  # <generator object merge at 0x05896810>
#heapq.merge never reads any of the supplied sequences all at once. We can use it on very long sequences with very little overhead

#example of how to merge two sorted files
import heapq
with open('sprted_file_1', 'rt') as file1, open('sorted_file_2', 'rt') as file2, open('merged_file', 'wt') as outf:
    for line in heapq.merge(file1, file2):
        outf.write(line)




#4.16. Replacing infinite while loops with a iterator
#A somewhat common scenario in programs involving I/O is to write code like this:
CHUNKSIZE = 8192
def reader(s):
    while True:
        data = s.recv(CHUNKSIZE)
        if data ==b'':
            break
        process_data(data)
#replace above code with iter()
def reader(s):
    for chunk in iter(lambda: s.recv(CHUNKSIZE), b''):
        process_data(data)
