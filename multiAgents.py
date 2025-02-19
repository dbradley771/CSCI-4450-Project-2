# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
from math import inf
import random, util, time

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPosition).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPosition = successorGameState.getPacmanPosition()
        currentFood = currentGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()

        # Don't go where ghosts could go
        badGhostPositions = [ghostState.getPosition() for ghostState in newGhostStates if ghostState.scaredTimer == 0]
        for (x, y) in badGhostPositions:
            x = int(x)
            y = int(y)
            for (xAdj, yAdj) in [(0, 0), (1, 0), (0, 1), (-1, 0), (0, -1)]:
                nearPos = (x + xAdj, y + yAdj)
                if(newPosition == nearPos):
                    return -inf

        # Go to nearest food
        closestFoodDistance = inf
        for x, row in enumerate(currentFood):
            for y, food in enumerate(row):
                if(food):
                    foodDistance = manhattanDistance(newPosition, (x, y))
                    if(foodDistance < closestFoodDistance):
                        closestFoodDistance = foodDistance

        return successorGameState.getScore() - closestFoodDistance

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        # Collect legal moves and successor states
        agentIndex = 0
        actions = gameState.getLegalActions(agentIndex)
        return max(actions, key = lambda action: self.value(gameState.generateSuccessor(agentIndex, action), agentIndex + 1, 0))
        
    def maxValue(self, gameState, agentIndex, depth):
        stateValue = -inf
        successorStates = [gameState.generateSuccessor(agentIndex, action) for action in gameState.getLegalActions(agentIndex)]
        for state in successorStates:
            stateValue = max(stateValue, self.value(state, agentIndex + 1, depth))
        return stateValue
    
    def minValue(self, gameState, agentIndex, depth):
        stateValue = inf
        successorStates = [gameState.generateSuccessor(agentIndex, action) for action in gameState.getLegalActions(agentIndex)]
        for state in successorStates:
            stateValue = min(stateValue, self.value(state, agentIndex + 1, depth))
        return stateValue

    def value(self, gameState, agentIndex, depth):
        if(agentIndex >= gameState.getNumAgents()):
            agentIndex = 0
            depth = depth + 1

        if(gameState.isWin() or gameState.isLose() or depth >= self.depth):
            # Terminal state
            return self.evaluationFunction(gameState)

        if(agentIndex == 0):
            return self.maxValue(gameState, agentIndex, depth)
        else:
            return self.minValue(gameState, agentIndex, depth)
             

# This could be nicer, but I ran out of time...
class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        agentIndex = 0

        A = -inf
        B = inf
        bestAction = None
        bestValue = -inf
        for action in gameState.getLegalActions(agentIndex):
            successorState = gameState.generateSuccessor(agentIndex, action)
            successorValue = self.value(successorState, agentIndex + 1, 0, A, B)
            if(bestValue < successorValue):
                bestValue = successorValue
                bestAction = action

            if bestValue > B:
                return bestAction
            A = max(A, bestValue)

        return bestAction
        
    def maxValue(self, gameState, agentIndex, depth, A, B):
        stateValue = -inf
        for action in gameState.getLegalActions(agentIndex):
            successorState = gameState.generateSuccessor(agentIndex, action)
            successorValue = self.value(successorState, agentIndex + 1, depth, A, B)
            stateValue = max(stateValue, successorValue)
            if stateValue > B:
                return stateValue
            A = max(A, stateValue)
        return stateValue
    
    def minValue(self, gameState, agentIndex, depth, A, B):
        stateValue = inf
        for action in gameState.getLegalActions(agentIndex):
            successorState = gameState.generateSuccessor(agentIndex, action)
            successorValue = self.value(successorState, agentIndex + 1, depth, A, B)
            stateValue = min(stateValue, successorValue)
            if stateValue < A:
                return stateValue
            B = min(B, stateValue)
        return stateValue

    def value(self, gameState, agentIndex, depth, A, B):
        if(agentIndex >= gameState.getNumAgents()):
            agentIndex = 0
            depth = depth + 1

        if(gameState.isWin() or gameState.isLose() or depth >= self.depth):
            # Terminal state
            return self.evaluationFunction(gameState)

        if(agentIndex == 0):
            return self.maxValue(gameState, agentIndex, depth, A, B)
        else:
            return self.minValue(gameState, agentIndex, depth, A, B)

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        agentIndex = 0
        actions = gameState.getLegalActions(agentIndex)
        return max(actions, key = lambda action: self.value(gameState.generateSuccessor(agentIndex, action), agentIndex + 1, 0))

    def maxValue(self, gameState, agentIndex, depth):
        stateValue = -inf
        for action in gameState.getLegalActions(agentIndex):
            successorState = gameState.generateSuccessor(agentIndex, action)
            successorValue = self.value(successorState, agentIndex + 1, depth)
            stateValue = max(stateValue, successorValue)
        return stateValue
    
    def expValue(self, gameState, agentIndex, depth):
        stateValue = 0
        actions = gameState.getLegalActions(agentIndex)
        probability = 1/len(actions) # Equal probability for each action

        for action in actions:
            successorState = gameState.generateSuccessor(agentIndex, action)
            successorValue = self.value(successorState, agentIndex + 1, depth)
            stateValue = stateValue + probability * successorValue
        return stateValue

    def value(self, gameState, agentIndex, depth):
        if(agentIndex >= gameState.getNumAgents()):
            agentIndex = 0
            depth = depth + 1

        if(gameState.isWin() or gameState.isLose() or depth >= self.depth):
            # Terminal state
            return self.evaluationFunction(gameState)

        if(agentIndex == 0):
            return self.maxValue(gameState, agentIndex, depth)
        else:
            return self.expValue(gameState, agentIndex, depth)

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    currentPosition = currentGameState.getPacmanPosition()
    currentFood = currentGameState.getFood()
    ghostStates = currentGameState.getGhostStates()

    # Keep an eye on ghosts
    ghostValue = 0
    for ghostState in ghostStates:
        distance = manhattanDistance(currentPosition, ghostState.getPosition())
        if distance > 0:
            if ghostState.scaredTimer > 0:
                ghostValue += 10 / distance
            else:
                ghostValue -= 100 / distance

    # Go to nearest food
    closestFoodDistance = inf
    for x, row in enumerate(currentFood):
        for y, food in enumerate(row):
            if(food):
                foodDistance = manhattanDistance(currentPosition, (x, y))
                if(foodDistance < closestFoodDistance):
                    closestFoodDistance = foodDistance
    
    return currentGameState.getScore() + (10 / closestFoodDistance) + ghostValue

# Abbreviation
better = betterEvaluationFunction
