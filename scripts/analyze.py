import ROOT as root 


tracking_file_name = "../build/h/statistics0.root" 
tracking_file = root.TFile.Open(tracking_file_name)
tree = tracking_file.Get("integral_tree")

total_passed_cuts = 0


for event_number in range(int(tree.GetEntries())):
	
	tree.GetEntry(event_number)
	#we can add some cuts here if we would like
	if (tree.NumVertices < 1):
		continue

	if (tree.NumTracks < 2):
		continue
	

	print(event_number)

	_buffer = []
	for val in tree.Digi_hitIndices:
		if not val == -1:
			_buffer.append(val)
		else:
			print(_buffer)
			_buffer = []
	print(_buffer)

	event_display = visualization.Display()

#	for k in range(int(len(tree.Digi_x))):
#		event_display.AddPoint( [tree.Digi_x[k], tree.Digi_y[k], tree.Digi_z[k], tree.Digi_time[k]] )

	event_display.AddPoint( [tree.Vertex_x[0], tree.Vertex_y[0], tree.Vertex_z[0], tree.Vertex_t[0]], "*" )


	for k in range(int(tree.NumTracks)):
		x0, y0, z0, t0 = tree.Track_x0[k], tree.Track_y0[k], tree.Track_z0[k], tree.Track_t0[k]
		vx, vy, vz = tree.Track_velX[k], tree.Track_velY[k], tree.Track_velZ[k]
		event_display.AddTrack(x0, y0, z0, vx, vy, vz, t0)


	event_display.Draw( "event " + str(event_number), "event" + str(event_number) + ".png" )














