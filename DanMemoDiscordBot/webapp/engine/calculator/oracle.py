from .helper import *
from .calculator import *
from .mcts import *

from copy import deepcopy
from enum import Enum


class AttackTarget(Enum):
    ST = 0
    AOE = 1


class SkillBoost(Enum):
    NONE = 0
    LOW = 1
    MID = 2
    HIGH = 3
    SUPER = 4
    ULTRA = 5


class SkillTarget(Enum):
    SELF = 0
    ALLIES = 1
    FOE = 2
    FOES = 3


class EffectOrigin(Enum):
    UNIT = 0
    ASSIST = 1


class EffectPurpose(Enum):
    BUFF = 0
    DEBUFF = 1


class Unit(Helper):
    def __init__(self, name, hp, mp, physical, magic, defense, skills, applied_effects, damage_received):
        pass

    def __hash__(self):
        return hashAll(self.name, self.hp, self.mp, self.physical, self.magic, self.defense, self.skills,
                       self.applied_effects, self.damage_received)

    def get_applied_effect(self, effect):
        for applied_effect in self.applied_effects:
            if applied_effect.origin == effect.origin and applied_effect.purpose == effect.purpose \
                    and applied_effect.attribute == effect.attribute:
                return applied_effect
        return None

    def apply_if_necessary(self, effect):
        applied_effect = self.get_applied_effect(effect)
        if applied_effect is None:
            applied_effect = AppliedEffect.create_applied_effect_from_effect(effect)
            self.applied_effects.append(applied_effect)
        else:
            # buff
            if effect.purpose == EffectPurpose.BUFF:
                if effect.modifier > applied_effect.modifier:
                    applied_effect.modifier = effect.modifier
                    applied_effect.turns = effect.turns
            # debuff
            elif effect.modifier < applied_effect.modifier:
                applied_effect.modifier = effect.modifier
                applied_effect.turns = effect.turns


class Adventurer(Unit):
    def __init__(self, name, hp, mp, physical, magic, defense, skills, applied_effects, damage_received):
        pass

class Opponent(Unit):
    def __init__(self, name, hp, mp, physical, magic, defense, skills, applied_effects, damage_received):
        pass

    @staticmethod
    def get_possible_actions():
        possible_actions = []
        return possible_actions


class Attack(Helper):
    def __init__(self, target, power, element):
        pass


class Effect(Helper):
    def __init__(self, origin, purpose, target, attribute, modifier, turns):
        pass


class AppliedEffect(Helper):
    def __init__(self, origin, purpose, attribute, modifier, turns):
        pass

    @staticmethod
    def create_applied_effect_from_effect(effect):
        return AppliedEffect(effect.origin, effect.purpose, effect.attribute, effect.modifier, effect.turns)


class Skill:
    def __init__(self, name, effects, attack):
        self.name = name
        self.effects = effects
        self.attack = attack


class Skills:
    def __init__(self, skills):
        self.skills = skills
        self.nameToId = {}
        for i in range(len(skills)):
            self.nameToId[skills[i].name] = i

    def get_skill_from_id(self, skill_id):
        return self.skills[skill_id]

    def get_skill_id_from_name(self, skill_name):
        return self.nameToId[skill_name]

    def get_skill_from_name(self, skill_name):
        return self.get_skill_from_id(self.get_skill_id_from_name(skill_name))

    def apply(self, skill_id, attacker, targets):
        pass


def if_key_else(d, key, value_absent):
    if key in d:
        return d[key]
    else:
        return value_absent


def compute_skill_boost(attack):
    if attack.target == AttackTarget.ST:
        if attack.power == SkillBoost.LOW: return 50
        if attack.power == SkillBoost.MID: return 70
        if attack.power == SkillBoost.HIGH: return 90
        if attack.power == SkillBoost.SUPER: return 110
        if attack.power == SkillBoost.ULTRA: return 300
    if attack.target == AttackTarget.AOE:
        if attack.power == SkillBoost.LOW: return 10
        if attack.power == SkillBoost.MID: return 15
        if attack.power == SkillBoost.HIGH: return 20
        if attack.power == SkillBoost.SUPER: return 40
        if attack.power == SkillBoost.ULTRA: return 260
    raise Exception("Unknown attack target:", attack)


