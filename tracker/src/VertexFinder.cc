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
	

		VertexFitter fitter;
		auto status = fitter.fit(used_tracks, current_seed.guess());

		if (status == 4 or fitter.merit() > cuts::vertex_chi2){
			std::cout << fitter.merit() << std::endl;
			continue;
		} 

		vertices.push_back(new physics::vertex(fitter.parameters));
		tracks = unused_tracks;


	}





}




std::vector<physics::track*> VertexFitter::track_list = {};
std::vector<double> VertexFitter::parameters = {};
std::vector<double> VertexFitter::parameter_errors = {};
bool VertexFitter::bad_fit = false;
void VertexFitter::nll(int &npar, double *gin, double &f, double *pars, int iflag ){
	
	double _x = pars[0];
	double _y = pars[1];
	double _z = pars[2];
	double _t = pars[3];

	
	double error = 0.0 ;

	int n = 0;

	for (auto track : VertexFitter::track_list){

		double dist = track->distance_to(_x, _y, _z, _t);
		
		double err = track->err_distance_to(_x, _y, _z, _t);

		if (err > 0) error += TMath::Log(TMath::Abs(err) ) + 0.5*(dist/err)*(dist/err);
		
	
		if (isnan(error)){ 
			bad_fit = true;
			std::cout << dist << " " << err << std::endl;
			track->cov_matrix.Print();
			return;
		}	

		
	}

	
	f = error;
}