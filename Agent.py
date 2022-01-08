# Agent.py
#
#Cpts 440 Artificial Intelligence
#Homework #9
#Student: Anita Whyatt


import Action
import Orientation
import Search
import random

class WorldState:
    def __init__(self):
	self.agentLocation = [1,1]
	self.agentOrientation = Orientation.RIGHT
	self.agentHasArrow = True
	self.agentHasGold = False
	self.stenchLocations = []
	self.wumpusLocation = []
	self.wumpusAlive = True
	self.goldLocation = []
	self.visitedLocations = []
	self.worldSize = [1,1] #until proven otherwise
	self.breezeLocations = []
	self.pitLocations = []
	self.maxWorldY = 9 #until proven otherwise
	self.maxWorldX = 9 #unitl proven otherwise
	self.prevGoalTile = [0,0] #holds a goal tile from a prior run


class Agent:
    def __init__(self):
	self.previousAction = Action.CLIMB
	self.worldState = WorldState()
	self.agentHasGold = False
	self.wumpusAlive = True
        self.actionList = []
        self.searchEngine = Search.SearchEngine()

    def __del__(self):
        pass

    def Initialize(self):
	self.worldState.agentLocation = [1,1]
        self.worldState.agentOrientation = Orientation.RIGHT
        self.worldState.agentHasArrow = True
        self.worldState.agentHasGold = False
        self.previousAction = Action.CLIMB
        self.actionList = []


    def tileExist(self, tile): #checks if a tile exists
	if (tile[0] > 0 and tile[0] <= self.worldState.maxWorldX
		and tile[1] > 0 and tile[1] <= self.worldState.maxWorldY):
	    return(True)
	else:
	    return(False)

    def adjacentTiles(self, tile): #return list of adjacent tiles
	listOfTiles = []
	if self.tileExist([ tile[0]+1, tile[1] ]) == True:
	    listOfTiles.append([ tile[0]+1, tile[1] ])
	if self.tileExist([ tile[0]-1, tile[1] ]) == True:
	    listOfTiles.append([ tile[0]-1, tile[1] ])
	if self.tileExist([ tile[0], tile[1]+1 ]) == True:
	    listOfTiles.append([ tile[0], tile[1]+1 ])
	if self.tileExist([ tile[0], tile[1]-1 ]) == True:
	    listOfTiles.append([ tile[0], tile[1]-1 ])
	return listOfTiles

    def shootWumpusWhere(self):
	ix = self.worldState.wumpusLocation[0]
	iy = self.worldState.wumpusLocation[1]
	while ix > 0:
	    ix -= 1
	    if [ix, self.worldState.wumpusLocation[1]] in self.searchEngine.safeLocations:
		return([ix, self.worldState.wumpusLocation[1]])
	while ix < self.worldState.worldSize[0]:
	    ix += 1
	    if [ix, self.worldState.wumpusLocation[1]] in self.searchEngine.safeLocations:
		return(ix, self.worldState.wumpusLocation[1])
	while iy > 0:
	    iy -= 1
	    if [self.worldState.wumpusLocation[0], iy] in self.searchEngine.safeLocations:
		return([self.worldState.wumpusLocation[0], iy])
	while iy < self.worldState.worldStize[1]:
	    iy += 1
	    if [self.worldState.wumpusLocation[0], iy] in self.searchEngine.safeLocations:
		return([self.worldState.wumpusLocation[0], iy])
	return[0,0]


    def Process (self, percept):
	###############################################################
	#UPDATE KNOWLEDGE PHASE
	###############################################################
	self.UpdateState(percept)
	#Update our percept location lists
	if percept.stench:
	    if (self.worldState.agentLocation
		    not in self.worldState.stenchLocations):
		self.worldState.stenchLocations.append(self.worldState.agentLocation)
	if percept.glitter:
	    if (self.worldState.agentLocation
		    not in self.worldState.goldLocation):
		self.worldState.goldLocation = self.worldState.agentLocation
	if percept.breeze:
            if (self.worldState.agentLocation
		    not in self.worldState.breezeLocations):
                self.worldState.breezeLocations.append(self.worldState.agentLocation)
	if percept.scream:
	    self.worldState.wumpusAlive = False

	#world size updates
	if self.worldState.agentLocation[0] > self.worldState.worldSize[0]:
	    self.worldState.worldSize[0] = self.worldState.agentLocation[0]
	if self.worldState.agentLocation[1] > self.worldState.worldSize[1]:
	    self.worldState.worldSize[1] = self.worldState.agentLocation[1]
	#update our visited locations
	if (self.worldState.agentLocation
		not in self.worldState.visitedLocations):
	    self.worldState.visitedLocations.append(self.worldState.agentLocation)

	#The loop logic for stench locations locating wumpus (part f in prompt)
	if self.worldState.stenchLocations != []:
	    for location in self.worldState.stenchLocations:
		testLocation = [location[0] + 1, location[1] + 1 ]
		if testLocation in self.worldState.stenchLocations:
		    if ( [location[0], testLocation[1]]
			    in self.worldState.visitedLocations ):
			if ( [testLocation[0], location[1]]
				not in self.worldState.wumpusLocation ):
			    self.worldState.wumpusLocation = [testLocation[0], location[1]]
		    elif ( [testLocation[0], location[1]]
			    in self.worldState.visitedLocations ):
			if ( [location[0], testLocation[1]]
				not in self.worldState.wumpusLocation ):
			    self.worldState.wumpusLocation = [location[0], testLocation[1]]

		testLocation = [location[0] - 1, location[1] - 1]
		if testLocation in self.worldState.stenchLocations:
		    if ( [location[0], testLocation[1]]
			    in self.worldState.visitedLocations):
                        if ( [testLocation[0], location[1]]
				not in self.worldState.wumpusLocation):
                            self.worldState.wumpusLocation = [testLocation[0], location[1]]
                    elif ( [testLocation[0], location[1]]
			    in self.worldState.visitedLocations ):
                        if ( [location[0], testLocation[1]]
				not in self.worldState.wumpusLocation ):
                            self.worldState.wumpusLocation = [location[0], testLocation[1]]

		testLocation = [location[0] + 1, location[1] - 1]
		if testLocation in self.worldState.stenchLocations:
		    if ( [location[0], testLocation[1]]
			    in self.worldState.visitedLocations ):
                        if ( [testLocation[0], location[1]]
				not in self.worldState.wumpusLocation ):
                            self.worldState.wumpusLocation = [testLocation[0], location[1]]
                    elif ( [testLocation[0], location[1]]
			    in self.worldState.visitedLocations ):
                        if ( [location[0], testLocation[1]]
				not in self.worldState.wumpusLocation ):
                            self.worldState.wumpusLocation = [location[0], testLocation[1]]

		testLocation = [location[0] - 1, location[1] + 1]
		if testLocation in self.worldState.stenchLocations:
		    if ( [location[0], testLocation[1]]
			    in self.worldState.visitedLocations ):
                        if ( [testLocation[0], location[1]]
				not in self.worldState.wumpusLocation ):
                            self.worldState.wumpusLocation = [testLocation[0], location[1]]
                    elif ( [testLocation[0], location[1]]
			    in self.worldState.visitedLocations ):
                        if ( [location[0], testLocation[1]]
				not in self.worldState.wumpusLocation ):
                            self.worldState.wumpusLocation = [location[0], testLocation[1]]

	#The loop logic for breeze locations locating pits:
	if self.worldState.breezeLocations != []:
	    for location in self.worldState.breezeLocations:
		testLocation = [location[0] + 1, location[1] + 1]
		if testLocation in self.worldState.breezeLocations:
		    if ( [location[0], testLocation[1]] in self.worldState.visitedLocations):
			if( [testLocation[0], location[1]] not in self.worldState.pitLocations ):
			    self.worldState.pitLocations.append([testLocation[0], location[1]])
		    elif( [testLocation[0], location[1]] in self.worldState.visitedLocations ):
			if ( [location[0], testLocation[1]] not in self.worldState.pitLocations ):
			    self.worldState.pitLocations.append([location[0], testLocation[1]])

		testLocation = [location[0] - 1, location[1] - 1]
		if testLocation in self.worldState.breezeLocations:
		    if ( [location[0], testLocation[1]] in self.worldState.visitedLocations):
			if ( [testLocation[0], location[1]] not in self.worldState.pitLocations):
			    self.worldState.pitLocations.append([testLocation[0], location[1]])
		    elif ( [testLocation[0], location[1]] in self.worldState.visitedLocations ):
			if ( [location[0], testLocation[1]] not in self.worldState.pitLocations):
			    self.worldState.pitLocations.append([location[0], testLocation[1]])

		testLocation = [location[0] + 1, location[1] - 1]
		if testLocation in self.worldState.breezeLocations:
		    if( [location[0], testLocation[1]] in self.worldState.visitedLocations):
			if( [testLocation[0], location[1]] not in self.worldState.pitLocations ):
			    self.worldState.pitLocations.append([testLocation[0], location[1]])
		    elif ( [testLocation[0], location[1]] in self.worldState.visitedLocations ):
			if( [location[0], testLocation[1]] not in self.worldState.pitLocations):
			    self.worldState.pitLocations.append([location[0], testLocation[1]])

		testLocation = [location[0] - 1, location[1] + 1]
		if testLocation in self.worldState.breezeLocations:
		    if ( [location[0], testLocation[1]] in self.worldState.visitedLocations):
			if ( [testLocation[0], location[1]] not in self.worldState.pitLocations):
			    self.worldState.pitLocations.append([testLocation[0], location[1]])
		    elif ([testLocation[0], location[1]] in self.worldState.visitedLocations):
			if ( [location[0], testLocation[1]] not in self.worldState.pitLocations ):
			    self.worldState.pitLocations.append([location[0], testLocation[1]])


	    #should we know the location of wumpus or pits we clarify they are not safe locations:
	    if self.worldState.wumpusLocation != []:
		if self.worldState.wumpusLocation in self.searchEngine.safeLocations:
		    print("removing wumpus from safe locations!!!!!!!!!!!!!!!!")
		    self.searchEngine.RemoveSafeLocation(self.worldState.wumpusLocation[0], self.worldState.wumpusLocation[1])

	    if self.worldState.pitLocations != []:
		for location in self.worldState.pitLocations:
		    if location in self.searchEngine.safeLocations:
			self.searchEngine.RemoveSafeLocation(location)









	#maxWorldY updates:
	if percept.bump == True and self.worldState.agentOrientation == 1:
	    self.worldState.maxWorldY = self.worldState.agentLocation[1]
	    for x in range(1,10):
		if [x, self.worldState.maxWorldY+1] in self.searchEngine.safeLocations:
		    self.searchEngine.RemoveSafeLocation(x, self.worldState.maxWorldY+1)
	#maxWorldX updates:
	if percept.bump == True and self.worldState.agentOrientation == 0:
	    self.worldState.maxWorldX = self.worldState.agentLocation[0]
	    for y in range(1,10):
		if [self.worldState.maxWorldX+1, y] in self.searchEngine.safeLocations:
		    self.searchEngine.RemoveSafeLocation(self.worldState.maxWorldX+1, y)

	#update current location to safe location
	if (self.worldState.agentLocation not in self.searchEngine.safeLocations):
	    self.searchEngine.AddSafeLocation(self.worldState.agentLocation[0],
		self.worldState.agentLocation[1])
	#update adjacent location to safe location if !stench and !breeze
	if percept.breeze == False and percept.stench == False:
	    for tile in self.adjacentTiles(self.worldState.agentLocation):
		if tile not in self.searchEngine.safeLocations:
		    self.searchEngine.AddSafeLocation(tile[0], tile[1])

	#If wumpus location known, update safeness of stench adjacent squares:
	if self.worldState.wumpusLocation != []:
	    for smellyTile in self.worldState.stenchLocations:
		if smellyTile not in self.worldState.breezeLocations: #don't free up breeze tiles
		    for adjTile in self.adjacentTiles(smellyTile):
			if( (adjTile != self.worldState.wumpusLocation)
				and (adjTile not in self.searchEngine.safeLocations) ):
			    self.searchEngine.AddSafeLocation(adjTile[0], adjTile[1])




	#######################################################################
	#PRINT PHASE
	#######################################################################
        print("What does our agent know?")
        print("Orientation:", self.worldState.agentOrientation, "(0=R, 1=U, 2=L, 3=D)")
        print("Location:", self.worldState.agentLocation, "[X,Y]")
        print("Has Arrow?", self.worldState.agentHasArrow)
        print("Has Gold?", self.worldState.agentHasGold)
        print("Previous Action:", self.previousAction, "(0=F 1=L 2=R 3=G 4=S 5=C)")
        print("Action list:", self.actionList)
        print("Stench locations:", self.worldState.stenchLocations)
        print("Wumpus Location:", self.worldState.wumpusLocation)
	print("Breeze locations:", self.worldState.breezeLocations)
