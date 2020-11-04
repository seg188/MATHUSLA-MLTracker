import ROOT as root 
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.cm as cmx
from mpl_toolkits.mplot3d import Axes3D
import physics


output_dir = "../plots/"



def scatter3d(x,y,z, cs, arg_s, title, write_name, points=[], colorsMap='jet'):
    cm = plt.get_cmap(colorsMap)
    cNorm = matplotlib.colors.Normalize(vmin=min(cs), vmax=max(cs))
    scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=cm)
    fig = plt.figure()
    ax = Axes3D(fig)
    ax.scatter(x, y, z, s=arg_s, c=scalarMap.to_rgba(cs))

    ax.set_xlim(physics.box_lims[0][0], physics.box_lims[0][1])
    ax.set_ylim(physics.box_lims[1][0], physics.box_lims[1][1])
    ax.set_zlim(physics.box_lims[2][0], physics.box_lims[2][1])

    ax.set_xlabel('X[cm]')
    ax.set_ylabel('Y[cm]')
    ax.set_zlabel('Z[cm]')
    ax.set_title(title)
    scalarMap.set_array(cs)
    fig.colorbar(scalarMap)
    plt.savefig(output_dir + str(write_name) + ".png")
    plt.close()



class Display:

	def __init__(self):
		self.tracks = []
		self.points = []

	def AddTrack(self, x0, y0, z0, vx, vy, vz, t0):
		self.tracks.append(physics.Track(x0, y0, z0, vx, vy, vz, t0))

	def AddPoint(self, point):
		self.points.append(point)
	
	def AddPoints(self, points):
		self.points += points

	def Draw(self, title, name):
		if len(self.points) == 0 and len(self.tracks) == 0:
			return

		draw_x = []
		draw_y = []
		draw_z = []
		draw_t = []
		draw_s = []
		
		for track_n in range(len(self.tracks)):
			tx, ty, tz, tt = self.tracks[track_n].timed_points()
			draw_x += tx
			draw_y += ty
			draw_z += tz
			draw_t += tt
			draw_s += [1 for i in range(len(tx))] 

		for point_n in range(len(self.points)):
			draw_x.append(self.points[point_n][0])
			draw_y.append(self.points[point_n][1])
			draw_z.append(self.points[point_n][2])
			draw_t.append(self.points[point_n][3])
			draw_s.append(20)

		scatter3d( draw_x, draw_y, draw_z, draw_t, draw_s, title, name)




















