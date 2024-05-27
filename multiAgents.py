from util import manhattanDistance
from game import Directions
import random, util, sys  # Importaciones necesarias

from game import Agent

class ReflexAgent(Agent):
    
    def getAction(self, gameState):
        legalMoves = gameState.getLegalActions()
        # Evaluación de las acciones disponibles
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)  # Selecciona una acción al azar de las mejores acciones
        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        # Evalúa el estado del juego después de tomar una acción
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        Food = newFood.asList()
        gPos = successorGameState.getGhostPositions()  # Posiciones de los fantasmas
        FoodDist = []  # Distancias a la comida
        GhostDist = []  # Distancias a los fantasmas

        for food in Food:
            FoodDist.append(manhattanDistance(food, newPos))  # Calcula la distancia de Manhattan a la comida
        for ghost in gPos:
            GhostDist.append(manhattanDistance(ghost, newPos))  # Calcula la distancia de Manhattan a los fantasmas

        if currentGameState.getPacmanPosition() == newPos:
            return -(float("inf"))  # Evitar quedarse en el mismo lugar

        for dist in GhostDist:
            if dist < 2:
                return -(float("inf"))  # Evitar fantasmas cercanos
        if len(FoodDist) == 0:
            return float("inf")  # Si no hay comida, maximiza la puntuación
        return 1000 / sum(FoodDist) + 10000 / len(FoodDist)  # Evaluar la acción

def scoreEvaluationFunction(currentGameState):
    return currentGameState.getScore()  # Función de evaluación básica basada en la puntuación del juego

class MultiAgentSearchAgent(Agent):
    
    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman siempre es el agente 0
        self.evaluationFunction = util.lookup(evalFn, globals())  # Función de evaluación para el agente
        self.depth = int(depth)  # Profundidad de búsqueda

class MinimaxAgent(MultiAgentSearchAgent):

    def getAction(self, gameState):
        def max_value(gameState, depth):
            Actions = gameState.getLegalActions(0)
            if len(Actions) == 0 or gameState.isWin() or gameState.isLose() or depth == self.depth:
                return self.evaluationFunction(gameState), None  # Evaluar el estado del juego

            w = -(float("inf"))
            Act = None
            for action in Actions:
                sucsValue = min_value(gameState.generateSuccessor(0, action), 1, depth)
                sucsValue = sucsValue[0]
                if sucsValue > w:
                    w, Act = sucsValue, action
            return w, Act

        def min_value(gameState, agentID, depth):
            Actions = gameState.getLegalActions(agentID)
            if len(Actions) == 0:
                return self.evaluationFunction(gameState), None  # Evaluar el estado del juego

            l = float("inf")
            Act = None
            for action in Actions:
                if agentID == gameState.getNumAgents() - 1:
                    sucsValue = max_value(gameState.generateSuccessor(agentID, action), depth + 1)
                else:
                    sucsValue = min_value(gameState.generateSuccessor(agentID, action), agentID + 1, depth)
                sucsValue = sucsValue[0]
                if sucsValue < l:
                    l, Act = sucsValue, action
            return l, Act

        max_value = max_value(gameState, 0)[1]
        return max_value

class AlphaBetaAgent(MultiAgentSearchAgent):
    
    def getAction(self, gameState):   
        def max_value(gameState, depth, a, b):
            Actions = gameState.getLegalActions(0) 
            if len(Actions) == 0 or gameState.isWin() or gameState.isLose() or depth == self.depth:
                return self.evaluationFunction(gameState), None  # Evaluar el estado del juego

            w = -(float("inf"))
            Act = None
            for action in Actions:
                sucsValue = min_value(gameState.generateSuccessor(0, action), 1, depth, a, b)
                sucsValue = sucsValue[0]
                if w < sucsValue:
                    w, Act = sucsValue, action
                if w > b:
                    return w, Act
                a = max(a, w)
            return w, Act

        def min_value(gameState, agentID, depth, a, b):
            Actions = gameState.getLegalActions(agentID)
            if len(Actions) == 0:
                return self.evaluationFunction(gameState), None  # Evaluar el estado del juego

            l = float("inf")
            Act = None
            for action in Actions:
                if agentID == gameState.getNumAgents() - 1:
                    sucsValue = max_value(gameState.generateSuccessor(agentID, action), depth + 1, a, b)
                else:
                    sucsValue = min_value(gameState.generateSuccessor(agentID, action), agentID + 1, depth, a, b)
                sucsValue = sucsValue[0]
                if sucsValue < l:
                    l, Act = sucsValue, action
                if l < a:
                    return l, Act
                b = min(b, l)
            return l, Act
        
        a = -(float("inf"))
        b = float("inf")
        max_value = max_value(gameState, 0, a, b)[1]
        return max_value

