#include "physics.hh"

#ifndef TF_DEFINE
#define TF_DEFINE


class Digitizer{

	std::vector<physics::sim_hit*> hits;

	int Digitize();

}; //Digitizer

class TrackFinder{
	
	std::vector<physics::digi_hit*> hits;
	int Seed();

private:
	double _score();
	double _c_compatability(int, int);



}; //TrackFinder



#endif