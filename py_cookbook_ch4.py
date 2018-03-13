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
        return iter(self._children)

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
'''Node(0)
Node(1)
Node(3)
Node(4)
Node(2)
Node(5)'''




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
