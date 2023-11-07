# Imports
import this
from numpy import array
myarray = array([1, 2, 3])
print(myarray, type(myarray))

import numpy as np
myarray = np.array([1, 2, 3])
print(myarray, type(myarray))

# Unicode
# Letters and Numbers (no Emojis!)
# This works but 🐈 can't be a variable name
print("Unicode")
챁챁 = ["🐈", "🐈🐈🐈", "🐈🐈🐈🐈🐈"]
for 챁 in 챁챁:
	print(챁)

# Bools
print("!= vs not")
x = 1
y = "string"

if x != y:
	print("!=")
	print(x, y)
if not x == y:
	print("not x == y")
	print(x, y)

# Modulo, div
print("Division, Div and Modulo of 7 and 2")
x = 7 / 2
y = 7 // 2
z = 7 % 2
print(x, y, z, sep=", ")
