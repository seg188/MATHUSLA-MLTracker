#include "globals.hh"
#include "VertexFinder.hh"
#include "statistics.hh"
#include "physics.hh"


void VertexFinder::FindVertices(){

	if (tracks.size() < 2) return; // no vertices with just 1 track, obviously

	//now, we find vertices as follows:
	//we start with the first two tracks, and fit it to a vertex
	//if the vertex passes a strict chi2 cut, we try to add other tracks sequentially
	//we sort the tracks by the distance of their (x0, y0, z0, t0) to the vertex, and start with the closest ones
	//we also use a distance cut in order to increase the efficiency--if the track is very far from the spacetime point
	//of the vertex, then there is no reason to try and fit it to the vertex

	//once a track is added to a vertex, we remove it from the list of available tracks
	//we iterate until all possible combinations of tracks are exhausted

	auto first_track = tracks[0];

	//now, we find the track that has the closest x, y, z, t to this track

	double min = 99999999.9;
	int min_index = -1;

	for (int trackn = 1; trackn < tracks.size(); trackn++){
		auto curr_track = tracks[trackn];
		double dist = first_track->distance_to(curr_track->x0, curr_track->y0, curr_track->z0, curr_track->t0);
		if (dist < min){
			min = dist;
			min_index = trackn;
		}
	}

	std::vector<physics::track*> tracks_to_fit = {first_track, tracks[min_index]};

	//now we have the track whose point is closest, we try and fit a vertex

	VertexFitter fitter;
	fitter.fit(tracks_to_fit, {first_track->x0, first_track->y0, first_track->z0, first_track->t0});

	if (fitter.merit() > cuts::vertex_chi2) return;

	auto curr_vertex = physics::vertex(fitter.parameters);


}




std::vector<physics::track*> VertexFitter::track_list = {};
std::vector<double> VertexFitter::parameters = {};
std::vector<double> VertexFitter::parameter_errors = {};
void VertexFitter::nll(int &npar, double *gin, double &f, double *pars, int iflag ){
	
	double x = pars[0];
	double y = pars[1];
	double z = pars[2];
	double t = pars[3];

	double error = 0.0 ;


	for (auto track : VertexFitter::track_list){

		double dist = track->distance_to(x, y, z, t);
		double err = track->err_distance_to(x, y, z, t);

		error += TMath::Log(TMath::Abs(error)) + 0.5*(dist/err)*(dist/err);
		
	}

	f = error;
}