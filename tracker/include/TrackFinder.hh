#include "physics.hh"
#include "globals.hh"
#include "LinearAlgebra.hh"
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

	vector::Vector VelVector(){
		auto P1 = hits.first->PosVector();
		auto P2 = hits.second->PosVector();
		double dt = hits.second->t - hits.first->t;

		return (P2 - P1).Scale(1.0/dt);
	}

	std::vector<double> guess(){
		auto P1 = hits.first->PosVector();
		auto velocity = VelVector();

		return {P1.x, P1.y, P1.z, velocity.x, velocity.y, velocity.z, hits.first->t };

	}

	template<typename hit>
	double time_difference(hit AHit){

		auto P1 = hits.first->PosVector();
		auto vel = VelVector();
		double seed_t = (AHit->y - P1.y)/vel.y;

		double hit_t = AHit->t - hits.first->t;

		return TMath::Abs(seed_t - hit_t)/AHit->et;;

	}

	template<typename hit>
	double timeless_residual(hit AHit){

		//calculate residual from the track using the two hits 
		//(assuming a straight line between them)

		auto P1 = hits.first->PosVector();
		auto velocity = VelVector();

		//NOW we use the TIMELESS residual!!!
		//this gives us a measure of how far the hit is from the track when the track would be in that layer

		auto HitP = AHit->PosVector();
		double delta_t = (HitP.y - P1.y)/velocity.y;
		auto expectedPos = P1 + velocity.Scale(delta_t);
		auto errMetric = vector::Vector(pow(AHit->ex, 2), pow(AHit->ex, 2), pow(AHit->ex, 2));
		
		return (expectedPos - HitP).Magnitude(errMetric);

	}

	template<typename hit>
	double distance_to_hit(hit AHit){

		auto P1 = hits.first->PosVector();
		auto velocity = VelVector();

		//NOW we use the TIMELESS residual!!!
		//this gives us a measure of how far the hit is from the track when the track would be in that layer

		auto HitP = AHit->PosVector();
		double delta_t = (HitP.y - P1.y)/velocity.y;
		auto expectedPos = P1 + velocity.Scale(delta_t);

		return (expectedPos - HitP).Magnitude();
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
	void MergeTracks();

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