'''
This stores all of the sharable game data between all the adventurers/assists
such as element, type etc.
'''


class Element:
    def __init__(self, element):
        ''' (Element, str) -> Element
        element : represents the elemental types in danmemo (ex: light,fire)
        '''
        self.element = element
        
    def __str__(self):
        return self.element

class Type:
    def __init__(self, atktype):
        ''' (Type, str) -> Type
        atktype : represents the type of attack (ex: physical, magical, mixed)
        '''
        self.atktype = atktype

    def __str__(self):
        return self.atktype

class Attribute:
    def __init__(self, name):
        ''' (Attribute, str) -> Attribute
        name : attributes/stat time (ex: str/strength, agi/agility)
        '''
        self.name = name

    def __str__(self):
        return self.name

class Target:
    def __init__(self, name):
        ''' (Target, str) -> Target
        name : what it targets (ex: self, enemy, allies)
        '''
        self.name = name
    def __str__(self):
        return self.name

class Modifier:
    def __init__(self, value):
        ''' (Modifier, str) -> Modifier
        value : the strength of an effect/skill (ex: Hi, Lo, 10, 15)
        Note: numbers are in percentages for example: 5 = 5%
        '''
        self.value = value

    def __str__(self):
        try:
            # check if it is a number
            temp_value = int(self.value)
            return self.value + "%"
        except:
            # its just a string b/c its uncastable
            return self.value
