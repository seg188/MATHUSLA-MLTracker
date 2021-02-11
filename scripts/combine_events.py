import ROOT as root 
import numpy as np 


file_name = "name_me"
file = root.TFile.Open(file)
tree = file.Get("box_run")

good_events = []

for n in range(int(tree.GetEntries())):
	if len(tree.)
