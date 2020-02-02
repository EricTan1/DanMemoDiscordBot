class Character:
    ''' This class is an object that represents the
    Character table in the DB
    '''
    def __init__(self, name, iscollab):
        ''' (self, str, bool) -> Character
        name : the name of the character (usually found in the characterlist
                                          section)
        isCollab : is the character originally from danmachi universe?
        '''
        self.name = name
        self.iscollab = iscollab

    def __str__(self):
        return self.name
    
    
    
class Stats:
    ''' This class is an object that represents the
    stats table in the DB
    '''
    def __init__(self, statsid, adventurerassistid, attributeid, value):
        ''' (Stats, int, int, int, str) -> Stats
        value : python list but in str format of an attribute
        ex:
        attribute: Strength
        [1,2,3,4,5,6]
        [LB0,LB1,LB2,LB3,LB4,LB5]
        corresponds with limit break 0-5
        '''
        self.statsid = statsid
        self.adventurerassistid = adventurerassistid
        self.attributeid = attributeid
        self.value = value

    def __str__(self):
        return self.name    