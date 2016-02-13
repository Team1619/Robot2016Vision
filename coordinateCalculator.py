import math
class vertexMath:
	def __init__(self, width, height, focalLength, targetWidth=5, targetHeight=10, armLength = 0.0, armHeight = 0):
		self.height = height*1.0
		self.centerH = height/2*1.0
		self.width = width*1.0
		self.centerW = width/2*1.0
		self.focalLength = focalLength*1.0
		self.targetHeight = targetHeight*1.0
		self.targetWidth = targetWidth*1.0
		self.armLength = armLength*1.0
		self.armHeight = armHeight*1.0
		self.acceptableError = 0.001
		self.desiredDistance = 100.0
	
	def setHeight(self, h):
		self.height = h
		self.centerH = h/2
	
	def setWidth(self, w):
		self.width = w
		self.centerW = w/2

	def setFocalLength(self, l):
		self.focalLength = l

	def getVertexData(self, intCoords, armAngle=15.0):

		accurate = True


			
		vertices = [[(intCoords[0][0]*1.0), (intCoords[0][1]*1.0)], [(intCoords[1][0]*1.0), (intCoords[1][1]*1.0)], [(intCoords[2][0]*1.0), (intCoords[2][1]*1.0)], [(intCoords[3][0]*1.0), (intCoords[3][1]*1.0)]]

		for a16 in range(0,4,1):
			if( vertices[a16][0] == self.centerW):
				vertices[a16][0] += 0.000000001
			if( vertices[a16][1] == self.centerH):
				vertices[a16][1] += 0.000000001

		if(vertices[0][0] < vertices[3][0]):
			vertices[0], vertices[3] = vertices[3], vertices[0]

		if(vertices[1][0] < vertices[2][0]):
			vertices[1], vertices[2] = vertices[2], vertices[1]

		if(vertices[0][0] < vertices[2][0]):
			vertices[0], vertices[2] = vertices[2], vertices[0]

		if(vertices[1][0] < vertices[3][0]):
			vertices[1], vertices[3] = vertices[3], vertices[1]

		if(vertices[0][1] > vertices[1][1]):
			vertices[0], vertices[1] = vertices[1], vertices[0]

		if(vertices[2][1] < vertices[3][1]):
			vertices[2], vertices[3] = vertices[3], vertices[2]
                        
                #print(vertices)
                m1, b1 = self.getEquation(vertices[0], vertices[2])
		m2, b2 = self.getEquation(vertices[1], vertices[3])
		mH1, bH1 = self.getEquation(vertices[3], vertices[0])
		mH2, bH2 = self.getEquation(vertices[2], vertices[1])
		mV1, bV1 = self.getEquation(vertices[3], vertices[2])
		mV2, bV2 = self.getEquation(vertices[0], vertices[1])

		rectCenterX, rectCenterY = self.intersectLines(m1, b1, m2, b2)

		horizontalVector = [0, (self.getCameraXCoord(vertices[0][0]) - self.getCameraXCoord(vertices[3][0])), (self.getCameraYCoord(vertices[0][1]) - self.getCameraYCoord(vertices[3][1])) ]
		verticalVector = [0, (self.getCameraXCoord(vertices[3][0]) - self.getCameraXCoord(vertices[2][0])),  (self.getCameraYCoord(vertices[3][1]) - self.getCameraYCoord(vertices[2][1])) ]

		if (mH1 != mH2):
                        #print "full vertical vector"
			horizontalVanishingPointX, horizontalVanishingPointY = self.intersectLines(mH1, bH1, mH2, bH2)
			horizontalVanishingPointXDist = self.getCameraXCoord( horizontalVanishingPointX )
			horizontalVanishingPointYDist = self.getCameraYCoord( horizontalVanishingPointY )

			if horizontalVanishingPointXDist > 0:
				horizontalVector = [self.focalLength, horizontalVanishingPointXDist, horizontalVanishingPointYDist]

			if horizontalVanishingPointXDist < 0:
				horizontalVector = [0-self.focalLength, 0-horizontalVanishingPointXDist, 0-horizontalVanishingPointYDist]

		if (mV1 != mV2):
                        #print "full horizontal vector"
			verticalVanishingPointX, verticalVanishingPointY = self.intersectLines(mV1, bV1, mV2, bV2)
			verticalVanishingPointXDist = self.getCameraXCoord( verticalVanishingPointX )
			verticalVanishingPointYDist = self.getCameraYCoord( verticalVanishingPointY )
			
			if verticalVanishingPointYDist > 0:
				verticalVector = [self.focalLength, verticalVanishingPointXDist, verticalVanishingPointYDist]

			if verticalVanishingPointYDist < 0:
				verticalVector = [0-self.focalLength, 0-verticalVanishingPointXDist, 0-verticalVanishingPointYDist]
		
		#print "horizontal raw", horizontalVector
		#print "vertical raw", verticalVector

		horizontalMagnitude = math.sqrt(math.pow(horizontalVector[0], 2) + math.pow(horizontalVector[1], 2) + math.pow(horizontalVector[2], 2))
		verticalMagnitude = math.sqrt(math.pow(verticalVector[0], 2) + math.pow(verticalVector[1], 2) + math.pow(verticalVector[2], 2))
		
		horizontalIRLVector = [(horizontalVector[0] * (self.targetWidth/horizontalMagnitude)), (horizontalVector[1] * (self.targetWidth/horizontalMagnitude)), (horizontalVector[2] * (self.targetWidth/horizontalMagnitude))]
		verticalIRLVector = [(verticalVector[0] * (self.targetHeight/verticalMagnitude)), (verticalVector[1] * (self.targetHeight/verticalMagnitude)), (verticalVector[2] * (self.targetHeight/verticalMagnitude))]

		#print "horizontal", horizontalIRLVector
		#print "vertical", verticalIRLVector, "\n"

		upperRightVector = [self.focalLength, (self.getCameraXCoord(vertices[0][0]*1.0)), (self.getCameraYCoord(vertices[0][1]*1.0))]
		lowerRightVector = [self.focalLength, (self.getCameraXCoord(vertices[1][0]*1.0)), (self.getCameraYCoord(vertices[1][1]*1.0))]
		lowerLeftVector = [self.focalLength, (self.getCameraXCoord(vertices[2][0]*1.0)), (self.getCameraYCoord(vertices[2][1]*1.0))]
		upperLeftVector = [self.focalLength, (self.getCameraXCoord(vertices[3][0]*1.0)), (self.getCameraYCoord(vertices[3][1]*1.0))]

		#print "0-div check", upperLeftVector
		#print "0-div check", lowerRightVector
		
		lowerLeftScalar1 = 0
		if (upperLeftVector[1] != 0):
			lowerLeftScalar1 = (((upperLeftVector[2]/upperLeftVector[1])*verticalIRLVector[1]) - verticalIRLVector[2]) / (lowerLeftVector[2] - ((upperLeftVector[2]/upperLeftVector[1])*lowerLeftVector[1]))

		lowerLeftScalar2 = 0
		if (lowerRightVector[1] != 0):
			lowerLeftScalar2 = (((lowerRightVector[2]/lowerRightVector[1])*horizontalIRLVector[1]) - horizontalIRLVector[2]) / (lowerLeftVector[2] - ((lowerRightVector[2]/lowerRightVector[1])*lowerLeftVector[1]))

		lowerLeftScalar = (lowerLeftScalar1 + lowerLeftScalar1)/2
		if (upperLeftVector[1] == 0):
			lowerLeftScalar = lowerLeftScalar2

		if (lowerRightVector[1] == 0):
			lowerLeftScalar = lowerLeftScalar1
		
		if ((lowerLeftScalar2 - lowerLeftScalar2) > self.acceptableError):
			accurate = False
			print "start value check", lowerLeftScalar1 - lowerLeftScalar2

		aL = self.crossProduct(lowerLeftVector, upperLeftVector)
		nL = (verticalIRLVector[0]*aL[0] + verticalIRLVector[1]*aL[1] + verticalIRLVector[2]*aL[2])
		scaleL = nL / (math.pow(aL[0],2) + math.pow(aL[1],2) + math.pow(aL[2],2))
		separationL = [(scaleL*aL[0]), (scaleL*aL[1]), (scaleL*aL[2])]

		offsetL = [(verticalIRLVector[0] + separationL[0]), (verticalIRLVector[1] + separationL[1]), (verticalIRLVector[2] + separationL[2])]

		qL1 = self.getFirstScalar(offsetL, lowerLeftVector, upperLeftVector)
		qL2 = self.getSecondScalar(offsetL, qL1, lowerLeftVector, upperLeftVector)


		aU = self.crossProduct(lowerLeftVector, lowerRightVector)
		nU = (horizontalIRLVector[0]*aU[0] + horizontalIRLVector[1]*aU[1] + horizontalIRLVector[2]*aU[2])
		scaleU = nU / (math.pow(aU[0],2) + math.pow(aU[1],2) + math.pow(aU[2],2))
		separationU = [(scaleU*aU[0]), (scaleU*aU[1]), (scaleU*aU[2])]

		offsetU = [(horizontalIRLVector[0] + separationU[0]), (horizontalIRLVector[1] + separationU[1]), (horizontalIRLVector[2] + separationU[2])]

		qU1 = self.getFirstScalar(offsetU, lowerLeftVector, lowerRightVector)
		qU2 = self.getSecondScalar(offsetU, qU1, lowerLeftVector, lowerRightVector)


		aR = self.crossProduct(lowerRightVector, upperRightVector)
		nR = (verticalIRLVector[0]*aR[0] + verticalIRLVector[1]*aR[1] + verticalIRLVector[2]*aR[2])
		scaleR = nR / (math.pow(aR[0],2) + math.pow(aR[1],2) + math.pow(aR[2],2))
		separationR = [(scaleR*aR[0]), (scaleR*aR[1]), (scaleR*aR[2])]

		offsetR = [(verticalIRLVector[0] + separationR[0]), (verticalIRLVector[1] + separationR[1]), (verticalIRLVector[2] + separationR[2])]

		qR1 = self.getFirstScalar(offsetR, lowerRightVector, upperRightVector)
		qR2 = self.getSecondScalar(offsetR, qR1, lowerRightVector, upperRightVector)


		aT = self.crossProduct(upperLeftVector, upperRightVector)
		nT = (horizontalIRLVector[0]*aT[0] + horizontalIRLVector[1]*aT[1] + horizontalIRLVector[2]*aT[2])
		scaleT = nT / (math.pow(aT[0],2) + math.pow(aT[1],2) + math.pow(aT[2],2))
		separationT = [(scaleT*aT[0]), (scaleT*aT[1]), (scaleT*aT[2])]

		offsetT = [(horizontalIRLVector[0] + separationT[0]), (horizontalIRLVector[1] + separationT[1]), (horizontalIRLVector[2] + separationT[2])]

		qT1 = self.getFirstScalar(offsetT, upperLeftVector, upperRightVector)
		qT2 = self.getSecondScalar(offsetT, qT1, upperLeftVector, upperRightVector)

		qTR = (qR2 + qT2)/2
		qUR = (qU2 + qR1)/2
		qUL = (qL1 + qU1)/2
		qTL = (qL2 + qT1)/2

		qTRError = (qR2 - qT2)
		qURError = (qU2 - qR1)
		qULError = (qL1 - qU1)
		qTLError = (qL2 - qT1)

		upperRightIRLVector = [(upperRightVector[0]*qTR), (upperRightVector[1]*qTR), (upperRightVector[2]*qTR)]
		lowerRightIRLVector = [(lowerRightVector[0]*qUR), (lowerRightVector[1]*qUR), (lowerRightVector[2]*qUR)]
		lowerLeftIRLVector = [(lowerLeftVector[0]*qUL), (lowerLeftVector[1]*qUL), (lowerLeftVector[2]*qUL)]
		upperLeftIRLVector = [(upperLeftVector[0]*qTL), (upperLeftVector[1]*qTL), (upperLeftVector[2]*qTL)]

		upperRightIRLVector2 = [(upperRightVector[0]*qT2), (upperRightVector[1]*qT2), (upperRightVector[2]*qT2)]
		lowerRightIRLVector2 = [(lowerRightVector[0]*qU2), (lowerRightVector[1]*qU2), (lowerRightVector[2]*qU2)]
		lowerLeftIRLVector2 = [(lowerLeftVector[0]*qU1), (lowerLeftVector[1]*qU1), (lowerLeftVector[2]*qU1)]
		upperLeftIRLVector2 = [(upperLeftVector[0]*qT1), (upperLeftVector[1]*qT1), (upperLeftVector[2]*qT1)]

		upperLeftScalar = ((lowerLeftScalar*lowerLeftVector[2]) + verticalIRLVector[2])/upperLeftVector[2]
		#if ((lowerLeftVector[0]*lowerLeftScalar + verticalIRLVector[0]) - (upperLeftVector[0]*upperLeftScalar) > self.acceptableError):
		#	accurate = False
		#	print "vertical1", ((lowerLeftVector[0]*lowerLeftScalar + verticalIRLVector[0]) - (upperLeftVector[0]*upperLeftScalar))

		#print "scalarCheck", lowerLeftScalar-qL1, "\n", upperLeftScalar-qL2

		#print "vertical1a", ((lowerLeftVector[0]*qL1 + verticalIRLVector[0]) - (upperLeftVector[0]*qL2))
		#print "horizontal1a", ((lowerLeftVector[0]*qU1 + horizontalIRLVector[0]) - (lowerRightVector[0]*qU2))
		#print "vertical2a", ((lowerRightVector[0]*qR1 + verticalIRLVector[0]) - (upperRightVector[0]*qR2))
		#print "horizontal2a", ((upperLeftVector[0]*qT1 + horizontalIRLVector[0]) - (upperRightVector[0]*qT2))

		lowerRightScalar = ((lowerLeftScalar*lowerLeftVector[2]) + horizontalIRLVector[2])/lowerRightVector[2]
		#if ((lowerLeftVector[1]*lowerLeftScalar + horizontalIRLVector[1]) - (lowerRightVector[1]*lowerRightScalar) > self.acceptableError):
		#	accurate = False
		#	print "horizontal1", ((lowerLeftVector[1]*lowerLeftScalar + horizontalIRLVector[1]) - (lowerRightVector[1]*lowerRightScalar))

		upperRightScalar = ((upperLeftScalar*upperLeftVector[2]) + horizontalIRLVector[2])/upperRightVector[2]
		#if ((upperLeftVector[1]*upperLeftScalar + horizontalIRLVector[1]) - (upperRightVector[1]*upperRightScalar) > self.acceptableError):
		#	accurate = False
		#	print "horizontal2", ((upperLeftVector[1]*upperLeftScalar + horizontalIRLVector[1]) - (upperRightVector[1]*upperRightScalar))

		upperRightScalarCheck = ((lowerRightScalar*lowerRightVector[2]) + verticalIRLVector[2])/upperRightVector[2]
		#if ((lowerRightVector[1]*lowerRightScalar + verticalIRLVector[1]) - (upperRightVector[1]*upperRightScalarCheck) > self.acceptableError):
		#	accurate = False
		#	print "vertical2", ((lowerRightVector[1]*lowerRightScalar + verticalIRLVector[1]) - (upperRightVector[1]*upperRightScalarCheck))		

		#upperRightIRLVector = [(upperRightVector[0]*upperRightScalar), (upperRightVector[1]*upperRightScalar), (upperRightVector[2]*upperRightScalar)]
		#lowerRightIRLVector = [(lowerRightVector[0]*lowerRightScalar), (lowerRightVector[1]*lowerRightScalar), (lowerRightVector[2]*lowerRightScalar)]
		#lowerLeftIRLVector = [(lowerLeftVector[0]*lowerLeftScalar), (lowerLeftVector[1]*lowerLeftScalar), (lowerLeftVector[2]*lowerLeftScalar)]
		#upperLeftIRLVector = [(upperLeftVector[0]*upperLeftScalar), (upperLeftVector[1]*upperLeftScalar), (upperLeftVector[2]*upperLeftScalar)]

		#if((upperRightScalar - upperRightScalarCheck) > self.acceptableError):
		#	accurate = False
		#	print "meeting point check", ((upperRightScalar - upperRightScalarCheck))

		#print upperRightIRLVector
		#print lowerRightIRLVector
		#print lowerLeftIRLVector
		#print upperLeftIRLVector

		distanceToCenter = ((upperRightIRLVector[0] + lowerRightIRLVector[0] + lowerLeftIRLVector[0] + upperLeftIRLVector[0])/4)

		leftMidpoint = [(upperLeftIRLVector2[0] + lowerLeftIRLVector2[0])/2, (upperLeftIRLVector2[1] + lowerLeftIRLVector2[1])/2, (upperLeftIRLVector2[2] + lowerLeftIRLVector2[2])/2]
		rightMidpoint = [(upperRightIRLVector2[0] + lowerRightIRLVector2[0])/2, (upperRightIRLVector2[1] + lowerRightIRLVector2[1])/2, (upperRightIRLVector2[2] + lowerRightIRLVector2[2])/2]
		
		#horizontalAngle = 90.0 - math.degrees(math.atan2(math.hypot((leftMidpoint[1]-rightMidpoint[1]), (leftMidpoint[2]-rightMidpoint[2])), (leftMidpoint[0]-rightMidpoint[0])))

		horizontalAngle = 90.0 - math.degrees(math.atan2((rightMidpoint[1]-leftMidpoint[1]), (leftMidpoint[0]-rightMidpoint[0])))

		# print distanceToCenter

		# print "horizontal angle", horizontalAngle

		vertices3D = [upperRightIRLVector, lowerRightIRLVector, lowerLeftIRLVector, upperLeftIRLVector]
		verticesT3D = self.transformCoordinates(vertices3D, armAngle)
		targetPosition = self.getTargetPosition(verticesT3D)
		angleToTargetPosition = math.degrees(math.atan2((targetPosition[1]), targetPosition[0]))
		distanceToTargetPosition = math.hypot(targetPosition[0], targetPosition[1])

		#print accurate
		#return vertices3D

		#print accurate, distanceToCenter, horizontalAngle, distanceToTargetPosition, angleToTargetPosition, [qTRError, qURError, qULError, qTLError]

                return accurate, distanceToCenter, horizontalAngle, distanceToTargetPosition, angleToTargetPosition, [qTRError, qURError, qULError, qTLError]
		
		#robotPivotUpperRightVector = [(upperRightIRLVector[0] + self.armLength), (upperRightIRLVector[1]), (upperRightIRLVector[2] + self.armHeight)]
		#robotPivotLowerRightVector = [(lowerRightIRLVector[0] + self.armLength), (lowerRightIRLVector[1]), (lowerRightIRLVector[2] + self.armHeight)]
		#robotPivotLowerLeftVector = [(lowerLeftIRLVector[0] + self.armLength), (lowerLeftIRLVector[1]), (lowerLeftIRLVector[2] + self.armHeight)]
		#robotPivotUpperLeftVector = [(upperLeftIRLVector[0] + self.armLength), (upperLeftIRLVector[1]), (upperLeftIRLVector[2] + self.armHeight)]
		#robotPivotVertices = [
		
		#targetData = [length]
		#return

	def transformCoordinates(self, vertices, angle):
		newVertices = [[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
		for i in range(0,4):
			vertexAngle = math.atan2(vertices[i][2], vertices[i][0]) + math.radians(angle)
			vertexDistance = math.hypot(vertices[i][2], vertices[i][0])
			newVertices[i] = [(math.cos(vertexAngle)*vertexDistance), vertices[i][1], (math.sin(vertexAngle)*vertexDistance)]
		return newVertices

	def getTargetPosition(self, realVertices):
		direction1 = [(realVertices[1][0]-realVertices[3][0]), (realVertices[1][1]-realVertices[3][1]), (realVertices[1][2]-realVertices[3][2])]
		direction2 = [(realVertices[0][0]-realVertices[2][0]), (realVertices[0][1]-realVertices[2][1]), (realVertices[0][2]-realVertices[2][2])]
		#print direction1
		#print direction2
		directionNormal = self.crossProduct(direction1, direction2)
		center = [((realVertices[0][0] + realVertices[1][0] + realVertices[2][0] + realVertices[3][0])/4), ((realVertices[0][1] + realVertices[1][1] + realVertices[2][1] + realVertices[3][1])/4), ((realVertices[0][2] + realVertices[1][2] + realVertices[2][2] + realVertices[3][2])/4)]
		normalScaleLength = self.hypot3D(directionNormal[0], directionNormal[1], directionNormal[2])
		scalar = 0-(self.desiredDistance/normalScaleLength)
		translation = [(directionNormal[0]*scalar), (directionNormal[1]*scalar), (directionNormal[2]*scalar)]
		targetPosition = [(center[0] + translation[0]), (center[1] + translation[1]), (center[2] + translation[2])]
		#print targetPosition, "\n"
		#print directionNormal, "\n"
		#print "dot product 1 ", self.dotProduct(direction1, directionNormal)
		#print "dot product 2 ", self.dotProduct(direction2, directionNormal)
		a12 = self.hypot3D(center[0], center[1], center[2])
		b12 = self.hypot3D(targetPosition[0], targetPosition[1], targetPosition[2])
		c12 = self.hypot3D((center[0] - targetPosition[0]), (center[1] - targetPosition[1]), (center[2] - targetPosition[2]))
		#print a12, b12, c12
		return targetPosition

	def getAngleToCentralX(self, centerX):
		return(math.degrees(math.atan2((centerX - self.centerW), self.focalLength)))

	def getEquation(self, point0, point1):
		m = 1000000000
		if (point0[0] != point1[0]):
			m = (point0[1] - point1[1])/(point0[0]-point1[0])
		b = point0[1] - (m * point0[0])
		return([m,b])
	
	def getEquationFromSlope(self, point0, slope):
		m = slope
		b = point0[1] - (m * point0[0])
		return([m,b])

	def intersectLines(self, m1, b1, m2, b2):
		xCoord = (b1 - b2)/(m2 - m1)
		yCoord = (b1 + (m1 * xCoord))
		return(xCoord, yCoord)

	def getFirstScalar(self, translation, vector1, vector2):

		return((((vector2[2]/vector2[1])*translation[1]) - translation[2]) / (vector1[2] - ((vector2[2]/vector2[1])*vector1[1])))

	def getSecondScalar(self, translation, scalar1, vector1, vector2):

		return(((scalar1*vector1[2]) + translation[2])/vector2[2])

	def crossProduct(self, vector1, vector2):
		#print "(", vector1[1], "*", vector2[2], ") - (", vector1[2], "*", vector2[1], ") = ", ((vector1[1]*vector2[2]) - (vector1[2]*vector2[1]))
		return([((vector1[1]*vector2[2]) - (vector1[2]*vector2[1])), (vector1[2]*vector2[0] - vector1[0]*vector2[2]), (vector1[0]*vector2[1] - vector1[1]*vector2[0])])

	def dotProduct(self, vector1, vector2):
		return((vector1[0]*vector2[0]) + (vector1[1]*vector2[1]) + (vector1[2]*vector2[2]))

	def getCameraXCoord(self, xPixels):
		return xPixels - self.centerW

	def getCameraYCoord(self, yPixels):
		return self.centerH - yPixels

	def hypot3D(self, x, y, z):
		return(math.sqrt(math.pow(x, 2) + math.pow(y, 2) + math.pow(z, 2)))

#trig = vertexMath(720, 1080, 1116, 7.65625, 3.828125)
#trig.getVertexData([[110.0,641.0],[155.0,255.0],[897.0,295.0],[894.0,696.0]])

#targetTrig = vertexMath(640, 480, 732, 20.0, 14.0)
#targetTrig.getVertexData([[340,226],[340,254],[300,254],[300,226]])
#targetTrig.getVertexData([[467, 252], [471, 371], [279, 365], [292, 252]])
#targetTrig.getAngleToCentralX(320-732)