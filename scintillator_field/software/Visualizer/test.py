import random

def bit8(var):
    bit8 = 0
    for i in range(0, 8):

        new = (var >> 2 * i)&3

        if  new == 2:

            bit8 += 2**i

        elif new != 1:

            return False
        
    return bit8 - 128

def generate_data():
    list = []
    for i in range(random.randint(5,10)):
        list.append([random.randint(-128,128), - random.randint(-128,128)])
    return list

#test 0
data = []
for k in range(random.randint(7,13)):
    data.append(generate_data())


