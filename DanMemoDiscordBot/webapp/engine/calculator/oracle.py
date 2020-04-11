from .helper import *
from .calculator import *
from .mcts import *

from copy import deepcopy
from enum import Enum

class AttackTarget(Enum):
  ST = 0
  AOE = 1

class SkillBoost(Enum):
  LOW = 0
  MID = 1
  HIGH = 2
  SUPER = 3
  ULTRA = 4

class SkillTarget(Enum):
  SELF = 0
  ALLIES = 1
  FOE = 2
  FOES = 3


class Unit(Helper):
  def __init__(self, name, hp, mp, physical, magic, defense, skills=[], modifiers={}, damage_received=0):
    pass

class Adventurer(Unit):
    def __init__(self, name, hp, mp, physical, magic, defense, skills=[], modifiers={}, damage_received=0):
        pass
    def __hash__(self):
        return hashAll(self.name, self.hp, self.mp, self.physical, self.magic, self.defense, self.skills, self.modifiers, self.damage_received)

class Opponent(Unit):
    def __init__(self, name, hp, mp, physical, magic, defense, skills=[], modifiers={}, damage_received=0):
        pass
    def getPossibleActions(self):
        possibleActions = []
        return possibleActions
    def __hash__(self):
        return hashAll(self.name, self.hp, self.mp, self.physical, self.magic, self.defense, self.skills, self.modifiers, self.damage_received)

class Attack(Helper):
    def __init__(self, target, power, element):
        pass

class SubSkill(Helper):
    def __init__(self, target, attribute, modifier, turns):
        pass

class Skill():
    def __init__(self, name, subSkills, attack):
        self.name = name
        self.subSkills = subSkills
        self.attack = attack

class Skills():
    def __init__(self, skills):
        self.skills = skills
        self.nameToId = {}
        for i in range(len(skills)):
            self.nameToId[skills[i].name] = i
    def getSkillFromId(self,skillId):
        return self.skills[skillId]
    def getSkillIdFromName(self,skillName):
        return self.nameToId[skillName]
    def getSkillFromName(self,skillName):
        return self.getSkillFromId(self.getSkillIdFromName(skillName))
    def apply(self,skillId,attacker,targets):
        pass

attacks = [Attack(AttackTarget.AOE, SkillBoost.LOW, None),
               Attack(AttackTarget.AOE, SkillBoost.MID, None),
               Attack(AttackTarget.ST, SkillBoost.HIGH, None),
               Attack(AttackTarget.ST, SkillBoost.SUPER, None),
               Attack(AttackTarget.ST, SkillBoost.ULTRA, None)]

subSkills = [SubSkill(SkillTarget.ALLIES, "Strength", 0.5, 10),
             SubSkill(SkillTarget.ALLIES, "Dexterity", 0.3, 10)]

skillsList = [Skill("Skill 0", [subSkills[0]], attacks[0]),
              Skill("Skill 1", [], attacks[1]),
              Skill("Skill 2", [], attacks[2]),
              Skill("Skill 3", [], attacks[3]),
              Skill("Skill 4", [], attacks[4])]

skills = Skills(skillsList)

def ifKeyElse(d,key,valueAbsent):
    if key in d:
        return d[key]
    else:
        return valueAbsent

def computeSkillBoost(attack):
    if attack.target == AttackTarget.ST:
        if attack.power == SkillBoost.LOW: return 0.5
        if attack.power == SkillBoost.MID: return 0.7
        if attack.power == SkillBoost.HIGH: return 0.9
        if attack.power == SkillBoost.SUPER: return 1.1
        if attack.power == SkillBoost.ULTRA: return 3.0
    if attack.target == AttackTarget.AOE:
        if attack.power == SkillBoost.LOW: return 0.1
        if attack.power == SkillBoost.MID: return 0.15
        if attack.power == SkillBoost.HIGH: return 0.2
        if attack.power == SkillBoost.SUPER: return 0.4
        if attack.power == SkillBoost.ULTRA: return 2.6
    raise Exception("Unknown attack target:", attack)

