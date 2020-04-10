from database.entities.BaseConstants import Base

class Character(Base):
    ''' This class is an object that represents the
    Character table in the DB
    '''
    def __init__(self, characterid, name:str, iscollab:bool):
        ''' (self, str, bool) -> Character
        name : the name of the character (usually found in the characterlist
                                          section)
        isCollab : is the character originally from danmachi universe?
        '''
        self.name = str(name)
        self.characterid= characterid
        self.iscollab = bool(iscollab)

    def __str__(self):
        return self.name