from .helper import *
import time
import math
import random


def random_policy(state):
    while not state.is_terminal():
        try:
            action = random.choice(state.get_possible_actions())
        except IndexError:
            raise Exception("Non-terminal state has no possible actions: " + str(state))
        state = state.take_action(action)
    return state.get_reward()


def random_policy_no_duplicate(state, node):
    known_actions = [n.action_id for n in node.children if n.is_fully_discovered]
    possible_actions = [action for action in state.get_possible_actions() if action.skill not in known_actions]
    while not state.is_terminal():
        try:
            action = random.choice(possible_actions)
        except IndexError:
            raise Exception("Non-terminal state has no possible actions: " + str(state))
        state = state.take_action(action)
        possible_actions = state.get_possible_actions()
    return state.get_reward()


class TreeNode:
    def __init__(self, state, parent, action_id=None):
        self.state = state
        self.is_terminal = state.is_terminal()
        self.is_fully_expanded = self.is_terminal
        self.is_fully_discovered = False
        self.parent = parent
        self.num_visits = 0
        self.total_reward = 0
        self.max_reward = 0
        self.children = {}
        self.action_id = action_id
        self.stateHash = state.hash()
        pass

    def __repr__(self):
        return str(self.action_id) + ": " + str(self.max_reward) + " (" + str(0 if self.num_visits == 0 else self.total_reward/self.num_visits) + " = " + str(self.total_reward) \
               + "/" + str(self.num_visits) + ")"


class MCTS_Classical():
    def __init__(self, time_limit=None, iteration_limit=None, exploration_constant=math.sqrt(2), rollout_policy=random_policy):
        if time_limit is not None:
            if iteration_limit is not None:
                raise ValueError("Cannot have both a time limit and an iteration limit")
            self.time_limit = time_limit
            self.limit_type = 'time'
        else:
            if iteration_limit is None:
                raise ValueError("Must have either a time limit or an iteration limit")
            # number of iterations of the search
            if iteration_limit < 1:
                raise ValueError("Iteration limit must be greater than one")
            self.search_limit = iteration_limit
            self.limit_type = 'iterations'
        self.exploration_constant = exploration_constant
        self.rollout = rollout_policy
        self.number_of_iterations = 0

    def search(self, initial_state):
        self.root = TreeNode(initial_state, None)
        if self.limit_type == 'time':
            time_limit = time.time() + self.time_limit
            while time.time() < time_limit:
                self.execute_round()
                self.number_of_iterations += 1
        else:
            for i in range(self.search_limit):
                self.execute_round()
                self.number_of_iterations += 1

        best_child = self.get_best_child(self.root, 0)
        return self.get_action(self.root, best_child)

    def execute_round(self):
        node = self.select_node(self.root)
        reward = self.rollout(node.state)
        self.backpropogate(node, reward)

    def select_node(self, node):
        while not node.is_terminal:
            if node.is_fully_expanded:
                node = self.get_best_child(node, self.exploration_constant)
            else:
                return self.expand(node)
        return node

    def expand(self, node):
        actions = node.state.get_possible_actions()
        for action in actions:
            if action not in node.children:
                new_node = TreeNode(node.state.take_action(action), node, action.skill)
                node.children[action] = new_node
                if len(actions) == len(node.children):
                    node.is_fully_expanded = True
                return new_node

        raise Exception("Should never reach here")

    def backpropogate(self, node, reward):
        while node is not None:
            node.num_visits += 1
            node.total_reward += reward
            node = node.parent

    def get_best_child(self, node, exploration_value):
        best_value = float("-inf")
        best_nodes = []
        for child in node.children.values():
            node_value = node.state.get_current_player() * child.total_reward / child.num_visits \
                        + exploration_value * math.sqrt(math.log(node.num_visits) / child.num_visits)
            if node_value > best_value:
                best_value = node_value
                best_nodes = [child]
            elif node_value == best_value:
                best_nodes.append(child)
        return random.choice(best_nodes)

    def get_best_undiscovered_child(self, node, exploration_value):
        best_value = float("-inf")
        best_nodes = []

        for child in node.children.values():
            node_value = node.state.get_current_player() * child.total_reward / child.num_visits \
                        + exploration_value * math.sqrt(math.log(node.num_visits) / child.num_visits)
            if node_value > best_value:
                best_value = node_value
                best_nodes = [child]
            elif node_value == best_value:
                best_nodes.append(child)

        return random.choice(best_nodes)

    def get_action(self, root, bestChild):
        for action, node in root.children.items():
            if node is bestChild:
                return action

    def get_best_chain(self):
        chain = []
        best_child = self.root
        chain.append(self.root)
        while not best_child.is_terminal and best_child.children:
            best_child = self.get_best_child(best_child, 0)
            chain.append(best_child)
        return chain

    def print_best_chain(self):
        chain = self.get_best_chain()
        s = "X"
        for node in chain:
            if not node.action_id is None:
                s += " > " + str(node.action_id) + "(" + str(node.total_reward) + "/" + str(node.num_visits) + ")"
        print(s)

    def print_best_chain_and_brothers(self, skills):
        chain = self.get_best_chain()
        s = ""
        i = 0
        effective_action = 0
        node = self.root
        while i < len(chain) and len(node.children) > 0:
            if len(node.children) == 1:
                i += 1
                node = chain[i]
                continue
            effective_action += 1
            s += "Action "+str(effective_action)+":\n"
            for childaction_id in node.children:
                child = node.children[childaction_id]
                if i+1 < len(chain) and child.action_id == chain[i+1].action_id:
                    s += ">"
                s += "\t\t" + skills[child.action_id].name + "(" + str(child.total_reward/child.num_visits) + " = " + str(child.total_reward) + "/" + str(child.num_visits) + ")\n"
            i += 1
            if i < len(chain):
                node = chain[i]
        print(s)


