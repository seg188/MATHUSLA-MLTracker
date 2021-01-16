import visualization
import physics
import ROOT as root 

LAYERS_Y=[[6001.0, 6004.0],  [6104.0, 6107.0]]
 												 	

box_lims = [[-5000., 5000.], [5900.0, 9000.0], [6900., 17100.]]

def inside_box(x, y, z):
	if box_lims[0][0] < x and box_lims[0][1] > x:
		if box_lims[1][0] < y and box_lims[1][1] > y:
			if box_lims[2][0] < z and box_lims[2][1] > z:
				return True

	return False

tracking1_file_name = "../tracker_files/w/statistics0.root" 
tracking2_file_name = "../tracker_files/w/statistics1.root"



total_passed_cuts = 0

def in_layer(y_val):
	for n in range(len(LAYERS_Y)):
		_min = LAYERS_Y[n][0]
		_max = LAYERS_Y[n][1]
		if (y_val > _min) and (y_val < _max):
			return n 

	return 99

store = [0, 0, 0, 0, 0, 0, 0]
real_total = 0.0

files = [tracking1_file_name, tracking2_file_name]#], tracking3_file_name, tracking4_file_name]
plots = [root.TH1D("file1", "cutflow", 6, 0.5, 6.5), root.TH1D("file2", "cutflow", 6, 0.5, 6.5), root.TH1D("file3", "cutflow", 6, 0.5, 6.5), root.TH1D("file4", "cutflow", 5, 0.5, 5.5)]

c1 = root.TCanvas("c1")
for i in range(len(files)):

	file = files[i]
	tracking_file = root.TFile.Open(file)
	tree = tracking_file.Get("integral_tree")

	passed = [0, 0, 0, 0, 0, 0, 0]
	total = 0.0
	for event_number in range(int(tree.GetEntries())):
		total += 1.0
		real_total += 1.
		passed[0] += 1
		tree.GetEntry(event_number)

	#we can add some cuts here if we would like
		if (tree.NumTracks < 2):
			continue

		passed[1] += 1


		if not (tree.NumVertices >= 1):
			continue


		passed[2] += 1

		bottom_layer = False
		for hitn in range(len(tree.Digi_y)):
			y_ind = in_layer(tree.Digi_y[hitn])
			if y_ind < 2:
				bottom_layer = True
				continue

		if bottom_layer:
			continue

		passed[3] += 1

		## expected hits in bottom layer!!!
		## 
		
		close_to_ip = False
		for n in range(len(tree.track_ipDistance)):
			if (tree.track_ipDistance[n] < 350.):
				close_to_ip = True

		if close_to_ip:
			continue

		passed[4] += 1
		

		expect_hit = False
		for trn in range(len(tree.Track_x0)):
			dy = 6510.0 - tree.Track_y0[trn] 
			x1 = tree.Track_velX[trn]*dy/tree.Track_velY[trn] + tree.Track_x0[trn]
			z1 = tree.Track_velZ[trn]*dy/tree.Track_velY[trn] + tree.Track_z0[trn]
			if inside_box(x1, 6107.0, z1):
				expect_hit = True
				continue

		if not expect_hit:
			continue


		passed[5] += 1
	

		

	


	#if tree.Vertex_cosOpeningAngle[0] < 0.93:
	#	continue

	print(file)
	print(total)
	print(passed)
	print([x/total for x in passed])
	
#	print("********")
#	print(real_total)

	for kk in range(len(passed)):
		store[kk] += passed[kk]

#	print([x/real_total for x in store])

	for j in range(len(passed)):
		plots[i].SetBinContent(j+1, float(passed[j])/total)
	plots[i].SetLineColor(50+2*i)
	plots[i].SetLineWidth(2)
	
	if i == 0:
		plots[i].Draw()
	else:
		plots[i].Draw("SAME")


legend = root.TLegend(0.65, 0.75, 0.98, 0.95)
legend.AddEntry(plots[0], "W sample")
legend.AddEntry(plots[1], "H->aa sample")

legend.Draw("SAME")
c1.SetLogy()
c1.Print("cutflow.png", ".png")


		













