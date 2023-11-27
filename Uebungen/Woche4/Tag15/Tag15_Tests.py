# Tag 15 Tests
from dataclasses import *


@dataclass
class Teilnehmer:
    age: int
    name: str = "muh"

    def print_attributes(self):
        print(f'{self.name} is {self.age} years old')


bsp_teilnehmer = Teilnehmer(2, 'Kisa')
print(bsp_teilnehmer)
bsp_teilnehmer.print_attributes()

bsp_teilnehmer2 = astuple(Teilnehmer(4, 'Mahoney'))
print(bsp_teilnehmer2)
bsp_teilnehmer2.print_attributes()
