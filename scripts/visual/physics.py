import ROOT as root 
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.cm as cmx
from mpl_toolkits.mplot3d import Axes3D

box_lims = [  [-5000.0, 5000.0],  [5000.0, 10000.0],  [7000.0, 17000.0]    ]


def inside_box(x, y, z):
	if x > box_lims[0][0] and x < box_lims[0][1]:
		if y > box_lims[1][0] and y < box_lims[1][1]:
			if z > box_lims[2][0] and z < box_lims[2][1]:
				return True
	return False


class Track:

	def __init__(self, _x0, _y0, _z0, _vx, _vy, _vz, _t0):
		self.x0 = _x0
		self.y0 = _y0
		self.z0 = _z0
		self.vx = _vx
		self.vy = _vy
		self.vz = _vz
		self.t0 = _t0

	def timed_points(self):
		x, y, z, t = [], [], [], []
		_x, _y, _z, _t = self.x0, self.y0, self.z0, self.t0

		time_spacing = 0.2 #ns
		
		while inside_box(_x, _y, _z):
			x.append(_x)
			y.append(_y)
			z.append(_z)
			t.append(_t)

			_x += self.vx*time_spacing
			_y += self.vy*time_spacing
			_z += self.vz*time_spacing
			_t += time_spacing


		return x, y, z, t

	def untimed_points(self):
		x, y, z, t = [], [], [], []
		_x, _y, _z, _t = self.x0, self.y0, self.z0, 0.0

		time_spacing = 0.2 #ns
		
		while inside_box(_x, _y, _z):
			x.append(_x)
			y.append(_y)
			z.append(_z)
			t.append(_t)

			_x += self.vx*time_spacing
			_y += self.vy*time_spacing
			_z += self.vz*time_spacing

		return x, y, z, t



##################################################################################################
##################################################################################################

#THIS FILE CONTAINS DETECTOR GEOMETRY INFORMATION#

##################################################################################################

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
		if x > self.xLims()[0] and x < self.xLims()[1]:
			if y > self.yLims()[0] and y < self.yLims()[1]:
				if z > self.zLims()[0] and z < self.zLims()[1]:
					return True
		return False

	
	#determine number of layers a track goes through
	def nLayers(self, x0, y0, z0, vx, vy, vz):
		count = 0
		for n in range(len(self.LayerYLims)-2):
			layerY = self.LayerYMid(n+2)
			if (layerY-y0)/vy < 0:
				continue
			else:
				dt = (layerY - y0)/vy

				x1 = x0 + dt*vx
				z1 = y0 + dt*vz

				if self.inBox(x1, layerY, z1):
					count += 1

		return count		

	def closestLayer(self, y):
		dists = [ (y - self.LayerYMid(n+2)) for n in range(len(self.LayerYLims)-2) ]
		above = []
		for d in dists:
			if True:
				above.append( np.absolute(d) )
		if len(above) > 0:		
			return min(above)

		return -1

	def nLayersWHit(self, list_of_hit_y_vals):
		layers = set()

		for y_val in list_of_hit_y_vals:
			layer = self.inLayer(y_val)
			if not (layer < 2 ):
				layers.add(layer)

		return len(layers)

	def LayersWHit(self, list_of_hit_y_vals):
		layers = set()

		for y_val in list_of_hit_y_vals:
			layer = self.inLayer(y_val)
			if not (layer == -1):
				layers.add(layer)
		

		return layers




