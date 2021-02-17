import visualization
import physics
import ROOT as root 
import os

base_dir =  "../../build/etarange"
files = []
names = []
for file in os.listdir(base_dir):
	if file.endswith(".root"):
		files.append(base_dir + "/" + file)
		names.append(file)
files.sort()
names.sort()
print(names)

det = physics.Detector() 												 	

indices = [8, 9, 6, 7, 3, 12, 4, 10, 1, 14, 11, 5, 2, 13]

count = [0. for i in range(len(files))]
total = [0. for i in range(len(files))]

eff = root.TH1D("track_eff", "Track Efficiency by Eta", len(files), 0.0, float(len(files))/10. )


for n, file in enumerate(files):
	tracking_file = root.TFile.Open(file)
	tree = tracking_file.Get("integral_tree")

	for k in range(tree.GetEntries()):
		tree.GetEntry(k)
		total[n] += 1.0

		if tree.NumTracks > 0:
			count[n] += 1.

	eff.SetBinContent(indices[n], count[n]/total[n])

c1 = root.TCanvas("c1")
eff.Draw()
c1.Print("track_eff.png", ".png")










