from dataclasses import dataclass, field


@dataclass(order=True)
class Teilnehmer:
    sort_index: str = field(init=False, repr=False)
    age: int
    name: str
    legal_drinking: bool = field(init=False)

    def __post_init__(self):
        self.legal_drinking = self.age >= 18
        self.sort_index = self.name

    def printAttributes(self):
        print(f'{self.name} is {self.age} years old')


bsp_teilnehmer = Teilnehmer(7, 'Shiva')
print(bsp_teilnehmer)
bsp_teilnehmer.printAttributes()



class TeilnehmerKlassisch:
    def __init__(self, age: int, name: str = 'muh'):
        self.name = name
        self.age = age

    def test(self):
        print(f'{self.name} is {self.age} years old')


bsp_teilnehmerKlassisch = TeilnehmerKlassisch(7, 'Shiva')

print(bsp_teilnehmer)
print(bsp_teilnehmerKlassisch)