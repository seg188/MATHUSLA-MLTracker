#include "physics.hh"

#ifndef VF_H
#define VF_H

class VertexFinder{
public:

	std::vector<physics::track*> tracks;

	void clear(){
		tracks.clear();
	}

	void FindVertices();

}; //class VertexFinder




#endif