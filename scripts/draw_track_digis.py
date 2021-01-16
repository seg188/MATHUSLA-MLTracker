import ROOT as root 
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.cm as cmx
from mpl_toolkits.mplot3d import Axes3D

box_lims = [  [-5000.0, 5000.0],  [5000.0, 10000.0],  [7000.0, 17000.0]    ]

TRACKPOINTSPACING = 1.0	

def scatter3d(x,y,z, cs, tag, points=[], title="hit x,y,z,e", colorsMap='jet'):
    cm = plt.get_cmap(colorsMap)
    cNorm = matplotlib.colors.Normalize(vmin=min(cs), vmax=max(cs))
    scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=cm)
    fig = plt.figure()
    ax = Axes3D(fig)
    ax.scatter(x, y, z, s=10, c=scalarMap.to_rgba(cs))


    ax.set_xlim(-5000., 5000.0)
    ax.set_ylim(-6000.0, 10000.0)
    ax.set_zlim(7000.0, 17000.0)

    ax.set_xlabel('X[cm]')
    ax.set_ylabel('Y[cm]')
    ax.set_zlabel('Z[cm]')
    ax.set_title(title)
    scalarMap.set_array(cs)
    fig.colorbar(scalarMap)
    plt.savefig("../plots/" + str(tag) + ".png")
    plt.close()


def draw_track(hits, track_pts, tag, extra_pts=[]):
	x = []
	y = []
	z = []
	cs = []
	_s =[]
	colorsMap='jet'
	title="hit x,y,z,e with track"
	for k in range(len(track_pts[0])):
		x.append(track_pts[0][k])
		y.append(track_pts[1][k])
		z.append(track_pts[2][k])
		cs.append(-1.0)
		_s.append(2)

	for k in range(len(hits[0])):
		x.append(hits[0][k])
		y.append(hits[1][k])
		z.append(hits[2][k])
		cs.append(hits[3][k])
		_s.append(10)
	
	cm = plt.get_cmap(colorsMap)
	cNorm = matplotlib.colors.Normalize(vmin=min(cs), vmax=max(cs))
	scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=cm)
	fig = plt.figure()
	ax = Axes3D(fig)
	ax.scatter(x, y, z, s=_s, c=scalarMap.to_rgba(cs))
	if len(extra_pts ) > 0:
		ax.scatter(extra_pts[0], extra_pts[1], extra_pts[2], s=25, c='r', marker="*")
    	
	ax.set_xlabel('X[cm]')
	ax.set_ylabel('Y[cm]')
	ax.set_zlabel('Z[cm]')
	ax.set_title(title)
	scalarMap.set_array(cs)
	fig.colorbar(scalarMap)
	plt.savefig("../plots/track_pts/" + str(tag) + ".png")
	plt.close()


def inside_box(x, y, z):
	if (x < box_lims[0][1] and x > box_lims[0][0]) and (y < box_lims[1][1] and y > box_lims[1][0]):
		return (z < box_lims[2][1] and z > box_lims[2][0])

	return False


def track(x0, y0, z0, vx0, vy0, vz0, t0):
	x, y, z = [], [], []
	_x, _y, _z = x0, y0, z0
	enterded_box = False
	max_iter = 10000.0
	j = 0
	norm = np.sqrt(vx0*vx0 + vy0*vy0 + vz0*vz0)
	while ( (inside_box(_x, _y, _z) and enterded_box) or not enterded_box): 
		j += 1
		if inside_box(_x, _y, _z):
			enterded_box = True

		if enterded_box:
			x.append(_x)
			y.append(_y)
			z.append(_z)

		_x = _x + vx0*TRACKPOINTSPACING/norm
		_y = _y + vy0*TRACKPOINTSPACING/norm
		_z = _z + vz0*TRACKPOINTSPACING/norm

		if (j > max_iter) and not enterded_box:
			return [], [], []

	return x, y, z


def truth_track(x0, y0, z0, vx0, vy0, vz0):
	x, y, z = [], [], []
	_x, _y, _z = x0, y0, z0

	print([x0, y0, z0, vx0, vy0, vz0])
	
	norm = np.sqrt(vx0*vx0 + vy0*vy0 + vz0*vz0)

	while(not inside_box(_x, _y, _z)):
		_x = _x + vx0*TRACKPOINTSPACING/norm*10.
		_y = _y + vy0*TRACKPOINTSPACING/norm*10.
		_z = _z + vz0*TRACKPOINTSPACING/norm*10.

		#print(_y)

		if _y > 10000.0:
			break

	while inside_box(_x, _y, _z):
		print("inside box")
		x.append(_x)
		y.append(_y)
		z.append(_z)

		_x = _x + vx0*TRACKPOINTSPACING/norm
		_y = _y + vy0*TRACKPOINTSPACING/norm
		_z = _z + vz0*TRACKPOINTSPACING/norm

	return x, y, z




file_name = "/home/stephen/hex/mathusla_all/ml_tracker/build/statistics0.root"
file = root.TFile.Open(file_name)
tree = file.Get("integral_tree")


for k in range(tree.GetEntries()):
	tree.GetEntry(k)

	digi_index = []
	x_digi, y_digi, z_digi = [], [], []
	e_hit = []

	if tree.NumTracks == 0 or tree.NumTracks == 2:
		continue

	if len(tree.Track_x0) == 0:
		continue

	for j in ((tree.Digi_hitIndices)):
		index = int(j)
		if index < 0:
			continue
		x_digi.append(tree.Digi_x[index])
		y_digi.append(tree.Digi_y[index])
		z_digi.append(tree.Digi_z[index])
		e_hit.append(tree.Digi_energy[j])

	
	x0, y0, z0 = tree.Track_x0[0], tree.Track_y0[0], tree.Track_z0[0]
	vx0, vy0, vz0 = tree.Track_velX[0], tree.Track_velY[0], tree.Track_velZ[0]

	print ([x0, y0, z0])

	trackx, tracky, trackz = track(x0, y0, z0, vx0, vy0, vz0)

	draw_track( [x_digi, y_digi, z_digi, e_hit], [trackx, tracky, trackz], k)









file.Close()