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
    spceialSkills: dict
    upgradedStats: dict

    def __dict__(self):
        aux = OrderedDict()
        aux['id']= self.charaId
        aux['charaName']= self.charaName
        aux['unitName']= self.unitName
        aux['rarity']= self.rarity
        aux['weapon']= self.weapon
        aux['element']= self.element
        aux['hp']= self.hp
        aux['mp']= self.mp
        aux['atk']= self.atk
        aux['def']= self.deff
        aux['crit']= self.crit
        aux['swordSkills']= self.swordSkills
        aux['battleSkills']= self.battleSkills
        aux['spceialSkills']= self.spceialSkills
        aux['upgradedStats']=self.upgradedStats
        return dict(aux)
