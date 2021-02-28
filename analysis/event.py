import numpy as np
import physics
import visualization
from detector import Detector
import util

#########################################################################################
### DEFINITION OF EVENT CLASS ###########################################################


class Event:
	visEngine = visualization.Visualizer()
	###########################################################################################################################################################################
	TRUTH_PARTICLE_E_THRESHOLD = 0.05 #MeV

	t0 = 0.0
	tm = 0.0

	globalTime = 0.0
	timeResolution = 1.0 #ns
	timeRangeCut = 0.1 #ns

	tracksAtGlobalTime = []

	truthTrackList = []
	recoTrackList = []
	recoVertexList = []
	digiHitList = []
	simHitList = []
	###########################################################################################################################################################################

	###########################################################################################################################################################################
	def __init__(self, Tree, EventNumber):
		self.EventNumber = EventNumber
		self.Tree = Tree
		self.Tree.SetBranchStatus("*", 0)
		
	###########################################################################################################################################################################

	###########################################################################################################################################################################
	def ExtractTruthPhysics(self):
		self.Tree.SetBranchStatus("Hit_x", 1)
		self.Tree.SetBranchStatus("Hit_y", 1)
		self.Tree.SetBranchStatus("Hit_z", 1)
		self.Tree.SetBranchStatus("Hit_particlePdgId", 1)
		self.Tree.SetBranchStatus("Hit_G4ParentTrackId", 1)
		self.Tree.SetBranchStatus("Hit_G4TrackId", 1)
		self.Tree.SetBranchStatus("Hit_particlePx", 1)
		self.Tree.SetBranchStatus("Hit_particlePy", 1)
		self.Tree.SetBranchStatus("Hit_particlePz", 1)
		self.Tree.SetBranchStatus("Hit_particleEnergy", 1)
		
		self.Tree.GetEntry(self.EventNumber)


		particleSet = set()

		for hitn in range(int(self.Tree.NumHits)):
			if self.Tree.Hit_particleEnergy[hitn] > self.TRUTH_PARTICLE_E_THRESHOLD:
				particleSet.add( physics.Particle( int(self.Tree.Hit_G4TrackId[hitn]), int(self.Tree.Hit_particlePdgId[hitn]), int(self.Tree.Hit_G4ParentTrackId[hitn]) ))

		#print(particleSet)
		for particle in particleSet:
			currentTrack = physics.Track(particle)
			for hitn in range(int(self.Tree.NumHits)):
				if ( int(self.Tree.Hit_G4TrackId[hitn]) == particle.trackID):
					time = self.Tree.Hit_time[hitn]
					location = physics.Vector(self.Tree.Hit_x[hitn], self.Tree.Hit_y[hitn], self.Tree.Hit_z[hitn])
					energy = self.Tree.Hit_particleEnergy[hitn]
					momentum = physics.Vector( self.Tree.Hit_particlePx[hitn], self.Tree.Hit_particlePy[hitn], self.Tree.Hit_particlePz[hitn] )
					point = physics.TrackPoint(time, location, energy, momentum)
					currentTrack.AddPoint(point)
					
			if (len(currentTrack.pointList)) <= 2:
				continue
	
			if currentTrack.TimeRange() < self.timeRangeCut:
				continue

			currentTrack.pointList.sort()

			self.truthTrackList.append(currentTrack)

		self.ResetTracks()
		self.truthTrackList.sort()
		self.t0 = min([track.pointList[0].time for track in self.truthTrackList])
		self.tm = max([track.pointList[len(track.pointList)-1].time for track in self.truthTrackList])
	###########################################################################################################################################################################


	###########################################################################################################################################################################
	###########################################################################################################################################################################


	##########################################################################################################################################################################
	def Print(self):
		self.TruthAtTime(self.tm)
		for track in self.truthTrackList:
			print(track)
		colors = [self.truthTrackList[n].color() for n in range(len(self.truthTrackList))]
		self.visEngine.TrackDisplay(self.tracksAtGlobalTime, colors)
		self.visEngine.Draw()

	def ResetTracks(self):
		self.tracksAtGlobalTime = [ [] for x in range(len(self.truthTrackList))  ]
		self.globalTime = self.t0

	def StepParticles(self):
		self.globalTime += self.timeResolution

		for n, track in enumerate(self.truthTrackList):
			self.tracksAtGlobalTime[n].append(track.PointAtTime(self.globalTime))


	#returns location of particles at a given time t, called by visulaization engine
	def TruthAtTime(self, t):
		if ( np.absolute(self.globalTime - t) < self.timeResolution ):
			return self.tracksAtGlobalTime

		if (t < self.globalTime):
			self.globalTime = self.t0
			self.ResetTracks()

		while (self.globalTime < t):
			self.StepParticles()

		return self.tracksAtGlobalTime

	#draw reconstructed tracks in detector det
	def DrawReco(self):
		list_of_trackPt_lists = []
		list_of_colors = []
		det = Detector()

		self.Tree.SetBranchStatus("Track_x0", 1)
		self.Tree.SetBranchStatus("Track_y0", 1)
		self.Tree.SetBranchStatus("Track_z0", 1)
		self.Tree.SetBranchStatus("Track_velX", 1)
		self.Tree.SetBranchStatus("Track_velY", 1)
		self.Tree.SetBranchStatus("Track_velZ", 1)

		self.Tree.GetEntry(self.EventNumber)

		for trackNumber in range(int(self.Tree.NumTracks)):
			x0, y0, z0 = self.Tree.Track_x0[trackNumber], self.Tree.Track_y0[trackNumber], self.Tree.Track_z0[trackNumber]
			vx, vy, vz = self.Tree.Track_velX[trackNumber], self.Tree.Track_velY[trackNumber], self.Tree.Track_velZ[trackNumber]
			xl, yl, zl = det.RecoTrackPoints(x0, y0, z0, vx, vy, vz)
			list_of_trackPt_lists.append( [ physics.RecoTrackPt( xl[n], yl[n], zl[n]  ) for n in range(len(xl)) ] )
			list_of_colors.append(list_of_trackPt_lists[trackNumber][0].c)


		self.visEngine.TrackDisplay(list_of_trackPt_lists, list_of_colors)
		self.visEngine.Draw()

	def GetRecoInfo(self):
		self.Tree.SetBranchStatus("Digi_x", 1)
		self.Tree.SetBranchStatus("Digi_y", 1)
		self.Tree.SetBranchStatus("Digi_z", 1)
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
		self.Tree.SetBranchStatus("Track_expectedHitLayer", 1)
		self.Tree.SetBranchStatus("track_ipDistance", 1)
		self.Tree.SetBranchStatus("Track_hitIndices", 1)
		self.Tree.SetBranchStatus("Track_beta", 1)
		self.Tree.SetBranchStatus("Track_ErrorBeta", 1)

		self.Tree.GetEntry(self.EventNumber)

		print("Number of Tracks: " + str(self.Tree.NumTracks))

		associated_digis = util.unzip(self.Tree.Track_hitIndices)
		missing_hits     = util.unzip(self.Tree.Track_missingHitLayer)
		expected_hits    = util.unzip(self.Tree.Track_expectedHitLayer)

		for n in range(int(self.Tree.NumTracks)):
			print("**Track: " + str(n) + "**")
			print("Start Point: (" + str(self.Tree.Track_x0[n]) + ", " + str(self.Tree.Track_y0[n]) + ", " + str(self.Tree.Track_z0[n]) + ")")
			print("Velocity:    (" + str(self.Tree.Track_velX[n]) + ", " + str(self.Tree.Track_velY[n]) + ", " + str(self.Tree.Track_velZ[n]) + ")")
			print("Beta: " + str(self.Tree.Track_beta[n]) + " +/- " + str(self.Tree.Track_ErrorBeta[n]))
			print("Digis: ")
			for digi_index in associated_digis[n]:
				print("--Digi " + str(digi_index))
				print("--(" + str(self.Tree.Digi_x[digi_index]) + ", " + str(self.Tree.Digi_y[digi_index]) + ", " + str(self.Tree.Digi_z[digi_index]) + ")" )
			print("Missing Hits in Layers:  " + str(missing_hits[n]))
			print("Expected Hits in Layers: " + str(expected_hits[n]))


		

















			