class ExpectimaxAgent(MultiAgentSearchAgent):
    
    def getAction(self, gameState):
        def max_value(gameState, depth):
            Actions = gameState.getLegalActions(0)
            if len(Actions) == 0 or gameState.isWin() or gameState.isLose() or depth == self.depth:
                return self.evaluationFunction(gameState), None  # Evaluar el estado del juego

            w = -(float("inf"))
            Act = None

            for action in Actions:
                sucsValue = exp_value(gameState.generateSuccessor(0, action), 1, depth)
                sucsValue = sucsValue[0]
                if w < sucsValue:
                    w, Act = sucsValue, action
            return w, Act

        def exp_value(gameState, agentID, depth):
            Actions = gameState.getLegalActions(agentID)
            if len(Actions) == 0:
                return self.evaluationFunction(gameState), None  # Evaluar el estado del juego

            l = 0
            Act = None
            for action in Actions:
                if agentID == gameState.getNumAgents() - 1:
                    sucsValue = max_value(gameState.generateSuccessor(agentID, action), depth + 1)
                else:
                    sucsValue = exp_value(gameState.generateSuccessor(agentID, action), agentID + 1, depth)
                sucsValue = sucsValue[0]
                prob = sucsValue / len(Actions)
                l += prob
            return l, Act

        max_value = max_value(gameState, 0)[1]
        return max_value

def betterEvaluationFunction(currentGameState):
    # Obtener la posición actual del Pacman
    pacPosition = currentGameState.getPacmanPosition()
    # Obtener una lista de estados de los fantasmas
    gList = currentGameState.getGhostStates()
    # Obtener la disposición de la comida
    Food = currentGameState.getFood()
    # Obtener la ubicación de las cápsulas
    Capsules = currentGameState.getCapsules()

    # Si el estado actual es una victoria, asignar un valor infinito
    if currentGameState.isWin():
        return float("inf")
    # Si el estado actual es una derrota, asignar un valor negativo infinito
    if currentGameState.isLose():
        return float("-inf")

    # Calcular la distancia Manhattan a los alimentos
    foodDistList = [util.manhattanDistance(food, pacPosition) for food in Food.asList()]
    minFDist = min(foodDistList) if foodDistList else 0

    # Calcular la distancia Manhattan a los fantasmas normales y asustados
    GhDistList = []
    ScGhDistList = []
    for ghost in gList:
        dist = util.manhattanDistance(pacPosition, ghost.getPosition())
        if ghost.scaredTimer == 0:
            GhDistList.append(dist)
        elif ghost.scaredTimer > 0:
            ScGhDistList.append(dist)

    # Obtener las distancias mínimas a los fantasmas normales y asustados
    minGhDist = min(GhDistList) if GhDistList else 0
    minScGhDist = min(ScGhDistList) if ScGhDistList else 0

    # Calcular el valor de la evaluación teniendo en cuenta varios factores
    score = scoreEvaluationFunction(currentGameState)
    score -= 1.5 * minFDist + 2 * (1.0 / (minGhDist + 1)) + 2 * minScGhDist + 20 * len(Capsules) + 4 * len(Food.asList())
    return score

better = betterEvaluationFunction

