import visualization
import physics
import ROOT as root 
import numpy as np
import detector
import os
from time import time

det = detector.Detector()


#base_dir = "/cms/seg188/eos/mathusla/output/w"
base_dir = "/home/stephen/hex/mathusla_all/ml_tracker/tracker_files/feb2/w/"
files = []
for file in os.listdir(base_dir):
	if file.endswith(".root"):
		files.append(base_dir + "/" + file)

ncuts = 8

store = [0, 0, 0, 0, 0, 0, 0, 0]
real_total = 0.0

store_total = 0.
for i in range(len(files)):

	file = files[i]
	print(file)
	tracking_file = root.TFile.Open(file)
	tree = tracking_file.Get("integral_tree")
	if (not tree):
		continue

	#tree.SetBranchStatus("*", 0)
	tree.SetBranchStatus("Digi_x", 1)
	tree.SetBranchStatus("Digi_y", 1)
	tree.SetBranchStatus("NumTracks", 1)
	tree.SetBranchStatus("NumVertices", 1)
	tree.SetBranchStatus("Vertex_x", 1)
	tree.SetBranchStatus("Vertex_y", 1)
	tree.SetBranchStatus("Vertex_z", 1)
	tree.SetBranchStatus("Vertex_t", 1)
	tree.SetBranchStatus("Vertex_ErrorY", 1)
	tree.SetBranchStatus("Vertex_ErrorT", 1)
	tree.SetBranchStatus("Track_velX", 1)
	tree.SetBranchStatus("Track_velY", 1)
	tree.SetBranchStatus("Track_velZ", 1)
	tree.SetBranchStatus("Track_x0", 1)
	tree.SetBranchStatus("Track_y0", 1)
	tree.SetBranchStatus("Track_z0", 1)
	tree.SetBranchStatus("Track_t0", 1)
	tree.SetBranchStatus("Track_missingHitLayer", 1)
	tree.SetBranchStatus("track_ipDistance", 1)

	passed = [0.0 for n in range(ncuts)]

	total = 0.0

	start_time = time()

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

		if not det.inBox(vtxx, vtxy, vtxz):
			continue

		passed[2] += 1.0

		#cut 4 -- no hits in bottom layer
		veto = False
		for hity in tree.Digi_y:
			if det.inLayer(hity) < 2:
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


		##track in same layer cut
		track_hit_yvals = [ [] for i in range(len(tree.Track_x0))]
		trackn = 0
		for hitn in tree.Track_hitIndices:
			if hitn == -1:
				trackn += 1
			else:
				track_hit_yvals[trackn].append(tree.Digi_y[hitn])

		min_layers = [ det.inLayer(min(yvals_list)) for yvals_list in track_hit_yvals ]

		veto = False

		start = min_layers[0]

		for minval in min_layers:
			if not minval==start:
				veto = True
				break
		if veto:
			continue


		passed[7] += 1.

		continue

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

	total_time = time() - start_time
	print("total time: " + str(total_time))

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





		













