#include<iostream>
#include <TLorentzVector.h>
#include "Geometry.hh"
#include "units.hh"
#ifndef PHYSICS_DEFINE
#define PHYSICS_DEFINE

namespace physics{

	
	
	//defines detector hit
	class sim_hit{
	public:

		sim_hit(double _x, double _y, double _z, double _t, double _e){
			x = _x;
			y = _y;
			z = _z;
			t = _t;
			e = _e;
		}
		std::size_t index;
		double x;
		double y;
		double z;
		double t;
		double e;
		detID det_id;

	
	}; //sim



	class digi_hit{
	public:
		detID det_id;
		std::size_t index;
		double x, ex;
		double y, ey;
		double z, ez;
		double t;
		double e;
		double et = detector::time_resolution;

		std::vector<sim_hit*> hits;

		void AddHit(sim_hit* hit){hits.push_back(hit);}



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