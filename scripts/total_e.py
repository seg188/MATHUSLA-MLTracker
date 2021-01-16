import numpy as np
import ROOT as root 
from bethebloch import dEdx

root.gStyle.SetOptStat(0)



layers = [[6001.0, 6004.0], [6104.0, 6107.0], [8001.0, 8004.0],[8104.0, 8107.0],[8501.0, 8504.0],[8604.0, 8607.0],[8707.0, 8710.0],[8810.0, 8813.0],[8913.0, 8916.0] ]

def is_muon(pdg):
	return (pdg == 13 or pdg == -13)

def in_layer(x):
	for n in range(len(layers)):
		if layers[n][0] < x and layers[n][1] > x:
			return n 
	return -1

files = ["../tracker_files/w/statistics0.root", "../tracker_files/w/statistics1.root", "../tracker_files/w/statistics2.root", "../tracker_files/h/statistics0.root"  ]

c = 29.97

mu_edep_plot = root.TH1D("mu_edep", "w total edep", 100, 0.0, 200)
h_edep = root.TH1D("el_edep", "signal total edep", 100, 0.0, 200)
mu_edep_plot.Sumw2()
h_edep.Sumw2()

for file in files:
	w_sample = False
	if file[17] == "w":
		print("w sample!!")
		w_sample = True
	tracking_file = root.TFile.Open(file)
	tree = tracking_file.Get("integral_tree")

	for event_number in range(int(tree.GetEntries())):
	
		tree.GetEntry(event_number)

		ntracks = len(tree.Track_x0)
		if not (ntracks >= 1):
			continue
		track_digi_indices = []

		neg_index = -1
		for n in range(ntracks):
			indices = []
			for j in range(len(tree.Track_hitIndices)):
				if j <= neg_index:
					continue
				if not (tree.Track_hitIndices[j] == -1):
					indices.append(tree.Track_hitIndices[j])
				else:
					if not (indices == []):
						track_digi_indices.append(indices)
						neg_index = j
						indices = []

		#now we "Decoded" the track digi hit indices
		event_edep = 0.0
		for e in tree.Digi_energy:
			event_edep += e

		if ntracks > 0:
			if w_sample:
			
				mu_edep_plot.Fill(event_edep)
			else:
			
				h_edep.Fill(event_edep)



ca = root.TCanvas("c1")
mu_edep_plot.SetLineColor(1)
mu_edep_plot.SetLineWidth(2)
h_edep.SetLineColor(2)
h_edep.SetLineWidth(2)

mu_edep_plot.Scale(1.0/mu_edep_plot.Integral())
h_edep.Scale(1.0/h_edep.Integral())
mu_edep_plot.Draw()
h_edep.Draw("SAME")

ca.Print("edep.png", ".png")



		





	








