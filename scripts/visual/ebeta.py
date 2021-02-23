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


#base_dir = "/cms/seg188/eos/mathusla/MATHUSLA-MLTracker/build/output/feb15/w"
base_dir = "/home/stephen/hex/mathusla_all/ml_tracker/tracker_files/feb2/wc/w"
files = []
for file in os.listdir(base_dir):
	if file.endswith(".root"):
		files.append(base_dir + "/" + file)

beta_sig = root.TH1D("wey", "(beta-1)/e_beta", 100, -1., 1.)


store_total = 0.
for i in range(len(files)):

	file = files[i]
	print(file)
	tracking_file = root.TFile.Open(file)
	tree = tracking_file.Get("integral_tree")
	if (not tree):
		continue
	
	for event_number in range(int(tree.GetEntries())):
		tree.GetEntry(event_number)
		for track_n in range(int(tree.NumTracks)):
			beta = tree.Track_beta[track_n]
			ebeta = tree.Track_ErrorVy[track_n]
			beta_sig.Fill((beta-1.)/ebeta )


c1 = root.TCanvas("c1")
beta_sig.Draw()
c1.Print("betasig.png", ".png")

		













