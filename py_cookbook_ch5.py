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
