#include "TrackFinder.hh"
#include "globals.hh"
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

	int index = 0;
	int total_hits = hits.size();
	bool iterate = true;	
	int j = 0;
	int MAX_ITS = 25;

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

		for (auto hit : hits){\


			if ( (current_seed.timeless_residual(hit) < cuts::seed_residual or current_seed.distance_to_hit(hit) < cuts::distance_to_hit) 
													and current_seed.time_difference(hit) < cuts::seed_time_difference) 
			{
				track_pts.push_back(hit);
			} else {

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
	
		if (track_status == 4) continue; //fit failed


		auto current_track = new physics::track( fitter.parameters, fitter.parameter_errors);
		for (auto hit : track_pts) current_track->AddHit(hit);


		//first pass track is now cconstructed

		std::vector<physics::digi_hit*> second_unused_hits;

		for (auto hit : unused_hits){
			if ( (current_track->untimed_residual(hit) < cuts::residual_add or current_track->distance_to_hit(hit) < cuts::distance_to_hit) 
																			and current_track->time_difference(hit) < cuts::seed_time_difference )
			{
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
			if (current_track->untimed_residual(hit) > cuts::residual_drop or current_track->time_difference(hit) > cuts::time_difference_drop){
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
		current_track->CovMatrix(fitter.cov_matrix, fitter.npar);

		
		if ( current_track->nlayers() >= cuts::track_nlayers and current_track->chi2_per_dof() < cuts::track_chi2 and current_track->hits.size() > cuts::ntrack_hits) {
			current_track->index = index++;
			tracks.push_back(current_track);

			
		} else {
			delete current_track;
			continue;
		}

		hits = second_unused_hits;

		if (seeds.size() == 0) iterate = false;
		if (hits.size() < cuts::nseed_hits) iterate = false;

	} //while iterate



	//MergeTracks();
	//CleanTracks();

	int total_tracked_points = 0;

	for (auto track : tracks) total_tracked_points += track->hits.size();

	if ( (total_hits - hits.size() - total_tracked_points) != 0 ){
		std::cout << "total: " << total_hits << std::endl;
		std::cout << "used: " << total_tracked_points << std::endl;
		std::cout << "unused:" << hits.size() << std::endl;
	}

	if (j++ > MAX_ITS) iterate = false;
	
}

void TrackFinder::MergeTracks(){

	//at this point, all of the points have been fit to tracks. At this point, we will perform the track merging step. 

	if (tracks.size() == 0 or tracks.size() == 1) return;



	std::vector<int> deleted_tracks = {};

	for (int first_track = 0; first_track < tracks.size(); first_track++){
		for (int second_track = first_track+1; second_track < tracks.size(); second_track++){

			auto tr1 = tracks[first_track];
			auto tr2 = tracks[second_track];

			auto first_layer = tr1->layers()[0] < tr2->layers()[0] ? tr1->layers()[0] : tr2->layers()[0];

			auto d1 = tr1->direction();
			auto d2 = tr2->direction();

			int tr1_missing_hits = 0;
			int tr2_missing_hits = 0;


			auto cos_theta = d1 ^ d2;

			double distance = tr1->closest_approach(tr2);

			if (distance > cuts::merge_distance or cos_theta < cuts::merge_cos_theta) continue;

			//at this point, we need to check if they have a certain number of missing hits

			//if (tr1->_missing_layers.size() < 3 or tr2->_missing_layers.size() < 3) continue;
			std::vector<int> joint_missing_hit_layers = {};
			for (int i = 0; i < tr1->_missing_layers.size(); i++){
				auto layer = tr1->_missing_layers[i];
				if (layer < first_layer) continue;
				tr1_missing_hits++;
				
				bool missing = true;
				for (int j = 0; j < tr2->_missing_layers.size(); j++){

					auto layer2 = tr2->_missing_layers[j];

					if (layer2 == layer){
						missing = false;
						continue;
					}
				}

				if (missing) joint_missing_hit_layers.push_back(layer);
			}

			for (int i = 0; i < tr2->_missing_layers.size(); i++){
				auto layer = tr2->_missing_layers[i];
				if (layer < first_layer) continue;
				tr2_missing_hits++;
				bool missing = true;
				for (int j = 0; j < tr1->_missing_layers.size(); j++){

					auto layer2 = tr2->_missing_layers[j];

					if (layer2 == layer){
						missing = false;
						continue;
					}
				}

				for (int j = 0; j < joint_missing_hit_layers.size(); j++){

					auto layer2 = joint_missing_hit_layers[j];

					if (layer2 == layer){
						missing = false;
						continue;
					}
				}

				if (missing) joint_missing_hit_layers.push_back(layer);
			}

			bool merge = false;
			
			if ( joint_missing_hit_layers.size() < 3  and  (tr1_missing_hits > 2 or tr2_missing_hits > 2) ) merge = true;

			if (!merge) continue;


			for (auto hit : tr2->hits) tr1->AddHit(hit);

			TrackFitter fitter;

			fitter.fit(tr1->hits, tr1->parameters());
			tr1->parameters(fitter.parameters);
			tr1->par_errors(fitter.parameter_errors);

			deleted_tracks.push_back(second_track);
		
		} //second track
	} //first track



	std::vector<physics::track*> good_tracks;

	for (int k = 0; k < tracks.size(); k++){

		bool add = true;
		for (int del_index : deleted_tracks) {
			if (del_index == k) add = false;
		}

		if (add){
			good_tracks.push_back(tracks[k]);
		} 

	}


	tracks = good_tracks;

}

void TrackFinder::CleanTracks(){


	//we clean the tracks with the following critera:
	//-

	if (tracks.size() < 2) return;


	for (int first_track = 0; first_track < tracks.size(); first_track++){
		for (int second_track = first_track+1; second_track < tracks.size(); second_track++){
			auto tr1 = tracks[first_track];
			auto tr2 = tracks[second_track];

			if (tr1->hits.size() < cuts::cleaning_nhits or tr2->hits.size() < cuts::cleaning_nhits) continue;

			std::cout << "clean me" << std::endl;

		}//second track
	}//first track



}


std::vector<physics::digi_hit*> TrackFitter::digi_list = {};
std::vector<double> TrackFitter::parameters = {};
std::vector<double> TrackFitter::parameter_errors = {};
double TrackFitter::cov_matrix[TrackFitter::npar][TrackFitter::npar];

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
		//std::cout << "new track " << std::endl;
		std::vector<int> layers = track->layers();
		std::vector<int> expected_layers;

		int layer_n = 0;
		for (auto layer_lims : detector::LAYERS_Y){

			double y_center = (layer_lims[0] + layer_lims[1])/2.0;
			auto track_position = track->Position_at_Y(y_center);

			if (track_position.x > detector::x_min and track_position.x < detector::x_max){
				if (track_position.z > detector::z_min and track_position.z < detector::z_max){
					if ( ! (geo->GetDetID(track_position).IsNull()) ) expected_layers.push_back(layer_n);
				}
			}

			layer_n++;
		}

		track->SetExpectedLayers(expected_layers);

		std::vector<int> missing_layers;

		for (auto expected_index : expected_layers){
			
			bool missing = true; //flag to indicate if the "expected_index" for the layer is missing or not

			for (auto existing_index : layers){
				if (expected_index == existing_index) missing = false;
			}


			bool already_counted = false;
			if (missing){
				for (auto _index : missing_layers){
					if (expected_index == _index) already_counted = true;
				}

				if (!already_counted) {
				//	std::cout << expected_index << std::endl;
					missing_layers.push_back(expected_index);
				}
			} //if missing

		}

		track->missing_layers(missing_layers);


	}


}