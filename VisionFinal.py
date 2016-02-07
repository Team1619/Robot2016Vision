import math
class vertexMath:
	def __init__(self, height=200, width=200, focalLength=100, targetWidth=5, targetHeight=10, armLength = 2.5, armHeight = 0):
		self.height = height
		self.centerH = height/2
		self.width = width
		self.centerW = width/2
		self.focalLength = focalLength
		self.targetHeight = targetHeight
		self.targetWidth = targetWidth
		self.armLength = armLength
		self.armHeight = armHeight
	
	def setHeight(self, h):
		self.height = h
		self.centerH = h/2
	
	def setWidth(self, w):
		self.width = w
		self.centerW = w/2

	def setFocalLength(self, l):
		self.focalLength = l

	def getVertexData(self, vertices, armAngle=0):

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
			horizontalVanishingPointX, horizontalVanishingPointY = self.intersectLines(mH1, bH1, mH2, bH2)
			horizontalVanishingPointXDist = self.getCameraXCoord( horizontalVanishingPointX )
			horizontalVanishingPointYDist = self.getCameraYCoord( horizontalVanishingPointY )

			if horizontalVanishingPointXDist > 0:
				horizontalVector = [self.focalLength, horizontalVanishingPointXDist, horizontalVanishingPointYDist]

			if horizontalVanishingPointXDist < 0:
				horizontalVector = [0-self.focalLength, 0-horizontalVanishingPointXDist, 0-horizontalVanishingPointYDist]

		if (mV1 != mV2):
			verticalVanishingPointX, verticalVanishingPointY = self.intersectLines(mV1, bV1, mV2, bV2)
			verticalVanishingPointXDist = self.getCameraXCoord( verticalVanishingPointX )
			verticalVanishingPointYDist = self.getCameraYCoord( verticalVanishingPointY )
			
			if verticalVanishingPointYDist > 0:
				verticalVector = [self.focalLength, verticalVanishingPointXDist, verticalVanishingPointYDist]

			if verticalVanishingPointYDist < 0:
				verticalVector = [0-self.focalLength, 0-verticalVanishingPointXDist, 0-verticalVanishingPointYDist]
		
		#print horizontalVector
		#print verticalVector

		horizontalMagnitude = math.sqrt(math.pow(horizontalVector[0], 2) + math.pow(horizontalVector[1], 2) + math.pow(horizontalVector[2], 2))
		verticalMagnitude = math.sqrt(math.pow(verticalVector[0], 2) + math.pow(verticalVector[1], 2) + math.pow(verticalVector[2], 2))
		
		horizontalIRLVector = [(horizontalVector[0] * (self.targetWidth/horizontalMagnitude)), (horizontalVector[1] * (self.targetWidth/horizontalMagnitude)), (horizontalVector[2] * (self.targetWidth/horizontalMagnitude))]
		verticalIRLVector = [(verticalVector[0] * (self.targetHeight/verticalMagnitude)), (verticalVector[1] * (self.targetHeight/verticalMagnitude)), (verticalVector[2] * (self.targetHeight/verticalMagnitude))]

		upperRightVector = [self.focalLength, (self.getCameraXCoord(vertices[0][0])), (self.getCameraYCoord(vertices[0][1]))]
		lowerRightVector = [self.focalLength, (self.getCameraXCoord(vertices[1][0])), (self.getCameraYCoord(vertices[1][1]))]
		lowerLeftVector = [self.focalLength, (self.getCameraXCoord(vertices[2][0])), (self.getCameraYCoord(vertices[2][1]))]
		upperLeftVector = [self.focalLength, (self.getCameraXCoord(vertices[3][0])), (self.getCameraYCoord(vertices[3][1]))]

		lowerLeftScalar = (((upperLeftVector[2]/upperLeftVector[1])*verticalIRLVector[1]) - verticalIRLVector[2]) / (lowerLeftVector[2] - ((upperLeftVector[2]/upperLeftVector[1])*lowerLeftVector[1]))

		upperLeftScalar = ((lowerLeftScalar*lowerLeftVector[1]) + verticalIRLVector[1])/upperLeftVector[1]
		lowerRightScalar = ((lowerLeftScalar*lowerLeftVector[1]) + horizontalIRLVector[1])/lowerRightVector[1]

		upperRightScalar = ((upperLeftScalar*upperLeftVector[1]) + horizontalIRLVector[1])/upperRightVector[1]
		upperRightScalarCheck = ((lowerRightScalar*lowerRightVector[1]) + verticalIRLVector[1])/upperRightVector[1]
		
		upperRightIRLVector = [(upperRightVector[0]*upperRightScalar), (upperRightVector[1]*upperRightScalar), (upperRightVector[2]*upperRightScalar)]
		lowerRightIRLVector = [(lowerRightVector[0]*lowerRightScalar), (lowerRightVector[1]*lowerRightScalar), (lowerRightVector[2]*lowerRightScalar)]
		lowerLeftIRLVector = [(lowerLeftVector[0]*lowerLeftScalar), (lowerLeftVector[1]*lowerLeftScalar), (lowerLeftVector[2]*lowerLeftScalar)]
		upperLeftIRLVector = [(upperLeftVector[0]*upperLeftScalar), (upperLeftVector[1]*upperLeftScalar), (upperLeftVector[2]*upperLeftScalar)]

		print upperRightIRLVector
		print lowerRightIRLVector
		print lowerLeftIRLVector
		print upperLeftIRLVector

		distanceToCenter = ((upperRightIRLVector[0] + lowerRightIRLVector[0] + lowerLeftIRLVector[0] + upperLeftIRLVector[0])/4)

		print distanceToCenter

		#print ((upperRightScalar - upperRightScalarCheck)<0.0000000001)
		#print(upperRightScalar - upperRightScalarCheck)

		if((upperRightScalar - upperRightScalarCheck)>0.000001):
			print "Error in contour geometry"

		vertices3D = [upperRightIRLVector, lowerRightIRLVector, lowerLeftIRLVector, upperLeftIRLVector]
		return vertices3D
		
		#robotPivotUpperRightVector = [(upperRightIRLVector[0] + self.armLength), (upperRightIRLVector[1]), (upperRightIRLVector[2] + self.armHeight)]
		#robotPivotLowerRightVector = [(lowerRightIRLVector[0] + self.armLength), (lowerRightIRLVector[1]), (lowerRightIRLVector[2] + self.armHeight)]
		#robotPivotLowerLeftVector = [(lowerLeftIRLVector[0] + self.armLength), (lowerLeftIRLVector[1]), (lowerLeftIRLVector[2] + self.armHeight)]
		#robotPivotUpperLeftVector = [(upperLeftIRLVector[0] + self.armLength), (upperLeftIRLVector[1]), (upperLeftIRLVector[2] + self.armHeight)]
		#robotPivotVertices = [
		
		#targetData = [length]
		#return
	
	def getEquation(self, point0, point1):
		m = 1000000000
		if (point0[0] != point1[0]):
			m = ((point0[1] - point1[1]) + 0.0)/(point0[0]-point1[0])
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

	def getCameraXCoord(self, xPixels):
		return xPixels - self.centerW

	def getCameraYCoord(self, yPixels):
		return self.centerH - yPixels

#trig = vertexMath()
#trig.getVertexData([[125,50],[125,150],[75,150],[75,50]])
trig2 = vertexMath(720, 1080, 1116, 7.65625, 3.828125)
trig2.getVertexData([[897.0,295.0],[894.0,696.0],[110.0,641.0],[155.0,255.0]])
#1116

targetTrig = vertexMath(720, 1080, 1116, (20.0/12.0), (14.0/12.0))

#targetTrig.getVertexData(dataStream)