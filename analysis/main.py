import event
import ROOT as root

tracking_file_name = "../build/w/stat0.root"
tracking_file = root.TFile.Open(tracking_file_name)
tree = tracking_file.Get("integral_tree")


ev = event.Event(tree, 2)
ev.ExtractTruthPhysics()
ev.Print()
