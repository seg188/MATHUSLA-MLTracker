#include "globals.hh"
#include "Geometry.hh"
#include "physics.hh"

#ifndef SD_DEFINE
#define SD_DEFINE

class StudyDoer{
public:
  std::vector<physics::track*> tracks;
  // std::vector<double> particle_ids;

	std::vector<double> muonic_fractions;
  int muonic_trackcut;
  std::vector<int> muonic_trackindices;

  std::vector<double> avg_deposited_e;
  std::vector<double> muonic_deposited_e;
  std::vector<double> nonmuonic_deposited_e;

	void CalculateMuonicfraction(std::vector<double> ids);
  void CalculateAvgEnergyDeposition();
  void clear(){
    //particle_ids.clear();
    muonic_fractions.clear();
    avg_deposited_e.clear();
    muonic_trackindices.clear();
    muonic_deposited_e.clear();
    nonmuonic_deposited_e.clear();
    muonic_trackcut = 0;
		// for (auto tr : tracks) delete tr;
		// tracks.clear();

	}

private:

};


#endif
