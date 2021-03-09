import ROOT as root 
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.cm as cmx
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

from detector import Detector
import physics


class Visualizer:
	DrawMomentum = True

	writeDirectory = "../plots/"

	trackPtSize = 2

	def __init__(self):
		print("Hi I'm a Visualizer")
		self.fig = plt.figure()
		self.ax = Axes3D(self.fig)
	
		

	def AddTrack(self, track):
		self.liveTracks.append(track)

	def AddPoint(self, point):
		self.displayPoints.append(point)

	def DetectorDisplay(self):
		det = Detector()
		xLims = det.xLims()
		zLims = det.zLims()

		
		self.ax.set_xlim(xLims[0], xLims[1])
		self.ax.set_ylim(det.yLims()[0], det.yLims()[1])
		self.ax.set_zlim(zLims[0], zLims[1])

		#constructing each layer for Poly3DCollection class

		layerX = [xLims[0], xLims[0], xLims[1], xLims[1]]
		layerZ = [zLims[0], zLims[1], zLims[1], zLims[0]]

		cols = []
		
		for layerN in range(det.numLayers()):
			layerY = [det.LayerYMid(layerN) for x in range(len(layerX))]
			verts = [list(zip(layerX, layerY, layerZ))]
			cols.append(Poly3DCollection(verts, alpha=0.20))
			cols[layerN].set_facecolor(det.DrawColor())
			self.ax.add_collection3d(cols[layerN])
		
		return det

	def TrackDisplay(self, ListOf_trackPtLists, Listof_colors, list_of_labels=None):
		xs, ys, zs, cs = [], [], [], []
		scatters = []
		for n, trackPtList in enumerate(ListOf_trackPtLists):
			xs += [trackPt.x for trackPt in trackPtList]
			ys += [trackPt.y for trackPt in trackPtList]
			zs += [trackPt.z for trackPt in trackPtList]
			cs += [Listof_colors[n] for trackPt in trackPtList]
			scatters.append(self.ax.scatter(xs, ys, zs, c=cs[n][0], s=self.trackPtSize, label=list_of_labels[n]))
			xs, ys, zs, cs = [], [], [], []
		self.ax.set_xlabel("x [cm]")
		self.ax.set_ylabel("y [cm]")
		self.ax.set_zlabel("z [cm]")
		self.ax.legend(markerscale=3, loc=2)
		

	def Draw(self):
		self.DetectorDisplay()
		plt.show()

    	