class MCTS_Best_Score(MCTS_Classical):
    def __init__(self, time_limit=None, iteration_limit=None, exploration_constant=math.sqrt(2), rollout_policy=random_policy_no_duplicate):
        if time_limit is not None:
            if iteration_limit is not None:
                raise ValueError("Cannot have both a time limit and an iteration limit")
            self.time_limit = time_limit
            self.limitType = 'time'
        else:
            if iteration_limit is None:
                raise ValueError("Must have either a time limit or an iteration limit")
            # number of iterations of the search
            if iteration_limit < 1:
                raise ValueError("Iteration limit must be greater than one")
            self.searchLimit = iteration_limit
            self.limitType = 'iterations'
        self.explorationConstant = exploration_constant
        self.rollout = rollout_policy
        self.numberOfIterations = 0

    def search(self, initial_state):
        self.root = TreeNode(initial_state, None)
        if self.limitType == 'time':
            time_limit = time.time() + self.time_limit
            while time.time() < time_limit:
                self.execute_round()
                self.numberOfIterations += 1
        else:
            for i in range(self.searchLimit):
                ended = self.execute_round()
                if ended:
                    break
                self.numberOfIterations += 1

        bestChild = self.get_best_child(self.root, 0)
        return self.get_action(self.root, bestChild)

    def execute_round(self):
        node = self.select_node(self.root)
        if node is None:
            return True
        reward = self.rollout(node.state,node)
        self.backpropogate(node, reward)
        return False

    def select_node(self, node):
        while not node.is_terminal:
            if node.is_fully_expanded:
                node = self.get_best_undiscovered_child(node, self.explorationConstant)
                if node is None:
                    return None
            else:
                return self.expand(node)
        return node

    def expand(self, node):
        actions = node.state.get_possible_actions()
        for action in actions:
            if action not in node.children:
                new_node = TreeNode(node.state.take_action(action), node, action.skill)
                node.children[action] = new_node
                if len(actions) == len(node.children):
                    node.is_fully_expanded = True
                return new_node

        raise Exception("Should never reach here")

    def backpropogate(self, node, reward):
        while node is not None:
            node.num_visits += 1
            node.total_reward += reward
            node.max_reward = max(node.max_reward,reward)

            if self.check_discovery(node):
                node.is_fully_discovered = True

            node = node.parent

    @staticmethod
    def check_discovery(node):
        if node.is_terminal:
            return True
        if not node.is_fully_expanded:
            return False
        for child in node.children.values():
            if not child.is_fully_discovered:
                return False
        return True

    def get_best_child(self, node, exploration_value):
        best_value = float("-inf")
        best_nodes = []
        for child in node.children.values():
            node_value = node.state.get_current_player() * child.max_reward \
                        + exploration_value * math.sqrt(math.log(node.num_visits) / child.num_visits)
            if node_value > best_value:
                best_value = node_value
                best_nodes = [child]
            elif node_value == best_value:
                best_nodes.append(child)
        return random.choice(best_nodes)

    def get_best_undiscovered_child(self, node, exploration_value):
        undiscovered_children = [child for child in node.children.values() if not child.is_fully_discovered]

        if len(undiscovered_children) == 0:
            return None

        best_value = float("-inf")
        best_nodes = []

        for child in undiscovered_children:
            node_value = node.state.get_current_player() * child.max_reward \
                        + exploration_value * math.sqrt(math.log(node.num_visits) / child.num_visits)
            if node_value > best_value:
                best_value = node_value
                best_nodes = [child]
            elif node_value == best_value:
                best_nodes.append(child)

        chosen = random.choice(best_nodes)
        return chosen

    def get_action(self, root, best_child):
        for action, node in root.children.items():
            if node is best_child:
                return action

    def get_best_chain(self):
        chain = []
        bestChild = self.root
        chain.append(self.root)
        while not bestChild.is_terminal and bestChild.children:
            bestChild = self.get_best_child(bestChild, 0)
            chain.append(bestChild)
        return chain

    def print_best_chain(self):
        chain = self.get_best_chain()
        s = "X"
        for node in chain:
            if not node.action_id is None:
                s += " > " + str(node.action_id) \
                     #+ ": " + str(node.max_reward) + " (" + str(node.total_reward) + "/" + str(node.num_visits) + ")"
        print(s)

    def print_best_chain_and_brothers(self, skills):
        chain = self.get_best_chain()
        s = ""
        i = 0
        effective_action = 0
        node = self.root
        while i < len(chain) and len(node.children) > 0:
            if len(node.children) == 1:
                i += 1
                node = chain[i]
                continue
            effective_action += 1
            s += "Action "+str(effective_action)+":\n"
            for childaction_id in node.children:
                child = node.children[childaction_id]
                if i+1 < len(chain) and child.action_id == chain[i+1].action_id:
                    s += ">"
                s += "\t\t" + skills[child.action_id].name + ": " + str(child.max_reward) + "(" + str(child.total_reward/child.num_visits) + " = " + str(child.total_reward) + "/" + str(child.num_visits) + ")\n"
            i += 1
            if i < len(chain):
                node = chain[i]
        print(s)