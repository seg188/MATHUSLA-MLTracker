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
	