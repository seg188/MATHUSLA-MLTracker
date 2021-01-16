import numpy as np
import physics
import visualization
#########################################################################################
### DEFINITION OF EVENT CLASS ###########################################################


class Event:
	visEngine = visualization.Visualizer()
	###########################################################################################################################################################################
	TRUTH_PARTICLE_E_THRESHOLD = 0.25 #MeV

	t0 = 0.0
	tm = 0.0

	globalTime = 0.0
	timeResolution = 1.0 #ns
	timeRangeCut = 2.0 #ns

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

		#self.ExtractTruthPhysics()
		#self.RecordRecoPhysics()
	###########################################################################################################################################################################

	###########################################################################################################################################################################
	def ExtractTruthPhysics(self):
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
			print(track.TimeRange())
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












			





