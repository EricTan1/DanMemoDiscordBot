import mysql.connector

class DBcontroller:

  def __init(self, host, user, password, port, database):
    self._connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="danmemo", port="3306", database="danmemo")
    #print(self.connection)
    self._mycursor = self.connection.cursor()
    self._mycursor.execute("SHOW TABLES")
    # for x in mycursor:
    # print(x)

  def closeconnection(self):
    ''' (DBcontroller) -> None
    Closes the DB connection
    '''
    self._connection.close()

  def insertData(self, entity):
    ''' (DBcontroller, Entity) -> bool
    returns whether or not it is a successful insert
    '''
    pass
  
  def updateData(self, entity, columns, values):
    ''' (DBcontroller, Entity, str, ?) -> bool
    returns whether or not it is a successful update
    '''
    pass  

  def getDataColumn(self, entityname, column, value):
    ''' (DBcontroller, Entity, str, ?) -> List of Entity
    returns the entity list based on the columns
    '''
    pass
