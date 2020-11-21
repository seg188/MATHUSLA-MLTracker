#include<iostream>
#include <TLorentzVector.h>
#include "Geometry.hh"
#include "globals.hh"
#include "TFitter.h"
#include "TMatrix.h"
#include "TMatrixD.h"
#include "LinearAlgebra.hh"


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

	class vertex{
	public:
		double x, y, z, t;
		std::vector<int> track_indices;

		vertex(std::vector<double> pars){
			x = pars[0];
			y = pars[1];
			z = pars[2];
			t = pars[3];
		}

		vertex(){}
	};

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
		std::vector<int> _missing_layers;
		TMatrixD cov_matrix;

		template<typename matrix>
		void CovMatrix(matrix mat, int size){

			cov_matrix.ResizeTo(size, size);
			for (int i = 0; i < size; i++){
				for (int j = i; j < size; j++){
				
					cov_matrix[i][j] = mat[i][j];
					cov_matrix[j][i] = cov_matrix[i][j];
				}
			}	

		}

		void missing_layers(std::vector<int> layers){_missing_layers = layers; };

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

    	double ex2 = (hit->ex)*(hit->ex);
    	double ez2 = (hit->ez)*(hit->ez);

    	double res2 = (track_x - hit->x)*(track_x - hit->x)/ex2 + (track_z - hit->z)*(track_z - hit->z)/ez2;
    	return TMath::Sqrt(  res2  );
    }

    template<typename ahit>
    double distance_to_hit(ahit* hit){

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

    	double ex2 = (hit->ex)*(hit->ex);
    	double ey2 = (hit->ey)*(hit->ey);
    	double ez2 = (hit->ez)*(hit->ez);

    	double res2 = (track_x - hit->x)*(track_x - hit->x)/ex2 + (track_y - hit->y)*(track_y - hit->y)/ey2 + (track_z - hit->z)*(track_z - hit->z)/ez2;
    	return TMath::Sqrt(  res2  );
    }

    template<typename ahit>
    double time_difference(ahit* hit){
    	
    	//calculate the time the track particle would enter layer

    	double t_track = (hit->y - y0)/vy;
    	double t_hit = hit->t - t0;
 	
    	return TMath::Abs(t_track - t_hit)/hit->et;
    }


    int nlayers(){
    	//returns the number of layers that a track has hits in
    	std::vector<int> layer_indices;
    	for (auto hit : hits){
    		bool new_layer = true;
    		int layer_index = hit->det_id.layerIndex;
    		for (int layer_n : layer_indices){
    			if (layer_n == layer_index){
    				new_layer = false;
    				break;
    			} 
    		}

	    	if (new_layer) layer_indices.push_back(layer_index);

    	}

    	return layer_indices.size();
    } //nlayers

    std::vector<int> layers(){
    	//returns  layers that a track has hits in
    	std::vector<int> layer_indices;
    	for (auto hit : hits){
    		bool new_layer = true;
    		int layer_index = hit->det_id.layerIndex;
    		for (int layer_n : layer_indices){
    			if (layer_n == layer_index){
    				new_layer = false;
    				break;
    			} 
    		}

	    	if (new_layer) layer_indices.push_back(layer_index);

    	}

    	return layer_indices;
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


    std::vector<double> Position_at_Y(double y){

    	double delta_t = (y-y0)/vy;

    	//if (delta_t < 0) return {0.,0.,0.};

    	return { x0 + delta_t*vx, y, z0 + delta_t*vz    };
    }

    std::vector<double> direction(){ 

    	double velocity = beta()*constants::c;
    	return { vx/velocity, vy/velocity, vz/velocity };
    }


    std::vector<double> position(double t){ //global time t

    
    	double dt = t-t0;

    	return {x0 + vx*dt, y0 + vy*dt, z0 + vz*dt};
    }


    double distance_to(double x, double y, double z, double t){

    	auto pos = position(t);

    	return TMath::Sqrt( (pos[0] - x)*(pos[0] - x) + (pos[1] - y)*(pos[1] - y) + (pos[2] - z)*(pos[2] - z)     );

    }

    double err_distance_to(double x, double y, double z, double t){

    	std::vector<double> derivatives = {0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0}; //partial derivates of position_at
    	double dist = distance_to(x, y, z, t);

    	derivatives[0] = ((t-t0)*vx - x + x0)/dist;
    	derivatives[1] = detector::scintillator_height;
    	derivatives[2] = ((t-t0)*vz - z + z0)/dist;
    	derivatives[3] = (t-t0)*((t-t0)*vx - x + x0)/dist;
    	derivatives[4] = (t-t0)*((t-t0)*vy - y + y0)/dist;
    	derivatives[5] = (t-t0)*((t-t0)*vz - z + z0)/dist;
    	derivatives[6] = -1.0*(vx*((t-t0)*vx - x + x0) + vy*((t-t0)*vy - y + y0) + vz*((t-t0)*vz - z + z0))/dist;

    	//now we calculate the actual error
    	double error = 0.0;

    	for (int i = 0; i < derivatives.size(); i++){
    		for (int j = 0; j < derivatives.size(); j++){
    			
    			error += derivatives[i]*derivatives[j]*cov_matrix[i][j];
    			
    		}
    	}

    	return TMath::Sqrt(error);
    }

    double vertex_residual(std::vector<double> params){

    	double x = params[0];
    	double y = params[1];
    	double z = params[2];
    	double t = params[3];

    	return distance_to(x, y, z, t)/err_distance_to(x, y, z, t);
    }

    double closest_approach(track* tr2){

    	using namespace vector;

    	std::vector<double> rel_v = { tr2->vx - vx, tr2->vy - vy, tr2->vz - vz  };

    	double rel_v2 = dot(rel_v, rel_v);

    	std::vector<double> displacement = {x0 - tr2->x0 , y0 - tr2->y0 , z0 - tr2->z0  };

    	double t_ca  = ( dot(displacement, rel_v)/rel_v2 ) - (   dot( add(scaler_multiply(-1.0*tr2->t0, {tr2->vx, tr2->vy, tr2->vz}), scaler_multiply(1.0*t0, {vx, vy, vz})), rel_v)/rel_v2  );    	

    	std::vector<double> pos1 = {x0 + (t_ca - t0)*vx, y0 + (t_ca - t0)*vy, z0 + (t_ca - t0)*vz };
    	std::vector<double> pos2 = {tr2->x0 + (t_ca - tr2->t0)*tr2->vx, tr2->y0 + (t_ca - tr2->t0)*tr2->vy, tr2->z0 + (t_ca - tr2->t0)*tr2->vz };

    	auto disp = add(pos1, scaler_multiply(-1.0, pos2));

    	return TMath::Sqrt( dot(disp, disp)      );
    }

    std::vector<double> closest_approach_midpoint(track* tr2){

    	using namespace vector;

    	std::vector<double> rel_v = { tr2->vx - vx, tr2->vy - vy, tr2->vz - vz  };

    	double rel_v2 = dot(rel_v, rel_v);

    	std::vector<double> displacement = { tr2->x0 - x0, tr2->y0 - y0, tr2->z0 - z0  };

    	double t_ca  = ( dot(displacement, rel_v)/rel_v2 ) - (   dot(add(scaler_multiply(-1.0*tr2->t0, {tr2->vx, tr2->vy, tr2->vz}), scaler_multiply(1.0*t0, {vx, vy, vz})), rel_v)/rel_v2  );    	

    	std::vector<double> pos1 = {x0 + (t_ca - t0)*vx, y0 + (t_ca - t0)*vy, z0 + (t_ca - t0)*vz, t_ca };
    	std::vector<double> pos2 = {tr2->x0 + (t_ca - tr2->t0)*tr2->vx, tr2->y0 + (t_ca - tr2->t0)*tr2->vy, tr2->z0 + (t_ca - tr2->t0)*tr2->vz, t_ca };

    	auto sum = add(pos1, pos2);

    	return scaler_multiply(0.50, sum) ;
    }




	}; //track
  

};



#endif