

class Assist():
    def __init__(self, skills=[], name=""):
        ''' (self, list of skil effects, bool) -> Assist
        skills: non mlb skill effects or mlb skill effects
        '''
        self.skills = skills
        self.name=name