class BattleState():
    def __init__(self, adventurers=[], opponents=[]):
        self.adventurers = adventurers
        self.opponents = opponents
        self.damageDone = 0
        self.currentPlayer = 1
        self.currentTurn = 1

    def getCurrentPlayer(self):
        return self.currentPlayer

    def getPossibleActions(self):
        possibleActions = []
        if self.getCurrentPlayer() == 1:
            for skillId in self.adventurers[0].skills:
                possibleActions.append(Action(player=self.currentPlayer, skill=skillId))
        else:
            possibleActions.append(Action(player=self.currentPlayer, skill=None))
        return possibleActions

    def takeAction(self, action):
        newState = deepcopy(self)
        if newState.currentPlayer == 1:
            adventurer = newState.adventurers[0]
            opponent = newState.opponents[0]
            skill = skills.getSkillFromId(action.skill)

            #compute damage
            attack_base = adventurer.physical
            attack_boost = ifKeyElse(adventurer.modifiers,"Strength",0)
            temp_boost = 0
            foe_type_boost = 0
            sa_combo = 1

            defense_base = opponent.defense
            endurance_boost = 0
            def_boost = 0
            elemental_resistance = 0
            target_area_boost = 0

            familia_boost = 0
            elemental_boost = 0
            skill_boost = computeSkillBoost(skill.attack)
            skill_damage_boost = 0
            mode = CombatMode.PvE

            crit_boost = 0
            pen_boost = 0

            unitModifiers = UnitModifiers(attack_base, attack_boost, temp_boost, foe_type_boost, sa_combo)
            foeModifiers = FoeModifiers(defense_base, endurance_boost, def_boost, elemental_resistance, target_area_boost)
            combatModifiers = CombatModifiers(familia_boost, elemental_boost, skill_boost, skill_damage_boost, mode)
            otherModifiers = OtherModifiers(crit_boost, pen_boost)
            modifiers = Modifiers(unitModifiers, foeModifiers, combatModifiers, otherModifiers)

            damageResult = calculateDamage(modifiers)

            newState.damageDone += damageResult.average_damage
            opponent.hp -= damageResult.average_damage

            #apply modifiers
            for subSkill in skill.subSkills:
                if subSkill.target in [SkillTarget.SELF,SkillTarget.ALLIES]:
                    adventurer.modifiers[subSkill.attribute] = subSkill.modifier
                elif subSkill.target in [SkillTarget.FOE,SkillTarget.FOES]:
                    opponent.modifiers[subSkill.attribute] = subSkill.modifier

            newState.currentTurn = newState.currentTurn + 1
        newState.currentPlayer = newState.currentPlayer * -1
        return newState

    def isTerminal(self):
        return self.currentTurn > 7

    def getReward(self):
        return self.damageDone / 10_000_000

    def hash(self):
        return hashAll(self.adventurers, self.opponents, self.damageDone, self.currentPlayer, self.currentTurn)


class Action():
    def __init__(self, player, skill):
        self.player = player
        self.skill = skill

    def __str__(self):
        return str(self.skill)

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.player == other.player and self.skill == other.skill

    def __hash__(self):
        return hash((self.player, self.skill))



def main():
    adventurers = [Adventurer("[Sword Unleashed] Bell Cranel", 7681, 585, 2880, 921, 1103, skills=[0, 1, 2, 3, 4])]
    opponents = [Opponent("Revis", 100_000_000, 1, 1, 0, 0)]

    initialState = BattleState(adventurers, opponents)
    mcts = MCTS(iterationLimit=30_000_000,explorationConstant=0.001)
    action = mcts.search(initialState=initialState)

    print("Number of iterations done: ", mcts.numberOfIterations)
    mcts.printBestChain()
    mcts.printBestChainAndBrothers(skills.skills)
    print("Program terminated")




if __name__ == '__main__':
    main()