#include<iostream>
#include <TLorentzVector.h>


#ifndef PHYSICS_DEFINE
#define PHYSICS_DEFINE

namespace physics{

	//defines detector hit
	class sim_hit{
	public:
		sim_hit(double _x, double _y, double _z, double _t){
			x = _x;
			y = _y;
			z = _z;
			t = _t;
		}

		std::size_t index;
		double x;
		double y;
		double z;
		double t;
	}; //sim

	class digi_hit{
	public:
		std::size_t index;
		double x, ex;
		double y, ey;
		double z, ez;
		double t, et;
		std::vector<sim_hit*> comp_hits;
	}; //digi

	class track{
	public:
		std::size_t index;
		double vx, evx;
		double vy, evy;
		double vz, evz;
		double x0, y0, z0;
		std::vector<digi_hit*> hit;
	}; //track

};



#endif