'''
This stores all of the sharable game data between all the adventurers/assists
such as element, type etc.
'''
from abc import ABC

class Base(ABC):
    @classmethod
    def from_json(cls, data):
        return cls(**data)


class Element(Base):
    def __init__(self, elementid:int, name:str):
        ''' (Element, int, str) -> Element
        element : represents the elemental types in danmemo (ex: light,fire)
        '''
        self.elementid = int(elementid)
        self.name = str(name)
        
    def __str__(self):
        return self.name

class Type(Base):
    def __init__(self, typeid:int,name:str):
        ''' (Type, int, str) -> Type
        atktype : represents the type of attack (ex: physical, magical, mixed)
        '''
        self.typeid = int(typeid)
        self.name = str(name)

    def __str__(self):
        return self.name

class Attribute(Base):
    def __init__(self, attributeid:int, name:str):
        ''' (Attribute, int, str) -> Attribute
        name : attributes/stat time (ex: str/strength, agi/agility)
        '''
        self.attributeid= int(attributeid)
        self.name = str(name)

    def __str__(self):
        return self.name

class Target(Base):
    def __init__(self, targetid:int, name:str):
        ''' (Target, int, str) -> Target
        name : what it targets (ex: self, enemy, allies)
        '''
        self.name = str(name)
        self.targetid = int(targetid)
        
    def __str__(self):
        return self.name

class Modifier(Base):
    def __init__(self, modifierid:int,value):
        ''' (Modifier, int, str) -> Modifier
        value : the strength of an effect/skill (ex: Hi, Lo, 10, 15)
        Note: numbers are in percentages for example: 5 = 5%
        '''
        self.value = value
        self.modifierid = int(modifierid)

    def __str__(self):
        try:
            # check if it is a number
            temp_value = int(self.value)
            return self.value + "%"
        except:
            # its just a string b/c its uncastable
            return self.value

