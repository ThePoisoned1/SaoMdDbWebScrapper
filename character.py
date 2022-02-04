from dataclasses import dataclass
import json
from typing import OrderedDict


@dataclass
class Character:
    charaId: int
    charaName: str
    unitName: str
    rarity: int
    weapon: str
    element: str
    hp: int
    mp: int
    atk: int
    deff: int
    crit: int
    swordSkills: dict
    battleSkills: dict
    specialSkills: dict
    upgradedStats: dict

    def __dict__(self):
        aux = OrderedDict()
        aux['id'] = self.charaId
        aux['charaName'] = self.charaName
        aux['unitName'] = self.unitName
        aux['rarity'] = self.rarity
        aux['weapon'] = self.weapon
        aux['element'] = self.element
        aux['hp'] = self.hp
        aux['mp'] = self.mp
        aux['atk'] = self.atk
        aux['def'] = self.deff
        aux['crit'] = self.crit
        aux['swordSkills'] = self.swordSkills
        aux['battleSkills'] = self.battleSkills
        aux['specialSkills'] = self.specialSkills
        aux['upgradedStats'] = self.upgradedStats
        return dict(aux)

    @staticmethod
    def get_CSV_headers():
        return['id', 'charaName', 'unitName', 'rarity', 'weapon', 'element', 'hp', 'mp', 'atk', 'def', 'crit', 'swordSkills', 'battleSkills', 'specialSkills', 'upgradedStats']

    def to_CSV_line(self):
        data = []
        data.append(self.charaId)
        data.append(self.charaName)
        data.append(self.unitName)
        data.append(self.rarity)
        data.append(self.weapon)
        data.append(self.element)
        data.append(self.hp)
        data.append(self.mp)
        data.append(self.atk)
        data.append(self.deff)
        data.append(self.crit)
        data.append('|'.join([f'{key}: {val}' for key,
                    val in self.swordSkills.items()]) if self.swordSkills else '')
        data.append('|'.join([f'{key}: {val}' for key,
                    val in self.battleSkills.items()]) if self.battleSkills else '')
        data.append('|'.join(self.specialSkills) if self.specialSkills else '')
        data.append('|'.join([f'{key}: {val}' for key,
                    val in self.upgradedStats.items()]) if self.upgradedStats else '')
        return data
