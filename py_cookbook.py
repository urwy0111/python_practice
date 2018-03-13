#1.16 Filtering Sequence Elements
# filter() Function
values = ['1','2','-3','-','4','N/A','5']
def is_int(val):
    try:
        x = int(val)
        return True
    except ValueError:
        return False
ivals = list(filter(is_int, values)) #filter() creates an iterator, use list() to group them
print ivals

#list comprehension vs. generator expressions:
#list comprehension may produce a large result if the original input is large
mylist = [1,4,-5,10,-7,2,3,-1]
[n for n in mylist if n > 0] #list comprehension

pos = (n for n in mylist if n > 0)
pos   #<generator object <genexpr> at 0x1006a0eb0>
for x in pos:
    print (x)   #result is an iterator

#如果不想直接过滤掉不想要的item，可以用conditional expressions
 clip_neg = [n if n > 0 else 0 for n in mylist] # still no colon

 #另一种使用itertools.compress
addresses = [
'5412 N CLARK',
'5148 N CLARK',
'5800 E 58TH',
'2122 N CLARK'
'5645 N RAVENSWOOD',
'1060 W ADDISON',
'4801 N BROADWAY',
'1039 W GRANVILLE',
]
counts = [0,3,10,4,1,7,6,1]
from itertools import compress
more5 = [n > 5 for n in counts] #这个输出结果是一个Boolean mylist
list(compress(addresses, more5))  # ['5800 E 58TH', '4801 N BROADWAY', '1039 W GRANVILLE']


# 1.17. Extract a subset of a dictionary
#方法1： 使用dictionary comprehension
prices = {
'ACME': 45.23,
'AAPL': 612.78,
'IBM': 205.55,
'HPQ': 37.20,
'FB': 10.75
}
p1 = {key:value for key, value in prices.items() if value > 200}   #对于value选择
tech_names = {'AAPL', 'IBM', 'HPQ', 'MSFT'}
p2 = {key:value for key, value in prices.items() if key in tech_names}    #对于key的值选择

#方法2: Create a sequence of tuples and pass them to the dict() function
p1 = dict((key, value) for key, value in prices.items() if value >200)

#方法3:调用dictionary的key，选出和tech_names中相同的组成新的dictionary
p2 = {key:prices[key] in prices.keys() & tech_names} # 此方法比第一种方法慢1.6倍


#1.18 Mapping names to sequence Elements
from collections import namedtuple
Subscriber = namedtuple('Subscriber', ['addr', 'joined'])
sub = Subscriber('jonesy@example.com', '2012-10-19')
sub   # gives Subscriber(addr = 'jonesy@example.com', joined = '2012-10-19')
sub.addr #gives 'jonesy@example.com'
sub.joined #gives '2012-10-19'

#支持所有tuple的常规operation，例如indexing 和 unpacking
len(sub)  # gives 2
addr, joined = sub # gives value to two variables

#named tuple can be used to replace dictionary, which requires more space to store,but it's immutable
#use _replace() to generate a entirely new namedtuple with replaced values
from collections import namedtuple
Stock = namedtuple('Stock', ['name','shares','price'])
s = Stock('ACME',100, 123.45)
s = s._replace(shares = 72)

# Use _replace() method to populate named tuples that have optional or missing values
from collections import namedtuple
Stock = namedtupe('Stock', ['name', 'shares', 'price', 'date', 'time'])
stock_prototype = Stock('', 0, 0, None, None)  #Create a prototype instance
def dict_to_stock(s):
    return stock_prototype._replace(**s)  # function to conver dict to Stock
a = {'name': 'ACME', 'shares': '100', 'price': 123.45}
dict_to_stock(a)
b = {'name': 'ACME', 'shares': '100', 'price': 123.45, 'date': '12/17/2012'}



#1.19. Transforming and reducing data at the same time
nums = [1,2,3,4,5]
s = sum(x*x for x in nums)

#determine if any .py file exist in a dictionary
import os
files = os.listdir('dirname')
if any(name.endswith('.py') for name in files):
    print('There be python!')
else:
    print('Sorry, no python.')

#Output a tuple as CSV
s = ('ACME', 50, 123.45)
print(','.join(str(x) for x in s))

#Data reduction across fields of a data structure
portfolio = [
    {'name':'GOOG', 'shares': 50},
    {'name':'YHOO', 'shares': 75},
    {'name':'AOL', 'shares': 20},
    {'name':'SCOX', 'shares': 65}
]
min_shares = min(s['shares'] for s in portfolio)  #返回值是value 20

# s = sum((x*x for x in nums))和s = (x*x for x in nums)是一样的，省略了一组括号
#如果不用generator expressions, 就需要先产生一个temp list
s = sum([x*x for x in nums])  #使用list comprehension 先产生一个temp list

#Certain reduction functions accept a key argument
min_shares = min(portfolio, key = lambda s: s['shares']) #返回值是整条dict



#Combining multiple mappings into a single mapping
a = {'x': 1, 'z': 3}
b = {'y': 2, 'z': 4}
from collections import ChainMap
c = ChainMap(a, b)
#key value 'z'有重复，所以留用第一个mapping里的value
#当mutate the mapping时，总是affact第一个mapping,即使这个key只在后面的mapping里有
c['y'] = 25 #Add an item to a instead of chaning values in b

# A ChainMap is particularly useful when working with scoped values as variables in a programming language(i.e. globals, locals, etc.)
values = ChainMap()
values['x'] = 1
# Add a new mapping
values = values.new_child()
values['x'] = 2
# Add a new mapping
values = values.new_child()
values['x'] = 3
values    #gives ChainMap({'x': 3}, {'x': 2}, {'x': 1})
values['x']    #gives 3
# Discard last mapping
values = values.parents
values['x']    #gives 2
# Discard last mapping
values = values.parents
values['x']    #gives 1
values    #gives ChainMap({'x': 1})

#另一种merge dictionaries的办法是用update() method
a = {'x': 1, 'z': 3}
b = {'y': 2, 'z': 4}
merged = dict(b)
merged.update(a)
