import numpy as np
import ROOT as root 
from bethebloch import dEdx

root.gStyle.SetOptStat(0)

NDRAW = 2000
gamma_min = 1.1
gamma_max = 65.
theory = root.TGraph(NDRAW)
for i in range(NDRAW):
	gamma = gamma_min + (gamma_max - gamma_min)*(float(i)/float(NDRAW))
	theory.SetPoint(i, gamma, dEdx(gamma))

theory.SetLineColor(2)
theory.SetLineWidth(2)


scintillator_y_height = 3.00

layers = [[6001.0, 6004.0], [6104.0, 6107.0], [8001.0, 8004.0],[8104.0, 8107.0],[8501.0, 8504.0],[8604.0, 8607.0],[8707.0, 8710.0],[8810.0, 8813.0],[8913.0, 8916.0] ]

def in_layer(x):
	for n in range(len(layers)):
		if layers[n][0] < x and layers[n][1] > x:
			return n 
	return -1

files = ["../tracker_files/w/statistics0.root", "../tracker_files/w/statistics1.root", "../tracker_files/w/statistics2.root", "../tracker_files/w/statistics0.root" ]

c = 29.97

dedx_th1 = root.TH2D("dedx", "dE/dX", 200, 1.0, 50., 50, 1.0, 8.0)
beta_plot = root.TH1D("beta", "Digi Particle Gamma", 1000, 0.0, 100)

for file in files:
	tracking_file = root.TFile.Open(file)
	tree = tracking_file.Get("integral_tree")

	for event_number in range(int(tree.GetEntries())):
	
		tree.GetEntry(event_number)
		nhits = float(len(tree.Digi_x))
		e_sum = 0.
		p_sum = 0.
		dx_sum = 0.

		layer_e = [0. for i in layers]
		E = 0.
		beta = 0.
		theta = 0.
		gamma =0

		if nhits > 0:
			E = tree.Digi_particle_energy[0] #mev
			px, py, pz = tree.Digi_px[0], tree.Digi_py[0], tree.Digi_pz[0] #mev/c
			p = np.sqrt(px*px + py*py + pz*pz) #mev/c

			m = np.sqrt(E*E - p*p)
			if m < 100:
				continue
			gamma = E/(m)
			beta = p/(gamma*m)
			beta_plot.Fill(E/1000.)

			#print([beta, gamma, E/1000.0])
			theta = np.arccos(tree.Digi_py[0]/p)

		for k in range(int(len(tree.Digi_x))):
			E = tree.Digi_particle_energy[k]
		
			layer_index = in_layer(tree.Digi_y[k])
			energy_dep = tree.Digi_energy[k]
			layer_e[layer_index] += energy_dep

		if nhits > 0:
			for edep in layer_e:
				dedx_th1.Fill(gamma, edep/scintillator_y_height)	


mean = dedx_th1.ProfileX()

canvas = root.TCanvas("c2")
mean.Draw()
dedx_th1.Rebin(2)
canvas.Print("test.png", ".png")


c1 = root.TCanvas("c1")
c1.SetLogx()

dedx_th1.GetXaxis().SetTitle("gamma factor")
dedx_th1.GetYaxis().SetTitle("dE/dx [MeV/cm]")
dedx_th1.GetXaxis().CenterTitle()
dedx_th1.GetYaxis().CenterTitle()
dedx_th1.SetTitle("dE/dX for Muon-Digi Hits")

legend = root.TLegend(0.55, 0.65, 0.90, 0.90)
#legend.AddEntry(dedx_th1, "dE/dX binned in gamma")
legend.AddEntry(mean, "Mean dE/dX by gamma")
legend.AddEntry(theory, "Bethe-Bloche Curve (Muon in C9H10)")


dedx_th1.Draw("COLZ")
theory.Draw("SAME C")
mean.SetLineColor(1)
mean.SetLineWidth(2)
mean.Draw("SAME")
legend.Draw("SAME")
c1.Print("dedx.png", ".png")





