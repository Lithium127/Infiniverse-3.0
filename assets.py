from __future__ import annotations

from random import randint, choice

import re

def randiter(range_: list) -> int:
    value = randint(range_[0],range_[1])
    return range(value)

def randrange(range_: list) -> int:
    value = randint(range_[0],range_[1])
    return value

def randpercent(value: int) -> bool:
    return randint(0,100) < value


class StaticObject(object):
    
    _contents: list[StaticObject]
    _parent: StaticObject
    
    _is_generated: bool
    
    _name: str
    
    def __init__(self, preset_name: str|None = None) -> None:
        
        self._is_generated = False
        self._contents = []
        self._parent = None
        
        if preset_name is None:
            self._name = self._generate_name()
        else:
            self._name = preset_name
    
    def generate(self) -> None:
        if not self._is_generated:
            self._generate()
            self._is_generated = True
    
    def add_content(self, content: StaticObject) -> None:
        content._parent = self # simplify parent reference
        self._contents.append(content)
    
    
    # Abstract Methods
    def _generate(self) -> None:
        pass
    
    def _generate_name(self) -> str | None:
        return None
    
    def _dynamic_display(self) -> dict[str, str] | None:
        return None

    
    # Properties
    @property
    def _content_tuple(self):
        
        if not self._is_generated:
            return [("Object not yet generated", self)]
        
        data = []
        for child in self._contents:
            data.append((f"[{child.class_prefix}] {'+' if child._is_generated else '-'} {child.name}", child))
        return data
    
    @property
    def name(self) -> str:
        return self._name or self.__class__.__name__
    
    @name.setter
    def name(self, value: str) -> None:
        self._name = value
    
    @property
    def class_prefix(self) -> str:
        return re.sub(rf'[AEIOUaeiou]', "", self.__class__.__name__)[:3]



class Universe(StaticObject):
    GALAXY_RANGE = [5,9]
    
    NAME_PREFIXS = ["Bacon"]
    
    D_SPACE_TYPES = ["Euclidian", "Mixed", "Hyperbolic", "Spherical", "Cubic", "Empty"]
    D_AGE_RANGE = [10,999999]
    
    def _generate(self) -> None:
        for i in randiter(self.GALAXY_RANGE):
            self.add_content(Galaxy())
    
    def _generate_name(self) -> str | None:
        return f"{choice(self.NAME_PREFIXS)}verse"
    
    def _dynamic_display(self) -> dict[str, str] | None:
        return {
            "Space": choice(self.D_SPACE_TYPES),
            "Est Age": f"10^{randrange(self.D_AGE_RANGE)} M"
        }



class Galaxy(StaticObject):
    SYSTEM_RANGE = [7,25]
    
    GIVEN_NAME_PERCENT = 15
    
    NAME_PREFIXS = ["X","JW","HB","A","B"]
    NAME_NUMBER_RANGE = [1,999]
    
    GIVEN_NAME_PREFIXES = [
        "Andromeda",
        "Sombrero",
        "Samsung",
        "Disk",
        "Crab",
        "Predator"
    ]
    
    def _generate(self) -> None:
        for _ in randiter(self.SYSTEM_RANGE):
            self.add_content(StarSystem())
    
    def _generate_name(self) -> str | None:
        if randpercent(self.GIVEN_NAME_PERCENT):
            return f"{choice(self.GIVEN_NAME_PREFIXES)} Galaxy"
        return f"{choice(self.NAME_PREFIXS)}-{randrange(self.NAME_NUMBER_RANGE)}"

class BlackHole(StaticObject):
    pass

class StarSystem(StaticObject):
    
    def _generate(self) -> None:
        pass



START_OBJECT = Universe("Universe")