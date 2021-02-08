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

files = ["../../tracker_files/feb2/wc/h2/stat0.root", "../../tracker_files/feb2/wc/h10/stat0.root"]#, "../../tracker_files/feb2/wc/w/stat0.root", "../../tracker_files/feb2/wc/w/stat1.root" ]

c = 29.97

mu_ip= root.TH1D("mu_ip", "Vertex y resolution", 50, 0.0, 800)
el_ip = root.TH1D("el_ip", "Reconstructed Vertex distance from Truth", 50, 0.0, 800)

dist_vs_chi2 = root.TH2D("dist_vs_chi2", "Distance to Truth vs. Figure of Merit", 20, 0.0, 1000, 10, 0., 5.)

n = 0
for file in files:
	tracking_file = root.TFile.Open(file)
	tree = tracking_file.Get("integral_tree")

	for event_number in range(int(tree.GetEntries())):

		tree.GetEntry(event_number)

		if (tree.NumVertices == 0):
			continue

		x, y, z, t = tree.Vertex_x[0], tree.Vertex_y[0], tree.Vertex_z[0], tree.Vertex_t[0]
		ex, ey, ez = tree.Vertex_ErrorX[0], tree.Vertex_ErrorY[0], tree.Vertex_ErrorZ[0]
				
		if n == 0:
			mu_ip.Fill(ey)
		else:
			el_ip.Fill(ey)

		

				

		


		
	n += 1

line = root.TLine(350.0, 0.0, 350.0, 0.06)
line.SetLineWidth(2)
line.SetLineColor(3)
mu_ip.SetLineColor(1)
el_ip.SetLineColor(2)

mu_ip.SetLineWidth(2)
el_ip.SetLineWidth(2)

mu_ip.Scale(1./mu_ip.Integral())
el_ip.Scale(1./el_ip.Integral())

mu_ip.GetXaxis().SetTitle("error[cm]")
mu_ip.GetXaxis().CenterTitle()
mu_ip.GetYaxis().SetTitle("frequency")
mu_ip.GetYaxis().CenterTitle()

legend = root.TLegend(0.60, 0.57, 0.85, 0.82)
legend.AddEntry(mu_ip, "2 GeV Signal")
legend.AddEntry(el_ip, "10 GeV Signal")

c1 = root.TCanvas("c1")
c1.SetLogy()

mu_ip.Draw("HIST")
el_ip.Draw("SAME HIST")
legend.Draw("SAME")

c1.Print("ipdist.png", ".png")

c2 = root.TCanvas("c2")
dist_vs_chi2.Draw("COLZ")
c2.Print("merit.png", ".png")
