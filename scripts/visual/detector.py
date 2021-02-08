##################################################################################################
##################################################################################################

#THIS FILE CONTAINS DETECTOR GEOMETRY INFORMATION#

##################################################################################################

class Detector:

	BoxLimits = [  [-5000.0, 5000.0],  [6000.0, 8917.0],  [7000.0, 17000.0]    ]
	LayerYLims = [ [6001., 6004.],  [6104., 6107.], [8001., 8004.], [8104., 8107.], [8501., 8504.], [8604., 8607.], [8707., 8710.], [8810., 8813.], [8913., 8916.]  ]

	#               x range              y range             z range
	
	def __init__(self):
		print("Detector Constructed")

	def xLims(self):
		return self.BoxLimits[0]
	
	def yLims(self):
		return self.BoxLimits[1]
	
	def zLims(self):
		return self.BoxLimits[2]

	def LayerY(self, n):
		return self.LayerYLims[n]

	def LayerYMid(self, n):
		return (self.LayerYLims[n][0] + self.LayerYLims[n][1])/2.

	def nLayers(self):
		return len(self.LayerYLims)

	def DrawColor(self):
		return "tab:gray"

	def inLayer(self, yVal):
		for layerN, layerLims in enumerate(self.LayerYLims):
			if yVal > layerLims[0] and yVal < layerLims[1]:
				return layerN
		return -1

	def inLayer_w_Error(self, yVal, yErr):
		for layerN, layerLims in enumerate(self.LayerYLims):

			lower = yVal - yErr
			upper = yVal + yErr

			if lower < layerLims[0] and upper > layerLims[1]:
				return layerN

			if lower < layerLims[0] and upper > layerLims[0]:
				return layerN

			if lower < layerLims[1] and upper > layerLims[1]:
				return layerN


		return -1

	def inBox(self, x, y, z):
		if x > self.xLims[0] and x < self.xLims[1]:
			if y > self.yLims[0] and y < self.yLims[1]:
				if z > self.zLims[0] and z < self.zLims[1]:
					return True
		return False

	
	#determine number of layers a track goes through
	def nLayers(self, x0, y0, z0, vx, vy, vz):
		count = 0
		for n in range(len(self.LayerYLims)):
			layerY = self.LayerYMid(n)
			if (layerY-y0)/vy < 0:
				continue
			else:
				dt = (layerY - y0)/vy

				x1 = x0 + dt*vx
				z1 = y0 + dt*vz

				if inBox(x1, layerY, z1):
					count += 1

		return count		
