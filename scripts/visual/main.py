import visualization
import physics
import ROOT as root 

#/home/ag1378/cmslink/bobthebuilder/new_tracker/samples

LAYERS_Y=[[6001.0, 6004.0],  [6104.0, 6107.0]]
 												 	

box_lims = [[-5000., 5000.], [5900.0, 9000.0], [6900., 17100.]]

def inside_box(x, y, z):
	if box_lims[0][0] < x and box_lims[0][1] > x:
		if box_lims[1][0] < y and box_lims[1][1] > y:
			if box_lims[2][0] < z and box_lims[2][1] > z:
				return True

	return False


tracking_file_name = "../tracker_files/w/stat0.root"
tracking_file = root.TFile.Open(tracking_file_name)
tree = tracking_file.Get("integral_tree")


LAYERS_Y=[[6001.0, 6004.0],  [6104.0, 6107.0]]
 												 	

total_passed_cuts = 0

def in_layer(y_val):
	for n in range(len(LAYERS_Y)):
		_min = LAYERS_Y[n][0]
		_max = LAYERS_Y[n][1]
		if (y_val > _min) and (y_val < _max):
			return n 

	return 99


for event_number in range(int(tree.GetEntries())):
	
	tree.GetEntry(event_number)
	#we can add some cuts here if we would like
	if (tree.NumTracks < 2):
			continue



	if not (tree.NumVertices == 1):
		continue


		

	print(event_number)

	_buffer = []
	for val in tree.Track_missingHitLayer:
		if not val == -1:
			_buffer.append(val)
		else:
			print(_buffer)
			_buffer = []
	print(_buffer)

	event_display = visualization.Display()

	for k in range(int(len(tree.Digi_x))):
		event_display.AddPoint( [tree.Digi_x[k], tree.Digi_y[k], tree.Digi_z[k], tree.Digi_time[k]] )

	event_display.AddPoint( [tree.Vertex_x[0], tree.Vertex_y[0], tree.Vertex_z[0], tree.Vertex_t[0]], "*" )


	for k in range(int(tree.NumTracks)):
		x0, y0, z0, t0 = tree.Track_x0[k], tree.Track_y0[k], tree.Track_z0[k], tree.Track_t0[k]
		vx, vy, vz = tree.Track_velX[k], tree.Track_velY[k], tree.Track_velZ[k]
		event_display.AddTrack(x0, y0, z0, vx, vy, vz, t0)


	event_display.Draw( "event " + str(event_number), "event" + str(event_number) + ".png" )













