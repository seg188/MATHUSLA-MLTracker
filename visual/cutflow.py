import visualization
import physics
import ROOT as root 

LAYERS_Y=[[6001.0, 6004.0],  [6104.0, 6107.0]]
 												 	

tracking1_file_name = "../tracker_files/w/statistics0.root" 
tracking2_file_name = "../tracker_files/h2/statistics0.root"
tracking3_file_name = "../tracker_files/h5/statistics0.root" 
tracking4_file_name = "../tracker_files/h10/statistics0.root"  


total_passed_cuts = 0

def in_layer(y_val):
	for n in range(len(LAYERS_Y)):
		_min = LAYERS_Y[n][0]
		_max = LAYERS_Y[n][1]
		if (y_val > _min) and (y_val < _max):
			return n 

	return 99


files = [tracking1_file_name, tracking2_file_name, tracking3_file_name, tracking4_file_name]
plots = [root.TH1D("file1", "cutflow", 7, 0.5, 7.5), root.TH1D("file2", "cutflow", 7, 0.5, 7.5), root.TH1D("file3", "cutflow", 7, 0.5, 7.5), root.TH1D("file4", "cutflow", 7, 0.5, 7.5)]

c1 = root.TCanvas("c1")
for i in range(len(files)):

	file = files[i]
	tracking_file = root.TFile.Open(file)
	tree = tracking_file.Get("integral_tree")

	passed = [0, 0, 0, 0, 0, 0, 0]
	total = 0.0
	for event_number in range(int(tree.GetEntries())):
		total += 1.0
		passed[0] += 1.0
		tree.GetEntry(event_number)
	
	#we can add some cuts here if we would like
		if not (tree.NumVertices == 1):
			continue

		passed[1] += 1

		if (tree.NumTracks < 2):
			continue

		passed[2] += 1

		close_to_ip = False
		for n in range(len(tree.track_ipDistance)):
			if (tree.track_ipDistance[n] < 320.):
				close_to_ip = True

		if close_to_ip:
			continue

		passed[3] += 1

		if not (tree.Vertex_numTracks[0] == 2):
			continue

		passed[4] += 1


		bottom_layer = False
		for hitn in range(len(tree.Digi_y)):
			y_ind = in_layer(tree.Digi_y[hitn])
			if y_ind < 2:
				bottom_layer = True
				continue
		

		if bottom_layer:
			continue

		passed[5] += 1



	#if tree.Vertex_cosOpeningAngle[0] < 0.93:
	#	continue

		new_missing_hits = []
		for val in tree.Track_missingHitLayer:
			if val > 1:
				new_missing_hits.append(val)


		if len(new_missing_hits) > 4:
			continue

		passed[6] += 1

	
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
legend.AddEntry(plots[1], "h2 sample")
legend.AddEntry(plots[2], "h5 sample")
legend.AddEntry(plots[3], "h10 sample")
legend.Draw("SAME")
c1.SetLogy()
c1.Print("cutflow.png", ".png")


		













