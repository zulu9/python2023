x = "Kisa ist die beste Katze!"
print(len(x))
print(x[5:9])
print(x[9:12])
print(x[-1])
print(x[-8:3])
print(x[:-4])
print(x[-1:-4])
print(x[-18:])

print(
    x.lower(),
    x.upper(),
    x.strip(),
    x.replace('a', "A"),
    x.split('ist'),
    x.replace(" ", ""),
    "    Ein     String   ".strip(),
    x.lower().replace('a', '?!')
)
