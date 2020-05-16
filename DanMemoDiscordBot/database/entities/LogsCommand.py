import database.DBcontroller

class LogsCommand:
    '''
    This class is an object that represents the LOGS_COMMAND table in the DB
    '''
    def __init__(self, discord_id, date, command, query, parameters):
        ''' (self, str, date, str, str, tuple) -> LogsCommand
        discord_id: the id of the user in discord
        '''
        self.discord_id = discord_id
        self.date = date
        self.command = command
        self.query = query
        self.parameters = parameters

    def __str__(self):
        return str(self.__dict__)
