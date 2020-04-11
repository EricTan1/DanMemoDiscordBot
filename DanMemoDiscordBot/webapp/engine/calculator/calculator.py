from enum import Enum
from math import *
import time
from .helper import *

class CombatMode(Enum):
  PvE = 0
  PvP = 1

class DamagePercentRNG(Enum):
  MINUS_FOUR = -4
  MINUS_THREE = -3
  MINUS_TWO = -2
  MINUS_ONE = -1
  ZERO = 0
  PLUS_ONE = 1
  PLUS_TWO = 2
  PLUS_THREE = 3
  PLUS_FOUR = 4

class ResultTypeRNG(Enum):
  BASE = 0
  GUARD = 1
  PENETRATION = 2
  CRITICAL_BASE = 3
  CRITICAL_GUARD = 4
  CRITICAL_PENETRATION = 5

class Modifiers(Helper):
  def __init__(self, unitModifiers, foeModifiers, combatModifiers, otherModifiers):
    pass

class UnitModifiers(Helper):
  def __init__(self, attack_base, attack_boost, temp_boost, foe_type_boost, sa_combo):
    pass

class FoeModifiers(Helper):
  def __init__(self, defense_base, endurance_boost, def_boost, elemental_resistance, target_area_boost):
    pass

class CombatModifiers(Helper):
  def __init__(self, familia_boost, elemental_boost, skill_boost, skill_damage_boost, mode):
    pass

class OtherModifiers(Helper):
  def __init__(self, crit_boost, pen_boost):
    pass