attacks = [Attack(AttackTarget.AOE, SkillBoost.LOW, None),
           Attack(AttackTarget.AOE, SkillBoost.ULTRA, None),
           Attack(AttackTarget.ST, SkillBoost.HIGH, None),
           Attack(AttackTarget.ST, SkillBoost.SUPER, None),
           Attack(AttackTarget.ST, SkillBoost.ULTRA, None)]

effects = [Effect(EffectOrigin.UNIT, EffectPurpose.BUFF, SkillTarget.ALLIES, "Strength", 25, 10),
           Effect(EffectOrigin.UNIT, EffectPurpose.BUFF, SkillTarget.ALLIES, "Dexterity", 30, 10)]

skillsList = [Skill("Skill 0", [effects[0]], attacks[0]),
              Skill("Skill 1", [], attacks[1]),
              Skill("Skill 2", [], attacks[2]),
              Skill("Skill 3", [], attacks[3]),
              Skill("Skill 4", [], attacks[4])]

skills = Skills(skillsList)


class BattleState:
    def __init__(self, adventurers, opponents):
        self.adventurers = adventurers
        self.opponents = opponents
        self.damageDone = 0
        self.currentPlayer = 1
        self.currentTurn = 1

    def get_current_player(self):
        return self.currentPlayer

    def get_possible_actions(self):
        possible_actions = []
        if self.get_current_player() == 1:
            for skillId in self.adventurers[0].skills:
                possible_actions.append(Action(player=self.currentPlayer, skill=skillId))
        else:
            possible_actions.append(Action(player=self.currentPlayer, skill=None))
        return possible_actions

    def take_action(self, action):
        new_state = deepcopy(self)
        if new_state.currentPlayer == 1:
            adventurer = new_state.adventurers[0]
            opponent = new_state.opponents[0]
            skill = skills.get_skill_from_id(action.skill)

            # compute damage
            attack_base = adventurer.physical
            attack_boost = if_key_else(adventurer.applied_effects, "Strength", 0)
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
            skill_boost = compute_skill_boost(skill.attack)
            skill_damage_boost = 0
            mode = CombatMode.PvE

            crit_boost = 0
            pen_boost = 0

            unit_modifiers = UnitModifiers(attack_base, attack_boost, temp_boost, foe_type_boost, sa_combo)
            foe_modifiers = FoeModifiers(defense_base, endurance_boost, def_boost, elemental_resistance,
                                         target_area_boost)
            combat_modifiers = CombatModifiers(familia_boost, elemental_boost, skill_boost, skill_damage_boost, mode)
            other_modifiers = OtherModifiers(crit_boost, pen_boost)
            modifiers = Modifiers(unit_modifiers, foe_modifiers, combat_modifiers, other_modifiers)

            damage_result = calculateDamage(modifiers)

            new_state.damageDone += damage_result.average_damage
            opponent.hp -= damage_result.average_damage

            # apply modifiers
            for effect in skill.effects:
                if effect.target in [SkillTarget.SELF, SkillTarget.ALLIES]:
                    adventurer.apply_if_necessary(effect)
                elif effect.target in [SkillTarget.FOE, SkillTarget.FOES]:
                    opponent.apply_if_necessary(effect)

            new_state.currentTurn = new_state.currentTurn + 1
        new_state.currentPlayer = new_state.currentPlayer * -1
        return new_state

    def is_terminal(self):
        return self.currentTurn > 7

    def get_reward(self):
        return self.damageDone / 10_000_000

    def hash(self):
        return hashAll(self.adventurers, self.opponents, self.damageDone, self.currentPlayer, self.currentTurn)


class Action:
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
    adventurers = [Adventurer("[Sword Unleashed] Bell Cranel", 7681, 585, 2880, 921, 1103, [0, 1, 2, 3, 4], [], 0)]
    opponents = [Opponent("Revis", 100_000_000, 1, 1, 0, 0, [0, 1, 2, 3, 4], [], 0)]

    initial_state = BattleState(adventurers, opponents)

    mcts = MCTS_Best_Score(iteration_limit=10_000, exploration_constant=0.03)
    action = mcts.search(initial_state=initial_state)

    print("Number of iterations done: ", mcts.numberOfIterations)
    mcts.print_best_chain()
    mcts.print_best_chain_and_brothers(skills.skills)
    print("Program terminated")


if __name__ == '__main__':
    main()
