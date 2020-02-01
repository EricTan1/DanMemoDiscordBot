import mysql.connector

class DBcontroller:

  def __init(self, host, user, password, port, database):
    self.connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="danmemo", port="3306", database="danmemo")
    print(self.connection)

    mycursor = self.connection.cursor()

    mycursor.execute("SHOW TABLES")
    for x in mycursor:
      print(x)

    self.connection.close()

  # adventurer table
  def getAdventurerByID(self, adventurerid):
    pass

  def getAdventurerByColumn(self, column_name, value):
    pass

  def insertAdventurer(self, characterid, typeid, limited, ascended, stars, splashuri, iconuri):
    pass
  # adventurer development table
  def getAdventurerDevelopmentByID(self, adventurerdevelopmentid):
    pass

  def getAdventurerDevelopmentByColumn(self, column_name, value):
    pass

  def insertAdventurerDevelopment(self, adventurerid, name, attributeid, modifierid):
    pass

  # adventurer skill table
  def getAdventurerSkillByID(self, adventurerskillid):
    pass

  def getAdventurerSkillByColumn(self, column_name, value):
    pass

  def insertAdventurerSkill(self, adventurerid, typeid, eleid, skillname):
    pass

  # adventurer skill effects table
  def getAdventurerSkillEffectsByID(self, adventurerskilleffectsid):
    pass

  def getAdventurerSkillEffectsByColumn(self, column_name, value):
    pass

  def insertAdventurerSkillEffects(self, adventurerskillid, targetid, attributeid, modifierid, duration):
    pass
  # assist table
  def getAssistByID(self, assistid):
    pass
  
  def getAssistByColumn(self, column_name, value):
    pass

  def insertAssist(self, characterid, typeid, limited, stars, splashuri, iconuri):
    pass

  # assist skill table
  def getAssistSkillByID(self, assistskillid):
    pass

  def getAssistSkillByColumn(self, column_name, value):
    pass

  def insertAssistSkill(self, assistid, skillname):
    pass

  # assist skill effects table
  def getAssistSkillEffectsByID(self, assistskilleffectsid):
    pass

  def getAssistSkillEffectsByColumn(self, column_name, value):
    pass

  def insertAssistSkillEffects(self, assistskillid, targetid, attributeid, modifierid):
    pass

  # character
  def getCharacterByID(self, characterid):
    pass

  def getCharacterByColumn(self, column_name, value):
    pass

  def insertCharacter(self, name, iscollab):
    pass

  # basically constant tables
  # element
  def getElementByID(self, elementid):
    pass

  def getElementByColumn(self, column_name, value):
    pass

  def insertElement(self, name):
    pass
  # modifier
  def getModifierByID(self, modifierid):
    pass

  def getModifierByColumn(self, column_name, value):
    pass

  def insertModifier(self, value):
    pass
  # target
  def getTargetByID(self, targetid):
    pass

  def getTargetByColumn(self, column_name, value):
    pass

  def insertTarget(self, name):
    pass
  
  # type
  def getTypeByID(self, typeid):
    pass

  def getTypeByColumn(self, column_name, value):
    pass

  def insertType(self, name):
    pass
