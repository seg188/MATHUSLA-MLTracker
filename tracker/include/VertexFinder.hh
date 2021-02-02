#include "physics.hh"
#include "LinearAlgebra.hh"

#ifndef VF_H
#define VF_H

class vertex_seed{
public:
	double score(){return tracks.first->closest_approach(tracks.second);}
	std::pair<physics::track*, physics::track*> tracks;
	vertex_seed() {}
	vertex_seed(physics::track* track1, physics::track* track2) : tracks(track1, track2)
	{  }

	double closest_approach(physics::track* tr){

		double ca1 = tracks.first->closest_approach(tr);
		double ca2 = tracks.second->closest_approach(tr);

		return ca1 < ca2 ? ca1 : ca2; 
	}

	vector::Vector guess(){

		return tracks.first->closest_approach_midpoint(tracks.second);
	}
};

class VertexFinder{
public:

	std::vector<physics::track*> tracks;
	std::vector<physics::vertex*> vertices;
	std::vector<vertex_seed> seeds;

	int missedChi2 = 0;
	int noConverge = 0;

	void Seed();

	void clear(){
		tracks.clear();
		for (auto v : vertices) delete v;
		vertices.clear();
		seeds.clear();
	}

	void FindVertices();

}; //class VertexFinder




#endif