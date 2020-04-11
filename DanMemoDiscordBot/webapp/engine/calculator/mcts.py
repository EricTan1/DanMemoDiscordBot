from .helper import *
import time
import math
import random

def randomPolicy(state):
    while not state.isTerminal():
        try:
            action = random.choice(state.getPossibleActions())
        except IndexError:
            raise Exception("Non-terminal state has no possible actions: " + str(state))
        state = state.takeAction(action)
    return state.getReward()

class TreeNode():
    def __init__(self, state, parent, actionId=None):
        self.state = state
        self.isTerminal = state.isTerminal()
        self.isFullyExpanded = self.isTerminal
        self.parent = parent
        self.numVisits = 0
        self.totalReward = 0
        self.children = {}
        self.actionId = actionId
        self.stateHash = state.hash()
        pass

class MCTS():
    def __init__(self, timeLimit=None, iterationLimit=None, explorationConstant=math.sqrt(2), rolloutPolicy=randomPolicy):
        if timeLimit != None:
            if iterationLimit != None:
                raise ValueError("Cannot have both a time limit and an iteration limit")
            self.timeLimit = timeLimit
            self.limitType = 'time'
        else:
            if iterationLimit == None:
                raise ValueError("Must have either a time limit or an iteration limit")
            # number of iterations of the search
            if iterationLimit < 1:
                raise ValueError("Iteration limit must be greater than one")
            self.searchLimit = iterationLimit
            self.limitType = 'iterations'
        self.explorationConstant = explorationConstant
        self.rollout = rolloutPolicy
        self.numberOfIterations = 0

    def search(self, initialState):
        self.root = TreeNode(initialState, None)
        if self.limitType == 'time':
            timeLimit = time.time() + self.timeLimit
            while time.time() < timeLimit:
                self.executeRound()
                self.numberOfIterations += 1
        else:
            for i in range(self.searchLimit):
                self.executeRound()
                self.numberOfIterations += 1

        bestChild = self.getBestChild(self.root, 0)
        return self.getAction(self.root, bestChild)

    def executeRound(self):
        node = self.selectNode(self.root)
        reward = self.rollout(node.state)
        self.backpropogate(node, reward)

    def selectNode(self, node):
        while not node.isTerminal:
            if node.isFullyExpanded:
                node = self.getBestChild(node, self.explorationConstant)
            else:
                return self.expand(node)
        return node

    def expand(self, node):
        actions = node.state.getPossibleActions()
        for action in actions:
            if action not in node.children:
                newNode = TreeNode(node.state.takeAction(action), node, action.skill)
                node.children[action] = newNode
                if len(actions) == len(node.children):
                    node.isFullyExpanded = True
                return newNode

        raise Exception("Should never reach here")

    def backpropogate(self, node, reward):
        while node is not None:
            node.numVisits += 1
            node.totalReward += reward
            node = node.parent

    def getBestChild(self, node, explorationValue):
        bestValue = float("-inf")
        bestNodes = []
        for child in node.children.values():
            nodeValue = node.state.getCurrentPlayer() * child.totalReward / child.numVisits \
                        + explorationValue * math.sqrt(math.log(node.numVisits) / child.numVisits)
            if nodeValue > bestValue:
                bestValue = nodeValue
                bestNodes = [child]
            elif nodeValue == bestValue:
                bestNodes.append(child)
        return random.choice(bestNodes)

    def getAction(self, root, bestChild):
        for action, node in root.children.items():
            if node is bestChild:
                return action

    def getBestChain(self):
        chain = []
        bestChild = self.root
        chain.append(self.root)
        while not bestChild.isTerminal and bestChild.children:
            bestChild = self.getBestChild(bestChild,0)
            chain.append(bestChild)
        return chain

    def printBestChain(self):
        chain = self.getBestChain()
        s = "X"
        for node in chain:
            if not node.actionId is None:
                s += " > " + str(node.actionId) + "(" + str(node.totalReward) + "/" + str(node.numVisits) + ")"
        print(s)

    def printBestChainAndBrothers(self,skills):
        chain = self.getBestChain()
        s = ""
        i = 0
        effectiveAction = 0
        node = self.root
        while i < len(chain) and len(node.children) > 0:
            if len(node.children) == 1:
                i += 1
                node = chain[i]
                continue
            effectiveAction += 1
            s += "Action "+str(effectiveAction)+":\n"
            for childActionId in node.children:
                child = node.children[childActionId]
                if i+1 < len(chain) and child.actionId == chain[i+1].actionId:
                    s += ">"
                s += "\t\t" + skills[child.actionId].name + "(" + str(child.totalReward/child.numVisits) + " = " + str(child.totalReward) + "/" + str(child.numVisits) + ")\n"
            i += 1
            if i < len(chain):
                node = chain[i]
        print(s)