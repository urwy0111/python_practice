#CH8

#8.1. Changing the string representation of Instances
#Change the output produced by printing or viewing instances to something more sensible
#using __str__() and __repr__() methods
class Pair:
    def __init__(self, x, y):
        self.x = x
        self. y = y
    def __repr__(self):
        return 'Pair({0.x!r},{0.y!r})'.format(self)
    def __str__(self):
        return '({0.x!s}, {0.y!s})'.format(self)

p = Pair(3,4)
p # gives Pair(3, 4)
print (p) #gives (3, 4)




#8.2. Customizing string formatting
#to customize string fomatting, define the __format__() method on a class
_formats = {
    'ymd' : '{d.year}-{d.month}-{d.day}',
    'mdy' : '{d.month}/{d.day}/{d.year}',
    'dmy' : '{d.day}/{d.month}/{d.year}'
    }
class Date:
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day
    def __format__(self, code):
        if code == '':
            code = 'ymd'
        fmt = _formats[code]
        return fmt.format(d=self)

d = Date(2012, 12, 21)
format(d)  # gives '2012-12-21'
format(d, 'mdy') #gives '12/21/2012'
'The date is {:ymd}'.format(d) #gives 'The date is 2012-12-21'
'The date is {:mdy}'.format(d) #gives 'The date is 12/21/2012'

from datetime import date
d = date(2012,12,21)
format(d) #gives '2012-12-21'
format(d, '%A, %B, %d, %Y') # 'Friday, December, 21, 2012'
'The end is {:%d %b %Y}. Goodbye'.format(d) #gives 'The end is 21 Dec 2012. Goodbye'




#Making objects support the context-management protocol
# Implement  __enter__() and __exit__() methods
#Example, class to provide a network connection

from socket import socket, AF_INET, SOCK_STREAM
class LazyConnection:
    def __init__(self, address, family=AF_INET, type=SOCK_STREAM):
        self.address = address
        self.family = AF_INET
        self.type = SOCK_STREAM
        self.sock = None

    def __enter__(self):
        if self.sock is not None:
            raise RuntimeError('Already connected')
        self.sock = socket(self.family, self.type)
        self.sock.connect(self.address)
        return self.sock

    def __exit__(self, exc_ty, exc_val, tb):
        self.sock.close()
        self.sock = None


from functools import partial
conn = LazyConnection(('www.python.org', 80))
#connection closed
with conn as s:
    #conn.__enter__() executes: connection open
    s.send(b'GET /index.html HTTP/1.0\r\n')
    s.send(b'Host: www.python.org\r\n')
    s.send(b'\r\n')
    resp = b''.join(iter(partial(s.recv, 8192), b''))
    #conn.__exit__() executes: connection closed


from socket import socket, AF_INET, SOCK_STREAM

class LazyConnection:
    def __init__(self, address, family=AF_INET, type=SOCK_STREAM):
        self.address = address
        self.family = AF_INET
        self.type = SOCK_STREAM
        self.connections = []

    def __enter__(self):
        sock = socket(self.family, self.type)
        sock.connect(self.address)
        self.connections.append(sock)
        return sock

    def __exit__(self, exc_ty, exc_val, tb):
        self.connections.pop().close()
#example use
from functools import partial
conn = LazyConnection(('www.python.org', 80))
with conn as s1:
    ...
    with conn as s2:
        ...
        #s1 and s2 are independent sockets




#8.4. Saving memory when creating a large number of instances
#the program creates a large number of instances and uses a large amount of memory
#for classes that primarily serve as simple data structures,reduce the memory footprint by adding the __slots__ attributes to the class definition
class Date:
    __slots__ = ['year', 'month', 'day']
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day
#side ettect: no longer available to add new attributes to instances, __slots__ cannot have any other attributes added




#8.5. Encapsulating names in a class
class A:
    def __init__(self):
        self._internal = 0 # A internal attribute
        self.public = 1 # A public attribute

    def public_method(self):
        '''
        A public method
        '''

    def _internal_method(self):




#8.6. Creating managed attributes
#add extra processing (e.g. type checking or validation) to the getting or setting of an instance attribute
#A simple way to customize access to an attribute is to define it as a 'property'
#Example: defines a property that adds simple type checking to an attribute
class Person:
    def __init__(self, first_name):
        self.first_name = first_name

    #getter function
    @property
    def first_name(self):
        return self._first_name

    #setter function
    @first_name.setter
    def first_name(self, value):
        if not isinstance(value, str):
            raise TypeError('Expected a string')
        self._first_name = value

    #deleter function(optional)
    @first_name.deleter
    def first_name(self):
        raise AttributeError("Can't delete attribute")

a = Person('Guido')
a.first_name  #calls the getter    gives 'Guido'
a.first_name = 42 #calls the setter   raises TypeError
del a.first_name #calls the deleter   raises AttributeError

#properties can also be defined for existing get and set methods
class Person:
    def __init__(self, first_name):
        self.set_first_name(first_name)

    #getter function
    def get_first_name(self):
        return self._first_name

    #setter function
    def set_first_name(self, value):
        if not isinstance(value, str):
            raise TypeError('Expected a string')
        self._first_name = value

    #deleter function(optional)
    def del_first_name(self):
        raise AttributeError("Can't delete attribute")

