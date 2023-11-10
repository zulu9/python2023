myfile = open('./bsp.txt', 'r')
print(myfile.readlines())
myfile = open('./bsp.txt', 'r')
myfile.close()
myfile = open('./bsp.txt', 'r')
print(myfile.read(3))
print(myfile.read(5))
print(myfile.read())
myfile.close()

myinput = input("Input: >> ")
print(myinput+"5")

outputfile = open('./bsp2.txt', 'w')
outputfile.write("Hallo Erde!")

print('a','b','c')