#	print("Pit locations:", self.worldState.pitLocations) #removed after email announcement
        print("Gold Location:", self.worldState.goldLocation)
        print("Visited Locations:", self.worldState.visitedLocations)
        print("World Size", self.worldState.worldSize)
	print("Safe locations:", self.searchEngine.safeLocations)
#	c = raw_input("wait") #optional wait command



	#######################################################################
	#DECISION -> ACTION PHASE
	#######################################################################
        #if you see the gold GRAB it
        if percept.glitter == True:
            action = Action.GRAB
	    self.previousAction = action
            return action
	#if you are in [1,1] and have the gold, CLIMB
	if self.worldState.agentLocation == [1,1] and self.worldState.agentHasGold:
	    action = Action.CLIMB
	    self.previousAction = action
	    return action
	#if you know where gold is and don't have it, get it
	if ( self.worldState.agentHasGold == False and self.worldState.goldLocation != []
		and self.actionList == [] ):
	    self.actionList += self.searchEngine.FindPath(self.worldState.agentLocation,
							  self.worldState.agentOrientation,
							  self.worldState.goldLocation,
							  Orientation.RIGHT)
	#if you have the gold but aren't in the (1,1) location, go to (1,1)
	if self.worldState.agentHasGold == True and self.worldState.agentLocation != [1,1]:
	    self.actionList = []
	    self.actionList += self.searchEngine.FindPath(self.worldState.agentLocation,
							  self.worldState.agentOrientation,
							  [1,1], Orientation.RIGHT)

	#if agent does not have the gold, and there are no more safe unvisited locations then:
	#a: if the agent knows the location of the live wumpus and there is a safe location facing
	#   the wumpus, then the agent should move there and shoot the wumpus
	safeUnvisitLoc = False
	for safeLoc in self.searchEngine.safeLocations:
	    if safeLoc not in self.worldState.visitedLocations:
		safeUnvisitLoc = True
	if self.worldState.wumpusLocation != []:
	    shootLocation = self.shootWumpusWhere()

	if ( self.worldState.agentHasGold == False and safeUnvisitLoc == False and self.actionList == []):
	    if (self.worldState.wumpusLocation != [] and self.worldState.wumpusAlive == True):
		if shootLocation != [0,0]:
		    if shootLocation[0] < self.worldState.wumpusLocation[0]:
			self.actionList += self.searchEngine.FindPath(self.worldState.agentLocation,
									self.worldState.agentOrientation,
									shootLocation, Orientation.RIGHT)
		    elif shootLocation[0] > self.worldState.wumpusLocation[0]:
			self.actionList += self.searchEngine.FindPath(self.worldState.agentLocation,
									self.worldState.agentOrientation,
									shootLocation, Orientation.LEFT)
		    elif shootLocation[1] < self.worldState.wumpusLocation[1]:
			self.actionList += self.searchEngine.FindPath(self.worldState.agentLocation,
									self.worldState.agentOrientation,
									shootLocation, Orientation.UP)
		    elif shootLocation[1] > self.worldState.wumpusLocation[1]:
			self.actionList += self.searchEngine.FindPath(self.worldState.agentLocation,
									self.worldState.agentOrientation,
									shootLocation, Orientation.DOWN)
		    self.actionList += Action.SHOOT


	#b: (below) if the wumpus is dead or cannot be killed then the agent should move to an unvisited
	#   locationg this is not known to be unsafe



	#Choose a random exploration action
	goalTile = []
	goalTileList = []
	if self.actionList == []: #only if not running action list already
	    for safeTile in self.searchEngine.safeLocations:
		if ( (safeTile not in self.worldState.visitedLocations)
			and (safeTile in self.adjacentTiles(self.worldState.agentLocation)) ):
		    goalTileList.append(safeTile)
	    if self.worldState.prevGoalTile in goalTileList:
		goalTileList.remove(self.worldState.prevGoalTile)

	    if goalTileList != []:
		goalTile = random.choice(goalTileList)
		self.worldState.prevGoalTile = goalTile
		self.actionList += self.searchEngine.FindPath(self.worldState.agentLocation,
							      self.worldState.agentOrientation,
							      goalTile, Orientation.RIGHT)
	    #if there is no adjacent tile that meets our requirements, we select a non-adjacent tile
	    if goalTileList == []:
		for safeTile in self.searchEngine.safeLocations:
		    if safeTile not in self.worldState.visitedLocations:
			goalTileList.append(safeTile)
		if self.worldState.prevGoalTile in goalTileList:
		    goalTileList.remove(self.worldState.prevGoalTile)

		if goalTileList != []:
		    goalTile = random.choice(goalTileList)
		    self.worldState.prevGoalTile = goalTile
		    self.actionList += self.searchEngine.FindPath(self.worldState.agentLocation,
								  self.worldState.agentOrientation,
								  goalTile, Orientation.RIGHT)
	    #if STILL no options we take a chance
	    if goalTileList == []:
		for visTile in self.worldState.visitedLocations:
		    for riskTile in self.adjacentTiles(visTile):
			if riskTile not in self.worldState.visitedLocations:
			    goalTileList.append(riskTile)
		if self.worldState.prevGoalTile in goalTileList:
		    goalTileList.remove(self.worldState.prevGoalTile)

		goalTile = random.choice(goalTileList)
		self.worldState.prevGoalTile = goalTile
		print("************************************************************")
		print("No safe options! Taking a chance!", goalTile)
		if goalTile not in self.searchEngine.safeLocations: #necessary for taking a chance
		    self.searchEngine.AddSafeLocation(goalTile[0], goalTile[1])
		self.actionList += self.searchEngine.FindPath(self.worldState.agentLocation,
							      self.worldState.agentOrientation,
							      goalTile, Orientation.RIGHT)


	#if the action list is not null, execute the action list:
	if self.actionList != []:
	    action = self.actionList.pop(0)
	    self.previousAction = action
	    return action



    def UpdateState(self, percept):
        currentOrientation = self.worldState.agentOrientation
        if (self.previousAction == Action.GOFORWARD):
            if (not percept.bump):
                self.Move()
        if (self.previousAction == Action.TURNLEFT):
            self.worldState.agentOrientation = (currentOrientation + 1) % 4
        if (self.previousAction == Action.TURNRIGHT):
            currentOrientation -= 1
            if (currentOrientation < 0):
                currentOrientation = 3
            self.worldState.agentOrientation = currentOrientation
        if (self.previousAction == Action.GRAB):
            self.worldState.agentHasGold = True # Only GRAB when there's gold
        if (self.previousAction == Action.SHOOT):
            self.worldState.agentHasArrow = False
        # Nothing to do for CLIMB handled elsewhere



    def Move(self):
        X = self.worldState.agentLocation[0]
        Y = self.worldState.agentLocation[1]
        if (self.worldState.agentOrientation == Orientation.RIGHT):
            X = X + 1
        if (self.worldState.agentOrientation == Orientation.UP):
            Y = Y + 1
        if (self.worldState.agentOrientation == Orientation.LEFT):
            X = X - 1
        if (self.worldState.agentOrientation == Orientation.DOWN):
            Y = Y - 1
        self.worldState.agentLocation = [X,Y]


    def GameOver(self, score):
        pass
