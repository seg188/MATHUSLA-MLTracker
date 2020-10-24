#include <iostream>
#include "units.hh"
#include "Geometry.hh"
#include "physics.hh"


#ifndef DIGI_DEFINE
#define DIGI_DEFINE




class Digitizer{
public:
	std::vector<physics::sim_hit*> hits{};
	void Digitize();
	//std::vector<physics::digi_hit*> Digitize();
	Geometry* _geometry;

	void AddHit(physics::sim_hit &hit){hits.push_back(&hit);}

	Digitizer(){ _geometry = new Geometry; }

	~Digitizer() 
	{
		delete _geometry;
	}


	



private:


}; //Digitizer




#endif