class DamageResult(metaclass=AutoInit):
  def __init__(self, trueAttack, trueDefense, trueBonus, modifiers, damages, damage_base, damage_critical, damage_penetration, damage_critical_penetration, average_damage, max_damage, min_damage, penetration_modifier):
    pass
  def printDamages(damages):
    print("",end="\t\t")
    for i in damages[DamagePercentRNG.ZERO]:
      print(i.name,end="\t")
    print("")

    for j in damages:
      sep1 = "\t" if j.name != "ZERO" else "\t\t"
      print(j.name,end=sep1)

      for i in damages[j]:
        sep2 = "\t" * (len(i.name)//4)
        print(damages[j][i],end=sep2)
      print("")
  def __repr__(self):
    d = self.__dict__.copy()
    del d["damages"]
    #pp.pprint(d)
    #DamageResult.printDamages(self.damages)
    return ""
  def filter(self,resultType):
    filtered = []
    for percent in self.damages:
      filtered.append(self.damages[percent][resultType])
    return filtered

class Experiment(Helper):
  def __init__(self, modifiers, resultType, damages):
    pass

'''
  Unit modifiers => True Attack
    attack_base = Physical/Magic stat
    attack_boost = Sum of Assist Str/Mag boost and Adventurer Str/Mag boost
    temp_boost = Value related to a skill with the mention of a "temp Str/Mag Boost"
    foe_type_boost = Related to the status "Ability Pt. +X% towards Y" of some adventurers
    sa_combo = Combo Number for SA chain, 1 for normal case
  Foe modifiers => True Def
    defense_base = Defense stat of foes in PvE / adventurers in WG
    endurance_boost = Sum of Assists and Adventurers End buff/debuff
    def_boost = Sum of Assist and Adventurer Mag/phys res buff/debuff
    elemental_resistance = Sum of Assist and Adventurer elemental res buff/debuff
    target_area_boost = Sum of Assist and Adventurer ST/AoE damage buff/debuff
  Combat modifiers => True Bonus
    familia_boost = Familia skill bonus during Familia events
    elemental_boost = Sum of Assist and Adventurer elemental damage buff/debuff
    skill_boost = Value related to each skill. Phys normal attacks and counters have a 0% mod. Mag normal attacks and counters are light element and have a -25% mod.
    skill_damage_boost = Value related to specific skills that have the "Dmg +X% per 1 Y Buff skill". Put here the total of this bonus
    mode = PvP is in War Game or Familia War Game, PvE is everything else including Familia Rush or Record Buster
  Other modifiers
    crit_boost = For Adventurers with the status "Critical Damage +X%"
    pen_boost = For Adventurers with the status "Damage +X% upon Penetration"
'''
def calculateDamage(modifiers):
  trueAttack = modifiers.unitModifiers.attack_base
  trueAttack = floor(trueAttack*(1 + modifiers.unitModifiers.attack_boost/100))
  trueAttack = floor(trueAttack*(1 + modifiers.unitModifiers.temp_boost/100))
  trueAttack = floor(trueAttack*(1 + modifiers.unitModifiers.foe_type_boost/100))
  trueAttack *= 2

  trueDefense = modifiers.foeModifiers.defense_base
  trueDefense *= 1 + modifiers.foeModifiers.endurance_boost/100

  trueBonus = 1 - (modifiers.foeModifiers.def_boost + modifiers.foeModifiers.elemental_resistance)/100
  trueBonus *= 1 + modifiers.foeModifiers.target_area_boost/100
  trueBonus *= 1 + (modifiers.combatModifiers.familia_boost + modifiers.combatModifiers.elemental_boost)/100
  trueBonus *= 1 + modifiers.combatModifiers.skill_boost/100
  trueBonus *= 1 + modifiers.combatModifiers.skill_damage_boost/100
  if modifiers.combatModifiers.mode == CombatMode.PvP:
    trueBonus *= 0.2
  trueBonus *= 0.8 + 0.2*modifiers.unitModifiers.sa_combo

  damage_base = (trueAttack - floor(trueDefense)) * trueBonus
  damage_critical = damage_base * 1.5 * (1 + modifiers.otherModifiers.crit_boost/100)
  damage_penetration = (trueAttack - floor(trueDefense/2)) * trueBonus * (1 + modifiers.otherModifiers.pen_boost/100)
  damage_critical_penetration = (trueAttack - floor(trueDefense/2)) * trueBonus * 1.5 * (1 + (modifiers.otherModifiers.crit_boost+modifiers.otherModifiers.pen_boost)/100)

  damages = {}
  average_damage = 0
  for percent in DamagePercentRNG:
    damages[percent] = {}
    for res in ResultTypeRNG:
      d = (1 + percent.value/100)
      if res == ResultTypeRNG.BASE:
        d *= damage_base
      elif res == ResultTypeRNG.GUARD:
        d *= damage_base / 2
      elif res == ResultTypeRNG.PENETRATION:
        d *= damage_penetration
      elif res == ResultTypeRNG.CRITICAL_BASE:
        d *= damage_critical
      elif res == ResultTypeRNG.CRITICAL_GUARD:
        d *= damage_critical / 2
      elif res == ResultTypeRNG.CRITICAL_PENETRATION:
        d *= damage_critical_penetration
      d = ceil(d) - 1
      damages[percent][res] = d
      average_damage += d
  average_damage /= len(DamagePercentRNG) * len(ResultTypeRNG)
  max_damage = damages[DamagePercentRNG.PLUS_FOUR][ResultTypeRNG.CRITICAL_PENETRATION]
  min_damage = damages[DamagePercentRNG.MINUS_FOUR][ResultTypeRNG.GUARD]
  penetration_modifier = damage_penetration / damage_base - 1

  #print(trueAttack,trueDefense,trueBonus)
  damageResult = DamageResult(modifiers,trueAttack,trueDefense,trueBonus,damages,damage_base,damage_critical,damage_penetration,damage_critical_penetration,average_damage,max_damage,min_damage,penetration_modifier)
  #print(damageResult)

  return damageResult

def findFoeDefense(experiments):
  expected_range = 1500
  possible_defenses = set(range(expected_range))
  impossible_defenses = set()
  for experiment in experiments:
    for defense in possible_defenses:
      if defense not in impossible_defenses:
        experiment.modifiers.foeModifiers.defense_base = defense
        damageResult = calculateDamage(experiment.modifiers)
        predictedDamages = damageResult.filter(experiment.resultType)
        for damage in experiment.damages:
          if damage not in predictedDamages:
            impossible_defenses.add(defense)
            continue
  possible_defenses -= impossible_defenses
  print(possible_defenses)
  return possible_defenses


def main():
  unitModifiers = UnitModifiers(2432,0,0,0,1)
  foeModifiers = FoeModifiers(279,0,0,60,0)
  combatModifiers = CombatModifiers(0,0,10,0,CombatMode.PvE)
  otherModifiers = OtherModifiers(0,0)

  '''unitModifiers = UnitModifiers(2818,1,3,5,3)
  foeModifiers = FoeModifiers(-1,7,-11,13,17)
  combatModifiers = CombatModifiers(19,31,23,29,CombatMode.PvE)
  otherModifiers = OtherModifiers(37,41)'''

  modifiers = Modifiers(unitModifiers,foeModifiers,combatModifiers,otherModifiers)
  #calculateDamage(modifiers)
  
  experiments = []
  experiments.append(Experiment(modifiers,ResultTypeRNG.BASE,[1936,1956,1997,2037,2057,2077,2098]))
  experiments.append(Experiment(modifiers,ResultTypeRNG.CRITICAL_BASE,[2905,2935,2965,2995,3026,3056,3086,3116,3147]))
  experiments.append(Experiment(modifiers,ResultTypeRNG.GUARD,[988,1038]))
  experiments.append(Experiment(modifiers,ResultTypeRNG.PENETRATION,[2037,2079,2099,2141,2162]))
  experiments.append(Experiment(modifiers,ResultTypeRNG.CRITICAL_PENETRATION,[3024,3056,3118,3149,3180,3212,3243]))

  findFoeDefense(experiments)


if __name__ == '__main__':
  start = time.clock()
  main()
  end = time.clock()
  print("Total execution time: ",end - start)