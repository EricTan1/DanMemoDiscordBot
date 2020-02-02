import mysql.connector
import inspect

class DBcontroller:

  def __init(self, host, user, password, port, database):
    self._connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="danmemo", port="3306", database="danmemo")
    #print(self.connection)
    self._mycursor = self._connection.cursor()

  def closeconnection(self):
    ''' (DBcontroller) -> None
    Closes the DB connection
    '''
    self._connection.close()

  def insertData(self, entity):
    ''' (DBcontroller, Entity) -> bool
    returns whether or not it is a successful insert
    '''
    # get all the attributes of the members and their corresponding values
    attributes =inspect.getmembers(entity, lambda a:not(inspect.isroutine(a)))
    attributes =[a for a in attributes if not(a[0].startswith('__') and a[0].endswith('__'))]
    
    attribute_list = []
    value_list = []
    valueprep_list=[]
    
    for attributetuple in attributes:
      (attributename, attributevalue) = attributetuple
      attribute_list.append(attributename)
      valueprep_list.append('%s')
      value_list.append(attributevalue)
    
    attribute_list= str(tuple(attribute_list)).replace("'","")
    valueprep_list= str(tuple(value_list)).replace("'","")
    
    
    sql="INSERT INTO {} {} VALUES {}".format(type(entity).__name__,
                                             attribute_list,valueprep_list)
    values = tuple(value_list)
    self._mycursor.execute(sql,values)
    self._connection.commit()
    print(self._mycursor.rowcount, "record inserted.")
    
    
  
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
