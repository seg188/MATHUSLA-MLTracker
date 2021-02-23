import visualization
import physics
import ROOT as root 
import numpy as np
import detector
import os

LAYERS_Y=[[6001.0, 6004.0],  [6104.0, 6107.0]]
 												 	

box_lims = [[-5000., 5000.], [5900.0, 9000.0], [6900., 17100.]]

def inside_box(x, y, z):
	if box_lims[0][0] < x and box_lims[0][1] > x:
		if box_lims[1][0] < y and box_lims[1][1] > y:
			if box_lims[2][0] < z and box_lims[2][1] > z:
				return True

	return False

def in_layer(y_val):
	for n in range(len(LAYERS_Y)):
		_min = LAYERS_Y[n][0]
		_max = LAYERS_Y[n][1]
		if (y_val > _min) and (y_val < _max):
			return n 

	return 999


det = physics.Detector()


base_dir = "/cms/seg188/eos/mathusla/output/w"
#base_dir = "/home/stephen/hex/mathusla_all/ml_tracker/tracker_files/feb2/wc/w/stat0.root"
files = []
for file in os.listdir(base_dir):
	if file.endswith(".root"):
		files.append(base_dir + "/" + file)

w_ey = root.TH1D("wey", "ip assymetry", 100, 0., 10000.0)
h_ey = root.TH1D("hey", "ip assymetry", 100, 0., 10000.0)

ncuts = 8

store = [0, 0, 0, 0, 0, 0, 0, 0]
real_total = 0.0

plots = [root.TH1D("file" + str(n), "cutflow", ncuts, 0.5, ncuts + 0.5) for n in range(len(files))]

store_total = 0.
for i in range(len(files)):

	file = files[i]
	print(file)
	tracking_file = root.TFile.Open(file)
	tree = tracking_file.Get("integral_tree")
	if (not tree):
		continue
	passed = [0.0 for n in range(ncuts)]

	total = 0.0
	for event_number in range(int(tree.GetEntries())):		
		tree.GetEntry(event_number)

		if not (len(tree.Digi_x) > 3):
			continue

		total += 1.0
		#CUT #1-- NEED TO RECONSTRUCT >1 TRACK

		if not (tree.NumTracks > 1):
			continue

		passed[0] += 1.0

		#cut #2 -- NEED TO RECONSTRUCT A VERTEX

		if not (tree.NumVertices > 0):
			continue

		passed[1] += 1.0

		#cut 3-- fiducial volume cut for vertex

		vtxx, vtxy, vtxz = tree.Vertex_x[0], tree.Vertex_y[0], tree.Vertex_z[0]
		evtxy = tree.Vertex_ErrorY[0]

		if not inside_box(vtxx, vtxy, vtxz):
			continue

		passed[2] += 1.0

		#cut 4 -- no hits in bottom layer
		veto = False
		for hity in tree.Digi_y:
			if in_layer(hity) < 2:
				veto = True
		
		if veto:
			continue

		exp_passed = [False for i in range(int(tree.NumTracks))]
		for track_n in range( int(tree.NumTracks) ):
			x0, y0, z0 = tree.Track_x0[track_n], tree.Track_y0[track_n], tree.Track_z0[track_n]
			vx, vy, vz = tree.Track_velX[track_n], tree.Track_velY[track_n], tree.Track_velZ[track_n]
			y2 = det.LayerYMid(1)
			delt1 = (y2-y0)/vy
			exp_x1, exp_z1 = x0 + delt1 * vx, z0 + delt1 * vz

			y1 = det.LayerYMid(0)
			delt0 = (y1-y0)/vy
			exp_x0, exp_z0 = x0 + delt0 * vx, z0 + delt0 * vz

			if det.inSensitiveElement(exp_x1, y2, exp_z1) or det.inSensitiveElement(exp_x0, y1, exp_z0):
				exp_passed[track_n] = True


		for truthVal in exp_passed:
			if truthVal == False:
				veto = True
		if veto:	
			continue

		passed[3] += 1.0


		y1 = (tree.Vertex_y[0] - tree.Track_y0[0])
		e1 = (tree.Vertex_ErrorY[0])
		y2 = (tree.Vertex_y[0] - tree.Track_y0[1])
		e2 = (tree.Vertex_ErrorY[0])

		ydiff = max([y1/e1, y2/e2])

		t1 = (tree.Vertex_t[0] - tree.Track_t0[0])
		e1 = (tree.Vertex_ErrorT[0])
		t2 = (tree.Vertex_t[0] - tree.Track_t0[1])
		e2 = (tree.Vertex_ErrorY[0])

		tdiff = max([t1/e1, t2/e2])


		if max([ydiff, tdiff]) > 0.:
			continue

		passed[4] += 1.0

		##CHECK IF TRACKS ARE MISSING >2 HITS IN LAYERS 9,8,7,6,5
		#if det.inLayer_w_Error(vtxy, 2.*evtxy) >= 0 and evtxy < 100.:
		#	continue

		missing_upper_layers = [ [] for i in range(len(tree.Track_x0))]
		trackn = 0
		for layern in tree.Track_missingHitLayer:
			if layern == -1:
				trackn += 1
			else:
				if layern >= 5:
					missing_upper_layers[trackn].append(layern)

		veto = False

		for mh_list in missing_upper_layers:
			if len(mh_list) > 0:
				veto = True
		if veto:
			continue

		passed[5] += 1.

		if min(tree.track_ipDistance) < 250:
			continue

		passed[6] += 1


		##track beta cut
		track_hit_yvals = [ [] for i in range(len(tree.Track_x0))]
		trackn = 0
		for hitn in tree.Track_hitIndices:
			if hitn == -1:
				trackn += 1
			else:
				track_hit_yvals[trackn].append(tree.Digi_y[hitn])

		min_layers = [ min(yvals_list) for yvals_list in track_hit_yvals ]

		veto = False

		start = min_layers[0]

		for minval in min_layers:
			if not minval==start:
				veto = True
				break
		if veto:
			continue


		passed[7] += 1.

		print("*****event passed!!*****")
		print("file: " + file)
		print("Event number: " + str(event_number) )

		event_display = visualization.Display()

		for k in range(int(len(tree.Digi_x))):
			event_display.AddPoint( [tree.Digi_x[k], tree.Digi_y[k], tree.Digi_z[k], tree.Digi_energy[k]] )

#	event_display.AddPoint( [tree.Vertex_x[0], tree.Vertex_y[0], tree.Vertex_z[0], tree.Vertex_t[0]], "*" )

	
		for k in range(int(tree.NumTracks)):
			x0, y0, z0, t0 = tree.Track_x0[k], tree.Track_y0[k], tree.Track_z0[k], tree.Track_t0[k]
			vx, vy, vz = tree.Track_velX[k], tree.Track_velY[k], tree.Track_velZ[k]
			event_display.AddTrack(x0, y0, z0, vx, vy, vz, t0)


		event_display.Draw_NoTime( "event " + str(event_number), "event" + str(event_number) + ".png" )

		

	print(file)
	print("total events: " + str(total))

	print(passed)
	if total > 0:
		print([x/total for x in passed])

	for i, val in enumerate(passed):
		store[i] += val
	store_total += total

	if store_total > 0:
		print("totals:\n")
		print(store_total)
		print([x/store_total for x in store])

print("************************")
print([store])
print(store_total)
if store_total > 0:
	print([x/store_total for x in store])





		













