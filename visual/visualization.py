import ROOT as root 
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.cm as cmx
from mpl_toolkits.mplot3d import Axes3D
import physics


output_dir = "../plots/"



def scatter3d(xs,ys,zs, cs, arg_s, styles, title, write_name,  points=[], colorsMap='jet'):
    cm = plt.get_cmap(colorsMap)
    cNorm = matplotlib.colors.Normalize(vmin=min(cs[0]), vmax=max(cs[0]))
    scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=cm)
    fig = plt.figure()
    ax = Axes3D(fig)
    for n in range(len(xs)):
   		ax.scatter(xs[n], ys[n], zs[n], s=arg_s[n], c=scalarMap.to_rgba(cs[n]), marker=styles[n])

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

	point_style = "o"
	special_point_style = "*"

	def __init__(self):
		self.tracks = []
		self.points = []
		self.special_points = []
		self.styles = []

	def AddTrack(self, x0, y0, z0, vx, vy, vz, t0):
		self.tracks.append(physics.Track(x0, y0, z0, vx, vy, vz, t0))

	def AddPoint(self, point, style="o"):
		if style == "o":
			self.points.append(point)
			self.styles.append(style)
		else:
			self.special_points.append(point)
			self.special_point_style = style
	
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
		draw_style = []
		
		for track_n in range(len(self.tracks)):
			tx, ty, tz, tt = self.tracks[track_n].timed_points()
			draw_x.append(tx)
			draw_y.append(ty)
			draw_z.append(tz)
			draw_t.append(tt)
			draw_s.append(1) 
			draw_style.append(".") 

		_x, _y, _z, _t = [], [], [], []

		for point_n in range(len(self.points)):
			
			_x.append(self.points[point_n][0])
			_y.append(self.points[point_n][1])
			_z.append(self.points[point_n][2])
			_t.append(self.points[point_n][3])

		draw_s.append(20)
		draw_style.append(self.point_style)

		draw_x.append(_x)
		draw_y.append(_y)
		draw_z.append(_z)
		draw_t.append(_t)

		_x, _y, _z, _t = [], [], [], []

		for point_n in range(len(self.special_points)):
			
			_x.append(self.special_points[point_n][0])
			_y.append(self.special_points[point_n][1])
			_z.append(self.special_points[point_n][2])
			_t.append(self.special_points[point_n][3])

		draw_s.append(20)
		draw_style.append(self.special_point_style)

		draw_x.append(_x)
		draw_y.append(_y)
		draw_z.append(_z)
		draw_t.append(_t)

		scatter3d( draw_x, draw_y, draw_z, draw_t, draw_s, draw_style, title, name)




















