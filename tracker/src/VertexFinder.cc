#include "globals.hh"
#include "VertexFinder.hh"
#include "statistics.hh"
#include "physics.hh"
#include "LinearAlgebra.hh"

void VertexFinder::Seed(){
	for (int n1 = 0; n1 < tracks.size(); n1++){
		for (int n2 = n1+1; n2 < tracks.size(); n2++){

			auto tr1 = tracks[n1];
			auto tr2 = tracks[n2];

			if (tr1->closest_approach(tr2) < cuts::seed_closest_approach) seeds.push_back( vertex_seed(tr1, tr2)  );

		} //n2
	}//n1

	std::sort( seeds.begin(), seeds.end(), [](vertex_seed a, vertex_seed b)->bool { return a.score() < b.score();  } );
}//VF:Seed

void VertexFinder::FindVertices(){

	if (seeds.size() < 1) return; // no seeds

	
	while (seeds.size() > 0 and tracks.size() > 0){ 

		std::vector<physics::track*> used_tracks = {};
		std::vector<physics::track*> unused_tracks = {};

		auto current_seed = seeds[0];

		seeds.erase(seeds.begin());

		for (auto tr : tracks){
			if (current_seed.closest_approach(tr) < cuts::closest_approach_add){
				used_tracks.push_back(tr);
			} else {
				unused_tracks.push_back(tr);
			}
		}

		if (used_tracks.size() < 2) continue;
	

		VertexFitter fitter;
		auto status = fitter.fit(used_tracks, current_seed.guess().std() );

		if (status == false or fitter.merit() > cuts::vertex_chi2){
			if (status == false) noConverge += 1;
			if (fitter.merit() > cuts::vertex_chi2) missedChi2 += 1;
			continue;
		} 

		double cos_opening_angle = -1.0;
		if (used_tracks.size() == 2){

			auto tr1 = used_tracks[0];
			auto tr2 = used_tracks[1];

			cos_opening_angle = tr1->vx*tr2->vx + tr1->vy*tr2->vy + tr1->vz*tr2->vz;
			cos_opening_angle = cos_opening_angle/( tr1->beta()*tr2->beta()*constants::c*constants::c );
		}

		auto good_vertex = new physics::vertex(fitter.parameters, cos_opening_angle);
		
		for (auto track : used_tracks){
			good_vertex->track_indices.push_back(track->index);
		}

		good_vertex->CovMatrix(fitter.cov_matrix, fitter.npar);
		good_vertex->merit(fitter.merit());
		vertices.push_back(good_vertex);
		tracks = unused_tracks;


	}






}




std::vector<physics::track*> VertexFitter::track_list = {};
std::vector<double> VertexFitter::parameters = {};
std::vector<double> VertexFitter::parameter_errors = {};
double VertexFitter::_merit = 0.;
double VertexFitter::cov_matrix[VertexFitter::npar][VertexFitter::npar];

bool VertexFitter::bad_fit = false;
void VertexFitter::nll(int &npar, double *gin, double &f, double *pars, int iflag ){
	using Vector = vector::Vector;
	double _x = pars[0];
	double _y = pars[1];
	double _z = pars[2];
	double _t = pars[3];

	
	double error = 0.0 ;

	int n = 0;

	for (auto track : VertexFitter::track_list){

		double dist = track->distance_to( Vector(_x, _y, _z), _t);
		
		double err = track->err_distance_to( Vector(_x, _y, _z), _t);

		error += 0.5*(dist/err)*(dist/err) + TMath::Log(err);

		
	
		if (isnan(error)){ 
			bad_fit = true;
			std::cout << dist << " " << err << std::endl;
			track->CovMatrix().Print();
			return;
		}	

		
	}

	
	f = error;
}