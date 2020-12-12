#include "globals.hh"
#include "physics.hh"
#include <TMath.h>
#include <TRandom.h>
#include "TMinuit.h"
#include "statistics.hh"
#include "Geometry.hh"
#include "StudiesDoer.hh"
#include <numeric>
#include <iostream>


void StudyDoer::CalculateMuonicfraction(std::vector<double>ids){
  int muoncuts = 0;
  std::vector<int> muonictrackindices;
  for (auto track : tracks){
    double muonic_count = 0;
    double non_muonic_count = 0;
    for (auto digi : track->hits){
      int muons = 0;
      std::vector<int> digi_simindices;
      for (auto hit : digi->hits){
        digi_simindices.push_back(hit->index);}
      for (int index : digi_simindices){
          double particle_id = ids[index];
      if (particle_id == 13 || particle_id == -13){muons++;}}
      if (muons > 0){muonic_count++;} else {non_muonic_count++;}}

  muonic_fractions.push_back(muonic_count / (muonic_count + non_muonic_count));
  if (muonic_count / (muonic_count + non_muonic_count) > 0.8){
    muonictrackindices.push_back(track->index);
    muoncuts++;}
   } //track
  muonic_trackcut = muoncuts;
  muonic_trackindices = muonictrackindices;
}

void StudyDoer::CalculateAvgEnergyDeposition(){
  for (auto track : tracks){
    std::vector<double> deposited_e;
    int numdigi = track->hits.size();
    for (auto digi : track->hits){deposited_e.push_back(digi->e);}
    double total_e = std::accumulate(deposited_e.begin(), deposited_e.end(), 0);
    avg_deposited_e.push_back(total_e / numdigi);
    bool included = false;
    for (int ind : muonic_trackindices){
      if (track->index == ind){ included = true;}}
    if (included){muonic_deposited_e.push_back(total_e / numdigi);}else{
      nonmuonic_deposited_e.push_back(total_e / numdigi);}
    //std::cout << total_e / numdigi << '\n';
  }//track
}
