from detector import Detector 
import os
import ROOT as root
import util
from event import Event

class H_mumu_Analayzer:

	plot_dir = ""
	NCUTS = 7
	events_passing_cuts = [0.0 for n in range(NCUTS+1)]
	det = Detector()

	def __init__(self, loop_dir):
		self.files = util.GetFilesInDir(loop_dir)
		self.passed_files = []
		self.passed_events= []

	def SetPlotDir(self, dirname):
		self.plot_dir = dirname

	def Analyze(self, tree_name="integral_tree"):
		self.tree_name = tree_name
		for file in self.files:
			passed_events = []
			print("Working in file: " + file)
			tfile = root.TFile.Open(file)
			self.InitTree(tfile.Get(tree_name))
			for eventNumber in range(self.Tree.GetEntries()):
				self.Tree.GetEntry(eventNumber)
				if self.Selection():
					print(file + ": " + str(eventNumber))
					passed_events.append(eventNumber)
			if len(passed_events) > 0:
				self.passed_files.append(file)
				self.passed_events.append(passed_events)
		
		print(self.passed_events)
		print("H_mumu Analyzer Results:")
		print(self.events_passing_cuts)

	def StudyPassedEvents(self, n):
		file = self.passed_files[n]
		tfile = root.TFile.Open(file)
		self.Tree = tfile.Get(self.tree_name)
		for eventNumber in self.passed_events[n]:
			self.Tree.GetEntry(eventNumber)
			currEvent = Event(self.Tree, eventNumber)
			#currEvent.ExtractTruthPhysics()
			#currEvent.Print()
			currEvent.GetRecoInfo()
			currEvent.DrawReco()
		

	def InitTree(self, tree):
		self.Tree = tree
		self.Tree.SetBranchStatus("*", 0)
		self.Tree.SetBranchStatus("Digi_x", 1)
		self.Tree.SetBranchStatus("Digi_y", 1)
		self.Tree.SetBranchStatus("NumTracks", 1)
		self.Tree.SetBranchStatus("NumVertices", 1)
		self.Tree.SetBranchStatus("Vertex_x", 1)
		self.Tree.SetBranchStatus("Vertex_y", 1)
		self.Tree.SetBranchStatus("Vertex_z", 1)
		self.Tree.SetBranchStatus("Vertex_t", 1)
		self.Tree.SetBranchStatus("Vertex_ErrorY", 1)
		self.Tree.SetBranchStatus("Vertex_ErrorT", 1)
		self.Tree.SetBranchStatus("Track_velX", 1)
		self.Tree.SetBranchStatus("Track_velY", 1)
		self.Tree.SetBranchStatus("Track_velZ", 1)
		self.Tree.SetBranchStatus("Track_x0", 1)
		self.Tree.SetBranchStatus("Track_y0", 1)
		self.Tree.SetBranchStatus("Track_z0", 1)
		self.Tree.SetBranchStatus("Track_t0", 1)
		self.Tree.SetBranchStatus("Track_ErrorY0", 1)
		self.Tree.SetBranchStatus("Track_ErrorT0", 1)
		self.Tree.SetBranchStatus("Track_missingHitLayer", 1)
		self.Tree.SetBranchStatus("Track_expectedHitLayer", 1)
		self.Tree.SetBranchStatus("track_ipDistance", 1)
		self.Tree.SetBranchStatus("Track_hitIndices", 1)


	def Trigger(self):
		if len(self.Tree.Digi_x) < 3:
			return False 
		return True

	def Selection(self):
		
		if not self.Trigger():
			return False

		###########################################
		#counting total events
		self.events_passing_cuts[0] += 1.0
		###########################################
		
		###########################################
		#ntracks cut
		if (self.Tree.NumTracks < 2):
			return False

		self.events_passing_cuts[1] += 1.0
		###########################################

		###########################################
		#nvertices cut
		if self.Tree.NumVertices < 1:
			return

		self.events_passing_cuts[2] += 1.0
		###########################################

		###########################################
		#fiducial vertex cut
		if not self.det.inBox(self.Tree.Vertex_x[0], self.Tree.Vertex_y[0], self.Tree.Vertex_z[0]):
			return False

		self.events_passing_cuts[3] += 1.0
		###########################################

		###########################################
		#floor veto w/ expected hit cuts
		for hity in self.Tree.Digi_y:
			if self.det.inLayer(hity) < 2:
				return False

		expected_hits = util.unzip(self.Tree.Track_expectedHitLayer)

		bottom_layer_expected_hits = []

		for exp_list in expected_hits:
			for val in exp_list:
				if val < 2:
					bottom_layer_expected_hits.append(val)

		if len(bottom_layer_expected_hits) < 4:
			return


		self.events_passing_cuts[4] += 1.0
		###########################################

		###########################################
		#vertex before track cut

		vtxTrackConsistencyY = max( [ (self.Tree.Vertex_y[0] - self.Tree.Track_y0[n])/self.Tree.Track_ErrorY0[n] for n in range(int(self.Tree.NumTracks)) ] )
		#vtxTrackConsistencyT = max( [ (self.Tree.Vertex_t[0] - self.Tree.Track_t0[n])/self.Tree.Track_ErrorT0[n] for n in range(int(self.Tree.NumTracks)) ] )

		if vtxTrackConsistencyY > 1.0:
			return

		self.events_passing_cuts[5] += 1.0
		###########################################

		###########################################
		#missing hits in upper layers

		trackn = 0
		for layern in self.Tree.Track_missingHitLayer:
			if layern == -1:
				trackn += 1
			else:
				if layern >= 5:
					return False

		self.events_passing_cuts[6] += 1.0
		###########################################

		###########################################
		#tracks in vertex start in same layer

		track_hit_yvals = [ [] for i in range(len(self.Tree.Track_x0))]
		trackn = 0
		for hitn in self.Tree.Track_hitIndices:
			if hitn == -1:
				trackn += 1
			else:
				track_hit_yvals[trackn].append(self.Tree.Digi_y[hitn])

		min_layers = [ self.det.inLayer(min(yvals_list)) for yvals_list in track_hit_yvals ]

		veto = False

		start = min_layers[0]

		for minval in min_layers:
			if not minval==start:
				return False

		self.events_passing_cuts[7] += 1.0
		###########################################


		return True


	def Plot1D(self, branch_name):
		plotvar = 0.0
		self.Tree.SetBranchStatus("")







