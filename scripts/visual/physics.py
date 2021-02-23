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


