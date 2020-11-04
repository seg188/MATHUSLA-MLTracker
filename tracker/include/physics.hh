#include<iostream>
#include <TLorentzVector.h>
#include "Geometry.hh"
#include "units.hh"
#include "TFitter.h"


#ifndef PHYSICS_DEFINE
#define PHYSICS_DEFINE

namespace physics{


	
	
	//defines detector hit
	class sim_hit{
	public:

		sim_hit(int _index, double _x, double _y, double _z, double _t, double _e){
			index = _index;
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
		double ex0, ey0, ez0;
		double t0, et0;
		std::vector<int> hits_to_drop = {};

		void Refit();

		std::vector<digi_hit*> hits;
		void AddHit(physics::digi_hit* hit){ hits.push_back(hit); }
		track(){}
		track(std::vector<double> params, std::vector<double> par_errors){
			x0 = params[0]; ex0 = par_errors[0];
			y0 = params[1]; ey0 = par_errors[1];
			z0 = params[2]; ez0 = par_errors[2];
			vx = params[3]; evx = par_errors[3];
			vy = params[4]; evy = par_errors[4];
			vz = params[5]; evz = par_errors[5];
			if (params.size() == 7) {
				t0 = params[6];
				et0 = params[6];
			}

		}

		std::vector<double> parameters(){
			std::vector<double> p = { x0, y0, z0, vx, vy, vz };
			return p;
		}

		void parameters(std::vector<double> pars){
			x0 = pars[0];
			y0 = pars[1];
			z0 = pars[2];
			vx = pars[3];
			vy = pars[4];
			vz = pars[5];
			if (pars.size() == 7) t0 = pars[6];
		}

		void par_errors(std::vector<double> epars){
			ex0 = epars[0];
			ey0 = epars[1];
			ez0 = epars[2];
			evx = epars[3];
			evy = epars[4];
			evz = epars[5];
			if (epars.size() == 7) et0 = epars[6];
		}

		double chi2(){
			double chi_2 = 0.0;
			double t;
			double res_t, res_x, res_z;
			for (auto hit : hits){
				t = (hit->y - y0)/vy;
				
				res_x = ((x0 + vx*t) - hit->x)/hit->ex;
				res_z = ((z0 + vz*t) - hit->z)/hit->ez;

			//	res_t = ( (t0 + t) - hit->t)/hit->et;

				chi_2 +=  res_x*res_x + res_z*res_z;

			}

			return chi_2;
		}

      double chi2_per_dof(){
      	int n_track_params = 6;
      	int ndof = (4.0*hits.size() - n_track_params );
      	if (ndof < 1) ndof = 1;
      	std::cout << chi2()/ndof << std::endl;
      	return chi2()/ndof; //FIX ME
      }

      double beta(){
      	return TMath::Sqrt( vx*vx + vy*vy + vz*vz  )/constants::c;
      }

      double beta_err(){
      	return 2.0*TMath::Sqrt( vx*vx*evx*evx +  vy*vy*evy*evy + vz*vz*evz*evz)/constants::c;
      }

    template<typename ahit>
    double untimed_residual(ahit* hit){
    	
    	double hit_y = hit->y;

    	double track_delta_t = (hit_y - y0)/vy;

    	double track_x = x0 + vx*track_delta_t;
    	double track_z = z0 + vz*track_delta_t;

    	double res2 = (track_x - hit->x)*(track_x - hit->x) + (track_z - hit->z)*(track_z - hit->z);
    	return TMath::Sqrt(  res2  );
    }

    template<typename ahit>
    double residual(ahit* hit){
    	
    	double track_delta_t = hit->t - t0;

    	double track_x = x0 + vx*track_delta_t;
    	double track_y = y0 + vz*track_delta_t;
    	double track_z = z0 + vz*track_delta_t;

    	double res2 = (track_x - hit->x)*(track_x - hit->x) + (track_y - hit->y)*(track_y - hit->y) + (track_z - hit->z)*(track_z - hit->z);
    	return TMath::Sqrt(  res2  );
    }

    int nlayers(){
    	//returns the number of layers that a track has hits in
    	std::vector<int> layer_indices;
    	for (auto hit : hits){

    		int layer_index = hit->det_id.layerIndex;
    		for (int layer_n : layer_indices){
    			if (layer_n == layer_index) break;
    		}

    		layer_indices.push_back(layer_index);
    	}

    	return layer_indices.size();
    } //nlayers

    void AddHitToDrop(int index) { hits_to_drop.push_back(index); } 
    
    void DropHits(){
    	
    	for (int _index : hits_to_drop){

    		int hits_vector_index = 0;

    		for (auto hit : hits){
    			if (hit->index == _index){
    				hits.erase(hits.begin() + hits_vector_index);
    				break;
    			} 

    			hits_vector_index++;
    		}

    	}
    }



	}; //track
  

};



#endif