from detector import Detector
import os
import ROOT as root
import util
from event import Event

class H_mumu_Analyzer:

	plot_dir = ""
	NCUTS = 6
	events_passing_cuts = [0.0 for n in range(NCUTS+1)]
	det = Detector()

	def __init__(self, loop_dir):
		self.files = util.GetFilesInDir(loop_dir)
		self.passed_files = []
		self.passed_events= []
		self.floor_hit_location = root.TH2D("floor_hit_location", "floor hit x,z", 1000, -5100., 5100., 1000, 6900., 17100. )
		self.vertex_y = root.TH1D("vertex_y", "vertex y", 100, 6000., 9000.)

	def SetPlotDir(self, dirname):
		self.plot_dir = dirname

	def Analyze(self, tree_name="integral_tree"):
		self.tree_name = tree_name
		for file in self.files:
			passed_events = []
			print("Working in file: " + file)
			tfile = root.TFile.Open(file)
			self.events_passing_cuts_byfile = [0.0 for n in range(self.NCUTS+1)]
			self.InitTree(tfile.Get(tree_name))
			for eventNumber in range(self.Tree.GetEntries()):
				self.Tree.GetEntry(eventNumber)
				if self.Selection():
					print(file + ": " + str(eventNumber))
					passed_events.append(eventNumber)
			if len(passed_events) > 0:
				self.passed_files.append(file)
				self.passed_events.append(passed_events)

			print(self.events_passing_cuts_byfile)

		print(self.passed_events)
		print("H_mumu Analyzer Results:")
		print(self.events_passing_cuts)
		c1 = root.TCanvas("c1")
		self.floor_hit_location.SetMarkerSize(2)
		self.floor_hit_location.SetMarkerStyle(6)
		self.floor_hit_location.Draw()
		c1.Print("floor_hit.png")

		c2 = root.TCanvas("c2")
		self.vertex_y.Draw()
		c2.Print("vertex_y.png")

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
		self.Tree.SetBranchStatus("Hit_x", 1)
		self.Tree.SetBranchStatus("Hit_y", 1)
		self.Tree.SetBranchStatus("Hit_z", 1)
		self.Tree.SetBranchStatus("Hit_particlePy", 1)
		self.Tree.SetBranchStatus("Hit_particlePdgId", 1)
		self.Tree.SetBranchStatus("Hit_energy", 1)
		self.Tree.SetBranchStatus("Digi_hitIndices", 1)
		self.Tree.SetBranchStatus("Digi_x", 1)
		self.Tree.SetBranchStatus("Digi_y", 1)
		self.Tree.SetBranchStatus("Digi_z", 1)
		self.Tree.SetBranchStatus("Digi_numHits", 1)
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
		self.Tree.SetBranchStatus("Track_numHits", 1)


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
		self.events_passing_cuts_byfile[0] += 1.0
		###########################################

		###########################################
		#ntracks cut
		if (self.Tree.NumTracks < 2):
			return False


		postive_track_vel_y = []
		vely = util.unzip(self.Tree.Track_velY)

		for vely_list in vely:
			for val in vely_list:
				if val > 0:
					postive_track_vel_y.append(val)

		if len(postive_track_vel_y) < 2:
			return False

		# for k, value in enumerate(self.Tree.Track_velY):
		# 	if value < 0:
		# 		return False

		self.events_passing_cuts[1] += 1.0
		self.events_passing_cuts_byfile[1] += 1.0
		###########################################

		###########################################
		bottom_layer_count = 1


		expected_hits = util.unzip(self.Tree.Track_expectedHitLayer)
		bottom_layer_expected_hits = []
		number_of_tracks_with_postive_y_value = 0

		for k, value in enumerate(self.Tree.Track_velY):
			if value > 0:
				number_of_tracks_with_postive_y_value += 1.0
				for val in expected_hits[k]:
					if val < bottom_layer_count:
						bottom_layer_expected_hits.append(val)

		# dont have an expected hit at bottom layer
		if len(bottom_layer_expected_hits) != (number_of_tracks_with_postive_y_value*bottom_layer_count):
			return False


		self.events_passing_cuts[2] += 1.0
		self.events_passing_cuts_byfile[2] += 1.0
		###########################################
		track_digi_indices = util.unzip(self.Tree.Track_hitIndices)
		for k, value in enumerate(self.Tree.Track_velY):
			if value > 0:
				for digi_index in track_digi_indices[k]:
					if self.det.inLayer(self.Tree.Digi_y[digi_index]) < bottom_layer_count:
						return False

		self.events_passing_cuts[3] += 1.0
		self.events_passing_cuts_byfile[3] += 1.0
		###########################################

		# if len(self.Tree.Vertex_x) != 0:
		# 	self.events_passing_cuts[6] += 1.0
		# 	self.events_passing_cuts_byfile[6] += 1.0

