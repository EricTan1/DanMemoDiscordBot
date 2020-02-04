import mysql.connector
import inspect

class DBcontroller:

  def __init__(self, host, user, password, port, database):
    ''' (DBcontroller, str, str ,str, int ,str) -> DBcontroller
    '''
    self.database = database
    self._connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password, port=port, database=database)
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
    valueprep_list= str(tuple(valueprep_list)).replace("'","")
    
    
    sql="INSERT INTO {}.{} {} VALUES {}".format(self.database,str(type(entity).__name__).lower(),
                                             attribute_list.lower(),valueprep_list.lower())
    values = tuple(value_list)
    print(sql + "\n")
    print(str(values)+ "\n")
    self._mycursor.execute(sql,values)
    self._connection.commit()
    print(self._mycursor.rowcount, "record inserted.")
    
    
  
  def updateData(self, entity):
    ''' (DBcontroller, Entity, str, ?) -> bool
    returns whether or not it is a successful update
    '''
    pass  

  def getDataColumn(self, entityname, column, value):
    ''' (DBcontroller, Entity, str, ?) -> List of Entity
    returns the entity list based on the columns
    '''
    sql = 'SELECT * FROM {}.{} WHERE {}=%s'.format(self.database.lower(),
                                                   entityname.lower(),
                                                   column.lower())
    print(sql)
    
    self._mycursor.execute(sql,(value,))
    ret_list =[]
    for row in self._mycursor: 
      ret_list.append(row)
    print(ret_list)
    return ret_list
