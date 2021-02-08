import ROOT as root
import numpy as np


##H FILE
tracking_file_name = "../tracker_files/jan21/h/stat0.root"
tracking_file = root.TFile.Open(tracking_file_name)
tree = tracking_file.Get("integral_tree")



tracking_file_namew = "../tracker_files/jan21/w/stat0.root"
tracking_filew = root.TFile.Open(tracking_file_namew)
treew = tracking_filew.Get("integral_tree")

vertexResW = root.TH1D("vertex_res_w", "vertex resolution", 50, 0., 100.)



vertexResH = root.TH1D("vertex_res_H", "vertex resolution", 50, 0., 100.)

legend = root.TLegend(0.65, 0.75, 0.98, 0.95)

c = 29.97

for k in range(int(tree.GetEntries())):
	tree.GetEvent(k)

	if (tree.NumVertices < 1):
		continue

	ex = tree.Vertex_ErrorX[0]
	ey = tree.Vertex_ErrorY[0]
	ez = tree.Vertex_ErrorZ[0]
	et = tree.Vertex_ErrorT[0]

	err = np.sqrt(ex**2 + ey**2 + ez**2 ) #+ (c*et)**2) 

	vertexResH.Fill(err)

c1 = root.TCanvas("c1")
vertexResH.GetXaxis().SetTitle("total error [cm]")
vertexResH.GetXaxis().CenterTitle()
vertexResH.GetYaxis().SetTitle("count")
vertexResH.GetYaxis().CenterTitle()
vertexResH.Scale(1/vertexResH.Integral())




for k in range(int(treew.GetEntries())):
	treew.GetEvent(k)

	if (treew.NumVertices < 1):
		continue

	ex = treew.Vertex_ErrorX[0]
	ey = treew.Vertex_ErrorY[0]
	ez = treew.Vertex_ErrorZ[0]
	et = treew.Vertex_ErrorT[0]

	err = np.sqrt(ex**2 + ey**2 + ez**2 + (c*et)**2) 

	print(err)

	vertexResW.Fill(err)


vertexResW.SetLineColor(2)
vertexResW.Scale(1/vertexResW.Integral())
vertexResW.Draw("HIST")
vertexResH.Draw("HIST SAME")


blank = root.TGraph(1)
blank.SetLineColor(0)


legend.AddEntry(vertexResW, "W-sample (5 mil)" )
legend.AddEntry(blank, "mean=" + str( round(vertexResW.GetMean(), 2)))
legend.AddEntry(vertexResH, "signal (1 mil)")
legend.AddEntry(blank, "mean=" + str(round(vertexResH.GetMean(), 2) ))

legend.Draw("SAME")

c1.Print("vertexRes.png", ".png")