####################
		for k, value in enumerate(self.Tree.Track_velY):
			if value < 0:
				return False

		self.events_passing_cuts[4] += 1.0
		self.events_passing_cuts_byfile[4] += 1.0
#################
		for hity in self.Tree.Digi_y:
			if self.det.inLayer(hity) < bottom_layer_count:
				return False

		self.events_passing_cuts[5] += 1.0
		self.events_passing_cuts_byfile[5] += 1.0


		####
		####
		# print("#################################################################################################################################################################")
		# print("Hit_pdg: ", self.Tree.Hit_particlePdgId, "\n", "Hit_z: ", self.Tree.Hit_z, "\n", "Hit_x: ", self.Tree.Hit_x, "\n", "Hit_y: ", self.Tree.Hit_y, "\n", "Hit_VY: ", self.Tree.Hit_particlePy, "\n", "Hit size: ", self.Tree.Hit_x.size(), "\n",
		# "Digi_z: ", self.Tree.Digi_z, "\n", "Digi_x: ", self.Tree.Digi_x, "\n", "Digi_y: ", self.Tree.Digi_y, "\n", "Digi_numHits: ", self.Tree.Digi_numHits, "\n", "Digi size: ", self.Tree.Digi_x.size(), "\n", "digi_hit_index: ",  self.Tree.Digi_hitIndices,
		# "\n", "Track_x0: ", self.Tree.Track_x0, "\n", "Track_z0: ", self.Tree.Track_z0, "\n", "Track_y0: ", self.Tree.Track_y0, "\n", "trackpy:", self.Tree.Track_velY, "\n", "Track_hitIndices: ", self.Tree.Track_hitIndices, "\n", "Track_numhits: ", self.Tree.Track_numHits,
		# "\n", "Vertex_y: ", self.Tree.Vertex_y)
		# print("#################################################################################################################################################################")

		# for k, value in enumerate(self.Tree.Hit_y):
		# 	for index in self.Tree.Digi_hitIndices:
		# 		if k == index:
		# 			print("HHHHHHHHHHH_y: ", value, " PDG: ", self.Tree.Hit_particlePdgId[k], "\n")

		# for k, value in enumerate(self.Tree.Hit_energy):
		# 	if value < 0.65 and self.Tree.Hit_y[k] < 7000:
		# 		print("HHHHHHHHHHH_y: ", self.Tree.Hit_y[k], ", eeeeeeeee: ", value, " PDG: ", self.Tree.Hit_particlePdgId[k], "\n")
# ###########################
# 		for k, value in enumerate(self.Tree.Hit_particlePdgId):
# 			if abs(value) == 13 and self.Tree.Hit_particlePy[k] > 0:
# 				self.events_passing_cuts[6] += 1.0
# 				self.events_passing_cuts_byfile[6] += 1.0
# ###########################
		for k, value in enumerate(self.Tree.Vertex_y):
			self.vertex_y.Fill(value)



		for k, value in enumerate(self.Tree.Track_velY):
			if value > 0:
				x00, y00, z00 = self.Tree.Track_x0[k], self.Tree.Track_y0[k], self.Tree.Track_z0[k]
				vx0, vy0, vz0 = self.Tree.Track_velX[k], self.Tree.Track_velY[k], self.Tree.Track_velZ[k]

				floor_y = 6004.5

				delt0 = (floor_y - y00)/vy0
				expected_x0 = x00 + (delt0*vx0)
				expected_z0 = z00 + (delt0*vz0)

				self.floor_hit_location.Fill(expected_x0, expected_z0)

		####
		####

		###########################################
		#nvertices cut
		# if self.Tree.NumVertices == 0:
		# 	return False
		#
		# self.events_passing_cuts[3] += 1.0
		# self.events_passing_cuts_byfile[3] += 1.0
		###########################################

		###########################################
		#fiducial vertex cut
		# if not self.det.inBox(self.Tree.Vertex_x[0], self.Tree.Vertex_y[0], self.Tree.Vertex_z[0]):
		# 	return False
		#
		# self.events_passing_cuts[4] += 1.0
		# self.events_passing_cuts_byfile[4] += 1.0
		###########################################



		###########################################
		#vertex before track cut

		# vtxTrackConsistencyY = max( [ (self.Tree.Vertex_y[0] - self.Tree.Track_y0[n])/self.Tree.Track_ErrorY0[n] for n in range(int(self.Tree.NumTracks)) ] )
		# #vtxTrackConsistencyT = max( [ (self.Tree.Vertex_t[0] - self.Tree.Track_t0[n])/self.Tree.Track_ErrorT0[n] for n in range(int(self.Tree.NumTracks)) ] )
		#
		# if vtxTrackConsistencyY > 1.0:
		# 	return
		#
		# self.events_passing_cuts[5] += 1.0
		# self.events_passing_cuts_byfile[5] += 1.0
		###########################################

		###########################################
		#missing hits in upper layers

		# trackn = 0
		# vertex_first_layer = self.det.nextLayer(self.Tree.Vertex_y[0])
		# for layern in self.Tree.Track_missingHitLayer:
		# 	if layern >= vertex_first_layer:
		# 		return False
		#
		# self.events_passing_cuts[6] += 1.0
		# self.events_passing_cuts_byfile[6] += 1.0

		#note the cut below isnt necessary when requiring no missing hits
		###########################################








		###########################################
		#tracks in vertex start in same layer

		#track_hit_yvals = [ [] for i in range(len(self.Tree.Track_x0))]
		#trackn = 0
		#for hitn in self.Tree.Track_hitIndices:
		#	if hitn == -1:
		#		trackn += 1
		#	else:
		#		track_hit_yvals[trackn].append(self.Tree.Digi_y[hitn])

		#min_layers = [ self.det.inLayer(min(yvals_list)) for yvals_list in track_hit_yvals ]

		#veto = False

		#start = min_layers[0]

		#for minval in min_layers:
		#	if not minval==start:
		#		#check if there is expected hit in that layer
		#		return False

		#self.events_passing_cuts[7] += 1.0
		#self.events_passing_cuts_byfile[] += 1.0
		###########################################


		return True


	def Plot1D(self, branch_name):
		plotvar = 0.0
		self.Tree.SetBranchStatus("")

