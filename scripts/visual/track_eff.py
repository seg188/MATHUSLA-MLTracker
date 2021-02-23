import visualization
from detector import Detector
import ROOT as root 
import os
import numpy as np

root.gStyle.SetOptStat(0)
file = "../../build/output/pgun/e10gev/stat0.root"
tracking_file = root.TFile.Open(file)
tree = tracking_file.Get("integral_tree")

det = Detector() 		

nbins = 50										 	
nbinsy = 30

eff = root.TH1D("track_eff", "Track Efficiency by Eta", nbins, 0.1, 2.1 )
count = root.TH1D("count", "Track Efficiency by Eta", nbins, 0.1, 2.1 )
total = root.TH1D("total", "Track Efficiency by Eta", nbins, 0.1, 2.1 )

eta_diff = root.TH1D("eta_diff", "Truth vs. Reco Eta", 30, -0.15, 0.15)
count_2track = root.TH1D("count_2tracks", "Track Efficiency by Eta", nbins, 0.1, 2.1 ) 
eff_2track = root.TH1D("track_eff_2tracks", "Track Efficiency by Eta", nbins, 0.1, 2.1 ) 

eff2d = root.TH2D("track_eff2d", "Track Efficiency by Eta", nbins, 0.1, 2.1, nbinsy, -0.4, 0.4 )
count2d = root.TH2D("count2d", "Track Efficiency by Eta", nbins, 0.1, 2.1 , nbinsy, -0.4, 0.4)
total2d = root.TH2D("total2d", "Track Efficiency by Eta", nbins, 0.1, 2.1 , nbinsy, -0.4, 0.4)

nlayer_map = root.TH2D("nlayer_map", "Sensitive Layers hit by Eta, Phi", nbins, 0.1, 2.1, nbinsy, -0.4, 0.4 )
nlayer_1d = root.TH1D("nlayer_1d", "Sensitive Layers hit by Eta", nbins, 0.1, 2.1 )

for k in range(tree.GetEntries()):
	tree.GetEntry(k)
	x, y, z = 200., 6000., 7050.
	px, py, pz = tree.GenParticle_py[0], -1.*tree.GenParticle_pz[0], tree.GenParticle_px[0]
	pt = np.sqrt(px**2 + py**2)
	
	eta = np.arcsinh(pz/pt)
	phi = np.arcsin(px/pt)
	

	total.Fill(eta)
	total2d.Fill(eta, phi)
	nlayers = det.nSensitiveLayers(x, y, z, px, py, pz)
	nlayer_map.Fill(eta, phi, nlayers )
	nlayer_1d.Fill(eta, nlayers)

	if tree.NumTracks > 0:
		count.Fill(eta)
		count2d.Fill(eta, phi)
		vx, vy, vz = tree.Track_velX[0], tree.Track_velY[0], tree.Track_velZ[0]
		tr_vt = np.sqrt(vx**2 + vy**2)
		tr_eta = np.arcsinh(vz/tr_vt)
		eta_diff.Fill(eta - tr_eta)

	if tree.NumTracks > 1:
		count_2track.Fill(eta)

for k in range(count.GetNbinsX()):
	if total.GetBinContent(k+1) > 0 and count.GetBinContent(k+1) > 0:
		A = count.GetBinContent(k+1)
		B = total.GetBinContent(k+1)
		C = nlayer_1d.GetBinContent(k+1)
		eff.SetBinContent(k+1, A/B)
		eff.SetBinError(k+1, np.sqrt((A/B)*(1./B + A/(B**2))) )
		nlayer_1d.SetBinContent(k+1, C/B)
		nlayer_1d.SetBinError(k+1, np.sqrt((C/B)*(1./B + C/(B**2))) )

		if count_2track.GetBinContent(k+1) > 0:
			A = count_2track.GetBinContent(k+1)
			eff_2track.SetBinContent(k+1, A/B)
			eff_2track.SetBinError(k+1, np.sqrt((A/B)*(1./B + A/(B**2)))  )

	for l in range(count2d.GetNbinsY()):
		if total2d.GetBinContent(k+1, l+1) > 0 and count2d.GetBinContent(k+1, l+1) > 0:
			A = count2d.GetBinContent(k+1, l+1)
			B = total2d.GetBinContent(k+1, l+1)
			eff2d.SetBinContent(k+1, l+1, A/B)

		if total2d.GetBinContent(k+1, l+1) > 0:
			C = nlayer_map.GetBinContent(k+1, l+1)
			D = total2d.GetBinContent(k+1, l+1)
			nlayer_map.SetBinContent(k+1, l+1, C/D)




c1 = root.TCanvas("c1")
eff.GetYaxis().SetRangeUser(0., 1.0)
eff.Draw()
c1.Print("feb17/track_eff.png", ".png")

c2 = root.TCanvas("c2")
eff2d.Draw("COLZ")
c2.Print("feb17/track_eff2d.png", ".png")

c3 = root.TCanvas("c3")
eff_2track.Draw()
c3.Print("feb17/track_eff_2tracks.png", ".png")

c4 = root.TCanvas("c4")
nlayer_map.Draw("COLZ")
c4.Print("feb17/nlayer_map.png", ".png")

c5 = root.TCanvas("c5")
eta_diff.Draw()
c5.Print("feb17/eta_diff.png", ".png")

c6 = root.TCanvas("c6")
nlayer_1d.Draw()
c6.Print("feb17/1d_etamap.png", ".png")