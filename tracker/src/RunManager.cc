#include <iostream>
#include "RunManager.hh"
#include "TreeHandler.hh"
#include "TrackFinder.hh"
#include "Digitizer.hh"
#include "units.hh"



int RunManager::StartTracking(){
	
	TreeHandler _handler(_InputTree_Name, _InputFile_Name, _OutputTree_Name, _OutputFile_Name);
	TH = &_handler;


//looping over every event in the loop.
	while (TH->Next() >= 0){

		TH->LoadEvent(); //copying the data to the new tree, and loading all the variables, incrementing index

		auto hits_x = *(TH->sim_hit_x);
		auto hits_y = *(TH->sim_hit_y);
		auto hits_z = *(TH->sim_hit_z);
		auto hits_t = *(TH->sim_hit_t);
		auto hits_e = *(TH->sim_hit_e);

		
		//adding all hits of the tree into the digitizer
		std::cout << TH->sim_numhits << std::endl;
		for (int n_hit = 0; n_hit < TH->sim_numhits; n_hit++){
			physics::sim_hit* current = new physics::sim_hit(hits_x[n_hit], hits_y[n_hit], hits_z[n_hit], hits_t[n_hit], hits_e[n_hit] ); 
			_digitizer->AddHit(current);
		}
		
		std::vector<physics::digi_hit*> digi_list = _digitizer->Digitize();
		
		TH->Fill();
	}
	
	TH->Write();


	return 0;
}

