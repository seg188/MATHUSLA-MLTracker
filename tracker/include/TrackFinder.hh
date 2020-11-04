#include "physics.hh"
#include "globals.hh"
#include <TMath.h>
#include <TRandom.h>
#include "Geometry.hh"

#ifndef TF_DEFINE
#define TF_DEFINE



class seed{
public:
	double score;
	std::pair<physics::digi_hit*, physics::digi_hit*> hits;
	seed() {}
	seed(physics::digi_hit* hit1, physics::digi_hit* hit2) : hits(hit1, hit2)
	{  }

	std::vector<double> guess(){
		double x0 = hits.first->x;
		double y0 = hits.first->y;
		double z0 = hits.first->z;

		double dx = hits.second->x - x0;
		double dy = hits.second->y - y0;
		double dz = hits.second->z - z0;
		double dt = hits.second->t - hits.first->t;

		return {x0, y0, z0, dx/dt, dy/dt, dz/dt, hits.first->t };

	}

	template<typename hit>
	double time_difference(hit AHit){
		std::vector<double> pars = guess();

		double seed_t = (AHit->y - pars[1])/pars[4];

		double hit_t = AHit->t - hits.first->t;

		return TMath::Abs(seed_t - hit_t);

	}

	template<typename hit>
	double timeless_residual(hit AHit){

		//calculate residual from the track using the two hits 
		//(assuming a straight line between them)

		//here we calculate the velocity

		//std::cout << "first hit: " << std::endl;
		//std::cout << "{" << hits.first->x << ", " << hits.first->y << ", " << hits.first->z << ", " << hits.first->t << "}" << std::endl;
		//std::cout << "second hit: " << std::endl;
    	//std::cout << "{" << hits.second->x << ", " << hits.second->y << ", " << hits.second->z << ", " << hits.second->t << "}" << std::endl;
		
		double x0 = hits.first->x;
		double y0 = hits.first->y;
		double z0 = hits.first->z;
		double t0 = hits.first->t;

		double dx = hits.second->x - x0;
		double dy = hits.second->y - y0;
		double dz = hits.second->z - z0;
		double dt = hits.second->t - t0;

		double vx = dx/dt;
		double vy = dy/dt;
		double vz = dz/dt;

	//	std::cout << x0 << ", " << y0 << ", " << z0 << ", " << vx << ", " << vy << ", " << vz << ", " << dt << std::endl;

		//NOW we use the TIMELESS residual!!!
		//this gives us a measure of how far the hit is from the track when the track would be in that layer

		double y1 = AHit->y;
		double x1 = AHit->x;
		double z1 = AHit->z;

		double delta_t = (y1 - y0)/vy;
		
		double expected_x = x0 + delta_t*vx;
		double expected_z = z0 + delta_t*vz;

		double res2 = (x1 - expected_x)*(x1 - expected_x) + (z1 - expected_z)*(z1 - expected_z);





		return TMath::Sqrt(res2);

	}
 

};


class TrackFinder{
public:
	std::vector<physics::digi_hit*> hits;
	std::vector<seed> seeds;
	std::vector<physics::track*> tracks;


	void CalculateMissingHits(Geometry* geo);

	void clear(){ 
		seeds.clear();
		for (auto hit : hits) delete hit;
		hits.clear();
		for (auto tr : tracks) delete tr;
		tracks.clear();
	}
	seed first_seed;
	int first_n_to_delete = 0;
	void Seed();
	void FindTracks();
	void CleanTracks();
	void Reseed(bool);
	void CheckSeeds();

	double _score();
	double c_score(physics::digi_hit* hit1, physics::digi_hit* hit2){
		
		double dx = hit1->x - hit2->x;
		double dy = hit1->y - hit2->y;
		double dz = hit1->z - hit2->z;
		double dt = hit1->t - hit2->t;
	
		return TMath::Abs( (dx*dx + dy*dy + dz*dz)/(constants::c*constants::c ) - dt*dt  );
	}//c_score

	double c_score(const seed &s){
		auto val = c_score(s.hits.first, s.hits.second);;

		return val;
	}

	void score_seeds(){
		for (auto seed : seeds) seed.score = c_score(seed);
	}

	int min_seed( ){ //sorts by c_compatability score

		int min_index = -1;
		int min_val = cuts::seed_ds2;
		int j = 0;
		for (auto seed : seeds){
			if (seed.score < min_val){
				min_index = j;
				min_val = seed.score;
			}

			j++;
		}
	
		return min_index;
	}

}; //TrackFinder



#endif