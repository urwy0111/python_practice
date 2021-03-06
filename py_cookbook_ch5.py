#5.1 Reading and write text data
#read and write data in different texting encodings such as ASCII, UTF-8 or UTF-16

#Use open() function with mode 'rt' to read a text file
#Read the entire file as a single string
with open('somefile.txt', 'rt') as f:
    data = f.read()

#Iterate over lines of the file
with open('somefile.txt', 'rt') as f:
    for line in f:
        #process line

#Use open() with mode 'wt' to write a file, clearing and overwriting the previous contents(if any).
#Write chunks of text data
with open('somefile', 'wt') as f:
    f.write(text1)
    f.write(text2)  #连续写

#Redirected print statement
with open('somefile.txt', 'wt') as f:
    print(line1, file = f)
    print(line2, file = f) # 分行写

with open('somefile.txt', 'at') as f:
    print(line1, file = f)
    print(line2, file = f) # 续在后面  用mode 'at'

#use sys.getdefaultencoding() to find the system default text encoding
with open('somefile.txt', 'rt', encoding = 'latin-1') as f:
    #process

#if not use the 'with' statement, remember to close the file
f = open('somefile.txt', 'rt')
data = f.read()
f.close()

#read with disabled newline translation
with open('somefile.txt', 'rt', newline='') as f:
    ...

f = open('spain.txt', 'rt', encoding='ascii')
f.read() #UnicodeDecodeError
# Replace bad chars with Unicode U+fffd replacement char
f = open('sample.txt', 'rt', encoding='ascii', errors='replace')
f.read() #gives 'Spicy Jalape�o'
#Ignore bad chars entirely
g = open('sample.txt', 'rt', encoding='ascii', errors='ignore')
g.read() #gives 'Spicy Jalapeo!'




#5.2. Printing to a file
#redirect the output of the print() function to a file
#use the file keyword argument to print()
with open('somefile.txt', 'rt') as f:
    print ('Hello World', file = f)
#printing will fail if the underlying file is in binary mode rather than text mode




#5.3. Printing with a different separator or line ending
#use the sep and end keyword argument to print()
print('ACME', 50, 91.5) #ACME 50 91.5
print('ACME', 50, 91.5, sep=',') #ACME,50,91.5
print('ACME', 50, 91.5, sep=',', end='!!\n') #ACME,50,91.5!!

#Use of the end argument is also how you suppress the output of newlines in output
for i in range(5):
    print (i)
'''
0
1
2
3
4
'''
for i in range(5):
    print (i, end = ' ')  # 0 1 2 3 4

row = ('ACME', 50, 91.5)
print (','.join(str(x) for x in row))
#等同于
print (*row, sep = ',') #此处不加*打出来的是个list,前后有方括号




#5.4. Reading and writing binary data
# to read or write binary data, such as that found in images, sound files, and so on
#use open() function with mode 'rb' or 'wb' to read or write binary data

#read the entire file as a single byte string
with open('somefile.bin', 'rb') as f:
    data = f.read()
#write binary data to a file
with open('somefile.bin', 'wb') as f:
    f.write(b'Hello World')

#byte string
b = b'Hello World'
b[0] #gives 72

#decode or encode when read or write text from a binary-mode file
with open('somefile.bin', 'rb') as f:
    data = f.read(16)
    text = data.decode('utf-8')
with open('somefile.bin', 'wb') as f:
    text = 'Hello World'
    f.write(text.encode('utf-8'))

import array
nums = array.array('i', [1,2,3,4])
with open('data.bin', 'wb') as f:
    f.write(nums)

import array
a = array.array('i', [0, 0, 0, 0, 0, 0, 0, 0])
with open('data.bin', 'rb') as f:
    f.readinto(a)
a #gives array('i', [1, 2, 3, 4, 0, 0, 0, 0])




#5.5. Writing to a file that doesn't already exist, use x file mode (only for python 3)
with open('somefile', 'xt') as f:
    f.write('hello\n')  # will give FileExistError if file is alreay exist, no overwrite risk

#Alternative is to first test for the file
import os
if not os.path.exists('somefile'):
    with open('somefile', 'wt') as f:
        f.write('hello\n')
else:
    print ('file already exists')





#5.6. Performing I/O operations on a string
import io
s = io.StringIO()   #only for python 3
s.write('Hello World\n')
print ('This is a test', file = s)