###############################################################################################################################################################################
###############################################################################################################################################################################


class K_Long_Analayzer:

	plot_dir = ""
	NCUTS = 4
	events_passing_cuts = [0.0 for n in range(NCUTS+1)]
	det = Detector()

	def __init__(self, loop_dir):
		self.files = util.GetFilesInDir(loop_dir)
		self.passed_files = []
		self.passed_events= []

	def SetPlotDir(self, dirname):
		self.plot_dir = dirname

	def Plot(self, tree_name="integral_tree"):
		self.tree_name = tree_name
		plot = root.TH1D("plot", "Track Beta for events w/ vertex", 20, 0.60, 1.20)
		for file in self.files:
			print("Working in file: " + file)
			tfile = root.TFile.Open(file)
			self.InitTree(tfile.Get(tree_name))
			for eventNumber in range(self.Tree.GetEntries()):
				self.Tree.GetEntry(eventNumber)
				plotif, val = self.SelectionForPlot()
				if plotif:
					plot.Fill(val)
		c1 = root.TCanvas("c1")
		plot.Draw()
		c1.Print(self.plot_dir + "plot1.png", ".png")

	def SelectionForPlot(self):
		if not self.Trigger():
			return False, 0

		###########################################
		#counting total events

		###########################################
		#ntracks cut
		if (self.Tree.NumTracks < 2):
			return False, 0


		###########################################
		#nvertices cut
		if self.Tree.NumVertices == 0:
			return False, 0


		###########################################
		#fiducial vertex cut
		if not self.det.inBox(self.Tree.Vertex_x[0], self.Tree.Vertex_y[0], self.Tree.Vertex_z[0]):
			return False, 0


		###########################################
		#floor veto w/ expected hit cuts
		for hity in self.Tree.Digi_y:
			if self.det.inLayer(hity) < 2:
				return False, 0

		expected_hits = util.unzip(self.Tree.Track_expectedHitLayer)

		bottom_layer_expected_hits = []

		for exp_list in expected_hits:
			for val in exp_list:
				if val < 2:
					bottom_layer_expected_hits.append(val)

		if len(bottom_layer_expected_hits) < 3:
			return False, 0


		###########################################
		#vertex before track cut


		return True, min(self.Tree.Track_beta)


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

			print(self.events_passing_cuts_byfile)

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
		self.Tree.SetBranchStatus("Track_beta", 1)


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
		self.events_passing_cuts_byfile[0] += 1.0
		###########################################

		###########################################
		#ntracks cut
		if (self.Tree.NumTracks < 2):
			return False

		self.events_passing_cuts[1] += 1.0
		self.events_passing_cuts_byfile[1] += 1.0
		###########################################

		###########################################
		#nvertices cut
		if self.Tree.NumVertices == 0:
			return False

		self.events_passing_cuts[2] += 1.0
		self.events_passing_cuts_byfile[2] += 1.0
		###########################################

		###########################################
		#fiducial vertex cut
		if not self.det.inBox(self.Tree.Vertex_x[0], self.Tree.Vertex_y[0], self.Tree.Vertex_z[0]):
			return False

		self.events_passing_cuts[3] += 1.0
		self.events_passing_cuts_byfile[3] += 1.0
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

		if len(bottom_layer_expected_hits) < 3:
			return False


		self.events_passing_cuts[4] += 1.0
		self.events_passing_cuts_byfile[4] += 1.0
		###########################################

		###########################################
		#vertex before track cut


		return True


	def Plot1D(self, branch_name):
		plotvar = 0.0
		self.Tree.SetBranchStatus("")
