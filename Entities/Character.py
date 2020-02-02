class Character:
    ''' This class is an object that represents the
    Character table in the DB
    '''
    def __init__(self, name, isCollab):
        ''' (self, str, bool) -> Character
        name : the name of the character (usually found in the characterlist
                                          section)
        isCollab : is the character originally from danmachi universe?
        '''
        self.name = name
        self.isCollab = isCollab

    def __str__(self):
        return self.name