#get all of the data written so far
s.getvalue() #gives 'Hello World\nThis is a test\n'

s = io.StringIO('Hello\nWorld\n')
s.read(4) # gives 'Hell'
s.read() # gives 'o\nWorld\n'

#use for binary file
s = io.BytesIO()
s.write(b'binary data')
s.getvalue() #gives b'binary data'




#5.7. Reading and writing compressed datafiles

#to read compressed file as text
#gzip compression
import gzip
with gzip.open('somefile.gz', 'rt') as f:
    text = f.read()
#bz2 compression
import bz2
with bz2.open('somefile.bz2', 'rt') as f:
    text = f.read()


#to write
with gzip.open('somefile.gz', 'wt') as f:
    text = f.write(text)
#bz2 compression
import bz2
with bz2.open('somefile.bz2', 'wt') as f:
    text = f.write(text)

#use file mode rb wb for binary file


with gzip.open('somefile.gz', 'wt', compresslevel= 5) as f: #default compresslevel is 9, highest
    f.write(text)


import gzip  #gzip.open() and bz2.open() can be layered on top of an existing file opened in binary mode
f = open('somefile.gz', 'rb')
with gzip.open(f, 'rt') as g:
    text = g.read()
# report error when trying




#5.8. Iterating over fixed-sized records
#use the iter() function and functools.partial() using this neat trick:
from functools import partial
RECORD_SIZE = 32
with open('somefile.data', 'rb') as f:
    records = iter(partial(f.read, RECORD_SIZE), b'')
    for r in records:
        ...



#5.9. Reading binary data into a mutable buffer

#to read data into a mutable array, use the readinto() methods of files
import os.path

def read_into_buffer(filename):
    buf = bytearray(os.path.getsize(filename))
    with open(filename,'rb') as f:
        f.readinto(buf)
    return buf

#Write to a sample file
with open('sample.bin', 'wb') as f:
    f.write(b'Hello World')  #gives 11
buf = read_into_buffer('sample.bin')
buf #gives bytearray(b'Hello World')
buf[0:5] = b'Hallo'
buf #gives bytearray(b'Hallo World')
with open('newsample.bin', 'wb') as f:
    f.write(buf)  #写了一个新的binary文，件

#Reading a binary file consisting of equally sized records
record_size = 32 #size of each record
buf = bytearray(record_size)  #set up a buffer with record_size length
with open ('somefile', 'rb') as f:
    while True:
        n = f.readinto(buf) # n is the length of how long the content of f being written into buf
        if n < record_size: #ehich means that all content of f has been written into buf
            break
        #use the contents of buf, e.g. with open('newfile', 'wb') as g: g.write(buf)

#memoryview, which lets you make zero-copy slices of an existing buffer and even change its contents
buf = bytearray(b'Hello World')
m1 = memoryview(buf) # <memory at 0x05C1D100>
m2 = m1[-5:]
m2 #gives <memory at 0x05C1D1D0>
m2[:] = b'WORLD'
buf #gives bytearray(b'Hello WORLD')




#5.10. Memory mapping binary files
# memory map a binary file into a mutable byte array. Goal probably is to random access to its contents or to make in-place modifications
import os
import mmap
def memory_map(filename, access = mmap, ACCESS_WRITE):
    size = os.path.getsize(filename)
    fd = os.open(filename, os.O_RDWR)
    return mmap.mmap(fd, size, access = access)

#how to create a file and expand it to a desired size
size = 1000000
with open('data', 'wb') as f:
    f.seek(size-1)
    f.write(b'\x00')

#how to memory mapping the contents using the memory_map function
m = memory_map('data')
len(m) #gives 1000000
m[0:10] #gives
m[0] #gives 0
#reassign a slice
m[0:11] = b'Hello World'
m.close()
#verify that change was made
with open('data', 'rb') as f:
    print(f.read(11))  # gives b'Hello World'

#to use mmap object returned by memory_map() as a context manager
with memory_map('data') as m:
    print (len(m))
    print (m[0:10])   #gives 1000000  b'Hello World'
m.close() #gives True

#If read-only access is needed
m = memory_map('data', mmap.ACCESS_READ)
#If  modify the data locally with no changes written back to the original file
m = memory_map('data', mmap.ACCESS_COPY)
