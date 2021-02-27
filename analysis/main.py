import event
import ROOT as root

tracking_file_name = "../tracker_files/passed/stat91.root"
tracking_file = root.TFile.Open(tracking_file_name)
tree = tracking_file.Get("integral_tree")


for j in range(tree.GetEntries()):
	k = j + 1901
	# 292 - 2 tracks
	#635 - vertex
	tree.GetEntry(k)
#	if tree.NumTracks < 2:
#		continue
#	if tree.NumVertices < 1:
#		continue

	print(k)
	ev = event.Event(tree, k)
	#ev.ExtractTruthPhysics()
	#ev.Print()

	ev.DrawReco()


	break
