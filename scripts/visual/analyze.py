import visualization
import physics
import ROOT as root 

LAYERS_Y=[[6001.0, 6004.0],  [6104.0, 6107.0]]
 												 	

files = ["../tracker_files/w/statistics0.root", "../tracker_files/w/statistics1.root", "../tracker_files/w/statistics2.root" ]


total_passed_cuts = 0
total = 0
def in_layer(y_val):
	for n in range(len(LAYERS_Y)):
		_min = LAYERS_Y[n][0]
		_max = LAYERS_Y[n][1]
		if (y_val > _min) and (y_val < _max):
			return n 

	return 99

for file in files:
	print(file)
	tracking_file = root.TFile.Open(file)
	tree = tracking_file.Get("integral_tree")
	for event_number in range(int(tree.GetEntries())):
		total += 1
	
		tree.GetEntry(event_number)
		#we can add some cuts here if we would like
		if not (tree.NumVertices == 1):
			continue

		if (tree.NumTracks < 2):
			continue

		close_to_ip = False
		for n in range(len(tree.track_ipDistance)):
			if (tree.track_ipDistance[n] < 320.):
				close_to_ip = True

		if close_to_ip:
			continue

		if not (tree.Vertex_numTracks[0] == 2):
			continue


		bottom_layer = False
		for hitn in range(len(tree.Digi_y)):
			y_ind = in_layer(tree.Digi_y[hitn])
			if y_ind < 2:
				bottom_layer = True
				continue

		if bottom_layer:
			continue

	#if tree.Vertex_cosOpeningAngle[0] < 0.93:
	#	continue

		new_missing_hits = []
		for val in tree.Track_missingHitLayer:
			if val > 1:
				new_missing_hits.append(val)


		if len(new_missing_hits) > 3:
			continue

		total_passed_cuts += 1



		print(event_number)
		print(tree.Track_missingHitLayer)

		event_display = visualization.Display()

		for k in range(int(len(tree.Digi_x))):
			event_display.AddPoint( [tree.Digi_x[k], tree.Digi_y[k], tree.Digi_z[k], tree.Digi_time[k]] )

		event_display.AddPoint( [tree.Vertex_x[0], tree.Vertex_y[0], tree.Vertex_z[0], tree.Vertex_t[0]], "*" )


		for k in range(int(tree.NumTracks)):
			x0, y0, z0, t0 = tree.Track_x0[k], tree.Track_y0[k], tree.Track_z0[k], tree.Track_t0[k]
			vx, vy, vz = tree.Track_velX[k], tree.Track_velY[k], tree.Track_velZ[k]
			event_display.AddTrack(x0, y0, z0, vx, vy, vz, t0)


		event_display.Draw( "event " + str(event_number), "event" + str(event_number) + ".png" )
	tracking_file.Close()




print(str(total_passed_cuts) + "/" + str(total) + " passed selection")