#Make a property from existing get/set methods
name = property(get_first_name, set_first_name, del_first_name)

#use properties to define computed attributes
import math
class Circle:
    def __init__(self, radius):
        self.radius = radius

    @property
    def area(self):
        return math.pi * self.radius ** 2
    @property
    def perimeter(self):
        return 2 * math.pi *self.radius

c = Circle(4.0)
c.area #no ()
c.perimeter #no ()



#8.7. Calling a method on a parent class
#invoke a method in a parent class in place of a method that has been overridden in a subclass
#to call a method in a parent(or superclass), use the super() function
class A:
    def spam(self):
        print ('A.spam')

class B(A):
    def spam(self):
        print('B.spam')
        super().spam()    #call parent spam()

#use super() for handling of the __init__() method to make sure that parents are properly initialized
class A:
    def __init__(self):
        self.x = 0
class B(A):
    def __init__(self):
        super().__init__()
        self.y = 1

#in code that overides any of Python's special methods
class Proxy:
    def __init__(self, obj):
        self._obj = obj
#Delegate attribute lookup to internal obj
def __getattr__(self.name):
    return getattr(self._obj, name)
#Delegate attribute assignment
def __setattr__(self, name, value):
    if name.startswith('_'):
        super().__attr__(name, value)  #call original __setattr__
    else:
        setattr(self._obj, name, value)


#code directly calls a method in a parent
class Base:
    def __init__(self):
        print ('Base.__init__')
class A(Base):
    def __init__(self):
        Base.__init__(self)
        print ('A.__init__')

b = Base()  #gives 'Base.__init__'
c = A() #gives 'Base.__init__' \n  'A.__init__'

#this will lead to bizarre trouble in advanced code involving multiple inheritance
class Base:
    def __init__(self):
        print ('Base.__init__')
class A(Base):
    def __init__(self):
        Base.__init__(self)
        print('A.__init__')
class B(Base):
    def __init__(self):
        Base.__init__(self)
        print('B.__init__')
class C(A, B):
    def __init__(self):
        A.__init__(self)
        B.__init__(self)
        print('C.__init__')
c = C()
'''
Base.__init__
A.__init__
Base.__init__
B.__init__
C.__init__
'''

#change the code to use super()
class Base:
    def __init__(self):
        print('Base.__init__')
class A(Base):
    def __init__(self):
        super().__init__()
        print('A.__init__')
class B(Base):
    def __init__(self):
        super().__init__()
        print('B.__init__')
class C(A, B):
    def __init__(self):
        super().__init__()
        print ('C.__init__')
c = C()
'''
Base.__init__
B.__init__
A.__init__
C.__init__
'''

#use super() in a class with no parent at all
class A:
    def spam(self):
        print('A.spam')
        super().spam()
a = A()
a.spam()
'''
A.spam
Traceback (most recent call last):
  File "<pyshell#17>", line 1, in <module>
    a.spam()
  File "<pyshell#13>", line 4, in spam
    super().spam()
AttributeError: 'super' object has no attribute 'spam'
'''
class B:
    def spam(self):
        print('B.spam')
class C(A, B):
    pass
c = C()
c.spam()
'''
A.spam
B.spam
'''


#8.8. Extending a property in a subclass
#consider the following code, which defines a property
class Person:
    def __init__(self, name):
        self.name = name

    #getter function
    @property
    def name(self):
        return self._name

    #setter function
    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError('Expected a string')
        self._name = value

    #deleter function
    @name.deleter
    def name(self):
        raise AttributeError("Can't delete attribute")

#example of a class that inherits from Person and extends the name property with new functionality
class SubPerson(Person):
    @property
    def name(self):
        print ('Getting nsme')
        return super().name
    @name.setter
    def name(self, value):
        print ('Setting name to', value)
        super(SubPerson, SubPerson).name.__set__(self, value)
    @name.deleter
    def name(self):
        print ('Deleting name')
        super(SubPerson, SubPerson).name.__delete__(self)

#example of new class in use
s = SubPerson('Guido') #gives
s.name # gives
s.name = 'Larry'
s.name = 42 # TypeError('Expected a string')

#only extend one of the methods of a property
class SubPerson(Person):
    @Person.name.getter  # @Person.getter is also OK?
    def name(self):
        print ('Getting name')
        return super().name

# or just the setter
class SubPerson(Person):
    @Person.name.setter
    def name(self, value):
        print ('Setting name to', value)
        super(SubPerson, SubPerson).name.__set__(self, value)




#8.9. Creating a new kind of class or instance attribute
#create a new kind of instance sttribute type with some extra functionality, such as type checking

#create an entirely new kind of instance attribute, define its functionality in the form of a descriptor class

#descriptor attribute for an integer type-checked attribute
class Integer:
    def __init__(self, name):
        self.name = name

    def __get__(self, instance, cls):
        if instance is None:
            return self
        else:
            return instance.__dict__[self.name]

    def __set__(self, instance, value):
        if not isinstance(value, int):
            raise TypeError('Expected an int')
        instance.__dict__[self.name] = value

    def __delete__(self, instance):
        del instance.__dict__[self.name]
