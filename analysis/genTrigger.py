#!/usr/bin/env python
import detector
import numpy as np
import ROOT as root
import sys

if __name__ == "__main__":

	file_name = sys.argv[1]
	tfile = root.TFile.Open(file_name)
	tree = tfile.Get("box_run")
	det = detector.Detector()
	gen_trigger = 0.0
	for n in range(tree.GetEntries()):
		tree.GetEntry(n)
		n_good_tracks = 0.0
		for k, index in enumerate(tree.GenParticle_G4index):
			if index > 0:
				print(tree.GenParticle_pdgid[k])



