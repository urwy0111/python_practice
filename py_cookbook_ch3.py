#ch3 Numbers, Dates and Times


#3.1. Rounding Numerical Values
#for simple rounding, use the built-in round(values, ndigits)
round(1.23, 1)
round(-1.27, 1)  #gives -1.3
round(1.5) #gives 2, default setting is round to int
#ndigits can be negative, rounding takes place for 10, 100, 1000 and so on
a = 1627731
round(a, -1) #gives 1627730
round(a, -2) #gives 1627700
round(a, -3) #gives 1628000

#round()  vs  format()
x = 1.23456
format(x, '0.2f')
'value is {:0.3f}'.format(x) #gives 'value is 1.235'



#3.2. Performing accurate decimal calculations
#accurate calculations with decimal numbers, no small errors that naturally occur with floats
a = 4.2
b = 2.1
(a + b) == 6.3 #gives False

#to avoid this and give up some performance, use the decimal module
from decimal import decimal
a = Decimal('4.2')
b = Decimal('2.1')
a + b #gives Decimal('6.3')
print(a + b) #gives 6.3
(a + b) == Decimal('6.3') # gives True

#control number of digits and Rounding
from decimal import localcontext
a = Decimal('1.3')
b = Decimal('1.7')
print(a / b) #gives 0.7647058823529412225698141713
with localcontext() as ctx:
    ctx.prec = 3
    print (a / b)  # gives 0.765
with localcontext() as ctx:
    ctx.prec = 50
    print(a / b)  #gives 0.76470588235294122256981417128677796924031130635376  虽然有50位，但是已经是不准确的了

nums = [1.23e+18, 1, 1.23e-18]
sum(nums) #gives 0.0
import math
math.fsum(nums) #gives 1.0



#3.3. Formatting numbers for output
#format a single output, use built-in format() function
x = 1234.56789
format(x, '0.2f') #gives '1234.57'
format(x, '>10.1f') #gives '    1234.6'
format(x, '0,.1f') #gives '1,234.6'
format(x, 'e') #gives '1.234568e+03'
format(x, '0.2E') #gives '1.23E+03'
'The value is {:0,.2f}'.format(x) #gives 'The value is 1,234.57'

swap_separators = { ord('.'):',', ord(','):'.' }
format(x, ',').translate(swap_separators) # gives '1.234,56789'

# use the % operator to format Numbers
'%0.2f' % x    '1234.57'
'%10.1f' % x    '    1234.6'
'%-10.1f' % x    '1234.6    '




#3.4. Working with binary, octal and hexdecimal integers
x = 1234
# use these functions, the result will have 0b. 0o, 0x in the front
bin(x)
oct(x)
hex(x)
#use format() function, no these indicators in the front
format(x, 'b')
format(x, 'o')
format(x, 'h')

#convert integer strings in different bases, use int() function with an appropriate base.
int('4d2', 16) #gives 1234
int('10011010010', 2) #gives 1234

#Specify octal values using '0o' in front of the Numbers
import os
os.chmod('script.py', 0o755)


#3.5. Packing and unpacking large integers from bytes
# byte string <>integer value
data = b'\x00\x124V\x00x\x90\xab\x00\xcd\xef\x01\x00#\x004'
len(data)
int.from_bytes(data, 'little') #gives 69120565665751139577663547927094891008
int.from_bytes(data, 'big') #gives 94522842520747284487117727783387188





#3.15. Converting strings to Date

from datetime import datetime
text = '2012 - 09 - 20'
y = datetime.strptime(text, 'Y% - m% - d%')
z = datetime.now()
diff = z - y
diff #gives datetime.timedelta(1999, 42597, 426011) 从y那一天的0点开始算起
z # gives datetime.datetime(2018, 3, 12, 12, 3, 47, 801239)
nice_z = datetime.strftime(z, '%A %B %d, %Y')
nice_z #gives 'Monday March 12, 2018'

# strptime() 非常慢
from datetime import datetime
def parse_ymd(s):
    year_s, mon_s, day_s = s.split('-')
    return datetime(int(year_s), int(mon_s), int(day_s))
parse_ymd(text) # gives datetime.datetime(2018, 3, 12, 0, 0)




#3.16. Manipulating dates involving time zones
from datetime import datetime
from pytz import timezone
d = datetime(2012, 12, 21, 9, 30, 0)
pint (d)

#loclalize the date for Chicago
central = timezone('US/Central')
loc_d = central.localize(d)
print (loc_d)
#convert to Bangalore time
bang_d = loc_d.astimezone(timezone('Asia/Kolkata'))
print (bang_d)

#Considering daylight saving transition and other details
d = datetime(2013,3,10,1,45)
loc_d = central.localize(d)
print (loc_d)
later = loc_d + timedelta(minutes = 30) # gives 2013-03-10 02:15:00-06:00
later = central.normalize(loc_d + timedelta(minutes = 30)) #gives 2013-03-10 03:15:00-05:00

#Convert all times to UTC time
utc_d = loc_d.astimezone(pytz.utc)
print (utc_d) # gives 2013-03-10 07:45:00+00:00

#In UTC, no need to consider daylight saving and other matters
later_utc = utc_d + timedelta(minutes = 30)
print(later_utc.astimezone(central)) #gives 2013-03-10 03:15:00-05:00
