import numpy as np
import ROOT as root
import physics

def roc_curves(signal, backgrounds):
	nbins = signal.GetNbinsX()
	plots = [root.TGraph(nbins) for plot in backgrounds]
	for n in range(nbins):
		tpr = 1.-signal.Integral(0, n)
		fpr = [1.-plot.Integral(0, n) for plot in backgrounds]
		for k, plt in enumerate(plots):
			plt.SetPoint(n, fpr[k], tpr)

	for k, plt in enumerate(plots):
		plt.SetLineColor(k+1)
		plt.SetLineWidth(3)
		plt.SetMarkerColor(k+1)
		plt.SetMarkerStyle(8)

	return plots

root.gStyle.SetOptStat(0)



tracking4_file_name = "../../tracker_files/feb2/wc/w/stat0.root"
tracking5_file_name = "../../tracker_files/feb2/wc/w/stat1.root"
tracking6_file_name = "../../tracker_files/feb2/wc/w/stat2.root"

tracking1_file_name = "../../tracker_files/feb2/wc/h2/stat0.root" 
#tracking2_file_name = "../../tracker_files/feb2/wc/h5/stat0.root" 
tracking2_file_name = "../../tracker_files/feb2/wc/h10/stat0.root"

file_collection_2 = [tracking1_file_name, tracking2_file_name]#, tracking3_file_name ]
file_collection_1 = [tracking4_file_name]#, tracking5_file_name, tracking6_file_name]
file_collections =  [file_collection_1, [tracking1_file_name], [tracking2_file_name]]#, [tracking3_file_name]]#, file_collection_2]
collection_names = ["W-background", "Signal (2 GeV/c^2)", "Signal (10 GeV/c^2)"]#, "Signal (10 GeV/c^2)"]

det = physics.Detector()

totals = [0.0 for i in range(len(file_collections))]
fiducials = [0.0 for i in range(len(file_collections))]

plots = [root.TH1D("coll" + str(n), "Impact Parameter to IP", 30, -15., 15.) for n in range(len(file_collections))]
maps = [root.TH2D("map" + str(n), "Vertex Map", 200, 1000, 11000, 500, -10000., 10000.) for n in range(len(file_collections))]

for n, collection in enumerate(file_collections):
	for file in collection:
		tfile = root.TFile.Open(file)
		tree = tfile.Get("integral_tree")

		for ev_n in range(int(tree.GetEntries())):

			tree.GetEntry(ev_n)
			if tree.NumTracks == 0:
				continue

			if tree.NumVertices == 0:
				continue

			totals[n] += 1.

			x, y, z, t = tree.Vertex_x[0], tree.Vertex_y[0], tree.Vertex_z[0], tree.Vertex_t[0]
			maps[n].Fill(y, x)

			if not (det.inBox(x, y, z)):
				continue

			fiducials[n] += 1.

			#finding distance to closest layer!!!!
			t0 = min(tree.Track_t0)
			y0 = min(tree.Track_y0)

			ey = tree.Vertex_ErrorY[0]
			et = tree.Vertex_ErrorT[0]

			QOI = max([(y-y0)/ey, (t-t0)/et])

			plots[n].Fill(QOI)

			



c1 = root.TCanvas("c1")
col = 1

legend = root.TLegend(0.57, 0.63, 0.9, 0.9)

histstack = root.THStack()
for plot in plots:
	plot.Scale(1/plot.Integral())
	plot.SetLineColor(col)
	#plot.SetFillColor(col)
	plot.SetMarkerColor(col)
	plot.SetMarkerStyle(8)
	histstack.Add(plot, "HIST")
	plot.SetLineWidth(2)
	#plot.SetFillColor(col)
	legend.AddEntry(plot, collection_names[col-1])
	col += 1


histstack.Draw("NOSTACK")


legend.Draw("SAME")

c1.Print("plot.png", ".png")

c2 = root.TCanvas("c2")
            
rocs = roc_curves(plots[0], plots)

rocs[0].SetTitle("TPR vs. FPR")
rocs[0].Draw("AC")
rocs[0].GetXaxis().SetRangeUser(0.,1.)
rocs[0].GetYaxis().SetRangeUser(0.,1.)
rocs[0].GetXaxis().SetTitle("fpr")
rocs[0].GetXaxis().CenterTitle()
rocs[0].GetYaxis().CenterTitle()

legend2 = root.TLegend(0.60, 0.1, 0.9, 0.5)

for pltnum, plt in enumerate(rocs):
	if pltnum == 0:
		continue
	plt.Draw("SAME P")
	print(pltnum)
	legend2.AddEntry(plt, collection_names[pltnum])


legend2.Draw("SAME")
c2.Print("c2.png", ".png")

c3 = root.TCanvas("c3")

maps[0].SetMarkerStyle(8)
maps[0].GetXaxis().SetTitle("y [cm]")
maps[0].GetXaxis().CenterTitle()
maps[0].GetYaxis().SetTitle("x [cm]")
maps[0].GetYaxis().CenterTitle()

maps[0].Draw()
t = root.TLine(det.yLims()[0], det.xLims()[0] , det.yLims()[1], det.xLims()[0])
b = root.TLine(det.yLims()[0], det.xLims()[1] , det.yLims()[1], det.xLims()[1])
l = root.TLine(det.yLims()[0], det.xLims()[0] , det.yLims()[0], det.xLims()[1])
r = root.TLine(det.yLims()[1], det.xLims()[0] , det.yLims()[1], det.xLims()[1])
lines = [ t, b, l, r]

for line in lines:
	line.SetLineWidth(3)
	line.Draw("SAME")

c3.Print("c3.png", ".png")

legend.Draw("SAME")
print(totals)
print(fiducials)