import numpy as np
import ROOT as root 

root.gStyle.SetOptStat(0)



layers = [[6001.0, 6004.0], [6104.0, 6107.0], [8001.0, 8004.0],[8104.0, 8107.0],[8501.0, 8504.0],[8604.0, 8607.0],[8707.0, 8710.0],[8810.0, 8813.0],[8913.0, 8916.0] ]

def is_muon(pdg):
	return (pdg == 13 or pdg == -13)

def in_layer(x):
	for n in range(len(layers)):
		if layers[n][0] < x and layers[n][1] > x:
			return n 
	return -1

files = ["../tracker_files/w/statistics0.root", "../tracker_files/h/statistics0.root" ]

c = 29.97

mu_ip= root.TH1D("mu_ip", "IP Impact Paramter", 200, 0.7, 1.0)
el_ip = root.TH1D("el_ip", "IP Impact Paramter", 200, 0.7, 1.0)

n = 0
for file in files:
	tracking_file = root.TFile.Open(file)
	tree = tracking_file.Get("integral_tree")

	for event_number in range(int(tree.GetEntries())):

		tree.GetEntry(event_number)

		if n == 0:

			for i in range(int(len(tree.Vertex_x))):
				ip = tree.Vertex_cosOpeningAngle[i]
				mu_ip.Fill(ip)
		else:
			for i in range(int(len(tree.Vertex_x))):
				ip = tree.Vertex_cosOpeningAngle[i]
				el_ip.Fill(ip)

	n += 1
line = root.TLine(350.0, 0.0, 350.0, 0.074)
line.SetLineWidth(2)
line.SetLineColor(3)
mu_ip.SetLineColor(1)
el_ip.SetLineColor(2)

mu_ip.SetLineWidth(2)
el_ip.SetLineWidth(2)

mu_ip.Scale(1./mu_ip.Integral())
el_ip.Scale(1./el_ip.Integral())

mu_ip.GetXaxis().SetTitle("Impact Paramter [cm]")
mu_ip.GetXaxis().CenterTitle()
mu_ip.GetYaxis().SetTitle("frequency")
mu_ip.GetYaxis().CenterTitle()

legend = root.TLegend(0.60, 0.57, 0.85, 0.82)
legend.AddEntry(mu_ip, "Background")
legend.AddEntry(el_ip, "Signal")
legend.AddEntry(line, "Cut")
c1 = root.TCanvas("c1")

mu_ip.Draw()
el_ip.Draw("SAME")
line.Draw("SAME")
legend.Draw("SAME")

c1.Print("ipdist.png", ".png")
