#include "TrackFinder.hh"
#include "units.hh"
#include "physics.hh"
#include <TMath.h>
#include <TRandom.h>
#include "TMinuit.h"
#include "statistics.hh"
#include "Geometry.hh"

void TrackFinder::Seed(){

	seeds.clear();
	seeds = {};

	for (int first = 0; first < hits.size(); first++){
		for (int second = first+1; second < hits.size(); second++){

			int layer1 = ((hits[first])->det_id).layerIndex;
			int layer2 = ((hits[second])->det_id).layerIndex;

			if (layer1 == layer2) continue;
			
			double ds = c_score(hits[first], hits[second]);

			if (ds > cuts::seed_ds2) continue;

			seeds.push_back( seed(hits[first], hits[second]) );

		} //"second" loop
	} //"first" loop

	score_seeds();

	//for (auto seed : seeds) std::cout << c_score(seed.hits.first, seed.hits.second) << std::endl;
	

} //TF::Seed


void TrackFinder::FindTracks(){

	if (seeds.size() == 0) return; //no seeds found in initial seeding, will be retried with <c travel

	//we take the first seed now

	bool iterate = true;	
	int j = 0;
	while (iterate) {
		
		if (seeds.size() == 0) return;
		if (hits.size() == 0) return;

		int min_index = min_seed();
		auto current_seed = seeds[min_index];
		seeds.erase(seeds.begin() + min_index); //delete the seed so that it isn't used again
		
		std::vector<physics::digi_hit*> track_pts;
		std::vector<physics::digi_hit*> unused_hits;

		//now we use the seed::residual function to get the residual from the seed of all of the available hits.
		//if the residual is good, we add it to the track_pts vector 

		for (auto hit : hits){

			if (current_seed.timeless_residual(hit) < cuts::seed_residual and current_seed.time_difference(hit) < cuts::seed_time_difference) {
				track_pts.push_back(hit);
			} else {
				//std::cout << current_seed.timeless_residual(hit) << std::endl;
				unused_hits.push_back(hit);
				
			}
		}

		

		//we check that there are at least cuts::nseed_hits hits in the track_pts
		//if not, we move on to the next seed

		if (track_pts.size() < cuts::nseed_hits) {
			continue;
		}
	

		//at this point, all we have done is erase the seed, and none of the hits have been modified
		TrackFitter fitter;
		auto track_status = fitter.fit(track_pts, current_seed.guess());
	
		//if (track_status == 4) continue;

		auto current_track = new physics::track( fitter.parameters, fitter.parameter_errors);
		for (auto hit : track_pts) current_track->AddHit(hit);


		//first pass track is now cconstructed

		std::vector<physics::digi_hit*> second_unused_hits;

		for (auto hit : unused_hits){
			if (current_track->untimed_residual(hit) < cuts::residual_add and current_seed.time_difference(hit) < cuts::seed_time_difference){
				current_track->AddHit(hit);
			} else {
				second_unused_hits.push_back(hit);
			}
		}


		//NOW WE REFIT AGAIN

		fitter.fit(current_track->hits, current_track->parameters());
		current_track->parameters(fitter.parameters);
		current_track->par_errors(fitter.parameter_errors);
		



		std::vector<physics::digi_hit*> good_hits;
		for (auto hit : current_track->hits){
			if (current_track->untimed_residual(hit) > cuts::residual_drop or current_seed.time_difference(hit) > cuts::time_difference_drop){
				second_unused_hits.push_back(hit);
			} else {
				good_hits.push_back(hit);
			}
		}


		if (good_hits.size() < cuts::nseed_hits) continue;

		current_track->hits = good_hits;

		fitter.fit(current_track->hits, current_track->parameters());
		current_track->parameters(fitter.parameters);
		current_track->par_errors(fitter.parameter_errors);

		
		if ( current_track->nlayers() >= cuts::track_nlayers and current_track->chi2_per_dof() < cuts::track_chi2) {
			tracks.push_back(current_track);
			hits = second_unused_hits;
			
		} else {
			std::cout << "failed chi2 or nlayers cut" << std::endl;
			delete current_track;
			continue;
		}

		

		if (seeds.size() == 0) iterate = false;
		if (hits.size() < cuts::nseed_hits) iterate = false;


	} //while iterate

}


void TrackFinder::CleanTracks(){


	//we clean the tracks with the following critera:
	//-



}


std::vector<physics::digi_hit*> TrackFitter::digi_list = {};
std::vector<double> TrackFitter::parameters = {};
std::vector<double> TrackFitter::parameter_errors = {};
void TrackFitter::chi2_error(int &npar, double *gin, double &f, double *pars, int iflag ){
	
	double x0 = pars[0];
	double y0 = pars[1];
	double z0 = pars[2];
	double vx = pars[3];
	double vy = pars[4];
	double vz = pars[5];
	double t0 = pars[6];

	double error = 0.0 ;


	for (auto hit : TrackFitter::digi_list){
		double t = (hit->t - t0);
		double dt = (hit->y - y0)/vy;
		double expected_x = x0 + dt*vx;
		double expected_z = z0 + dt*vz;
		double _ex = (expected_x - hit->x)/hit->ex; 
		double _ez = (expected_z - hit->z)/hit->ez;
		double _et = (t - dt)/hit->et;  
		error += (_ex*_ex + _ez*_ez) + _et*_et ;
	}

	f = error;
}


void TrackFinder::CalculateMissingHits(Geometry* geo){


	for (auto track : tracks){

		std::vector<int> layers = track->layers();
		std::vector<int> expected_layers;

		int layer_n = 0;
		for (auto layer_lims : detector::LAYERS_Y){

			double y_center = (5.0*layer_lims[0] + layer_lims[1])/6.0;
			auto track_position = track->Position_at_Y(y_center);

			if (track_position[0] > detector::x_min and track_position[0] < detector::x_max){
				if (track_position[2] > detector::z_min and track_position[2] < detector::z_max){
					if ( ! (geo->GetDetID(track_position).IsNull()) ) expected_layers.push_back(layer_n);
				}
			}

			layer_n++;
		}

		std::vector<int> missing_layers;
		for (auto expected_index : expected_layers){
			bool missing = true;
			for (auto existing_index : layers){
				if (expected_index == existing_index) missing = false;
			}

			if (missing) missing_layers.push_back(expected_index);
		}

		track->missing_layers(missing_layers);

	}


}