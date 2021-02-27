from detector import Detector 
import os
import ROOT as root
import util


class H_mumu_Analayzer:

	NCUTS = 7
	events_passing_cuts = [0.0 for n in range(NCUTS+1)]
	det = Detector()

	def __init__(self, loop_dir):
		self.files = util.GetFilesInDir(loop_dir)

	def Analyze(self, tree_name="integral_tree"):
		for file in self.files:
			tfile = root.TFile.Open(file)
			self.InitTree(tfile.Get(tree_name))
			for eventNumber in range(self.Tree.GetEntries()):
				self.Tree.GetEntry(eventNumber)
				if self.Selection():
					print(file + ": " + str(eventNumber))
		print("H_mumu Analyzer Results:")
		print(self.events_passing_cuts)
		print([util.sigfigs(x/self.events_passing_cuts[0], 2) for x in self.events_passing_cuts])

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
		self.Tree.SetBranchStatus("Track_missingHitLayer", 1)
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

		expected_hits = [False for k in range(int(self.Tree.NumTracks))]
		for track_n in range( int(self.Tree.NumTracks) ):
			x0, y0, z0 = self.Tree.Track_x0[track_n], self.Tree.Track_y0[track_n], self.Tree.Track_z0[track_n]
			vx, vy, vz = self.Tree.Track_velX[track_n], self.Tree.Track_velY[track_n], self.Tree.Track_velZ[track_n]

			y1, y2 = self.det.LayerYMid(0), self.det.LayerYMid(1)

			dt1 = (y1-y0)/vy 
			dt2 = (y2-y0)/vy

			x1 = x0 + dt1*vx 
			z1 = z0 + dt1*vz

			x2 = x0 + dt2*vx 
			z2 = z0 + dt2*vz

			if not (self.det.inSensitiveElement(x1, y1, z1) or self.det.inSensitiveElement(x2, y2, z2)):
				return False


		self.events_passing_cuts[4] += 1.0
		###########################################

		###########################################
		#vertex before track cut

		if min([self.Tree.Track_y0[0], self.Tree.Track_y0[1]]) < self.Tree.Vertex_y[0]:
			return False

		if min([self.Tree.Track_t0[0], self.Tree.Track_t0[1]]) < self.Tree.Vertex_t[0]:
			return False

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








