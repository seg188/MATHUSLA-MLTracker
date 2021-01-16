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

files = ["../tracker_files/w/statistics0.root", "../tracker_files/w/statistics1.root", "../tracker_files/w/statistics2.root", "../tracker_files/h/statistics0.root" ]

c = 29.97

muon_edep_plot = root.TH1D("mu_edep", "Muonic track total edep", 1000, 0.0, 100)
electron_edep = root.TH1D("el_edep", "Other track total edep", 1000, 0.0, 100)

for file in files:
	tracking_file = root.TFile.Open(file)
	tree = tracking_file.Get("integral_tree")

	for event_number in range(int(tree.GetEntries())):
	
		tree.GetEntry(event_number)

		ntracks = len(tree.Track_x0)
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

		for n in range(ntracks):
			n_muon_hits = 0
			for digi_n in track_digi_indices[n]:
				if is_muon(tree.Digi_pdg_id[digi_n]):
					n_muon_hits += 1

			n_digi_hits = float(len(track_digi_indices[n]))
			muonic_fraction = float(n_muon_hits)/n_digi_hits
			edep = 0.0
			for digi_n in track_digi_indices[n]:
					edep += tree.Digi_energy[digi_n]

			if muonic_fraction > 0.5:
				muon_edep_plot.Fill(edep/n_digi_hits)
			else:
				electron_edep.Fill(edep/n_digi_hits)



ca = root.TCanvas("c1")

muon_edep_plot.SetLineColor(1)
muon_edep_plot.SetLineWidth(2)
electron_edep.SetLineColor(2)
electron_edep.SetLineWidth(2)

muon_edep_plot.Scale(1.0/muon_edep_plot.Integral())
electron_edep.Scale(1.0/electron_edep.Integral())

electron_edep.Draw()
muon_edep_plot.Draw("SAME")

ca.Print("pid.png", ".png")



		





	








