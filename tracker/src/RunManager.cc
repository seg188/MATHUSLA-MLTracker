#include <iostream>
#include "RunManager.hh"
#include "TreeHandler.hh"
#include "TrackFinder.hh"
#include "Digitizer.hh"
#include "globals.hh"
#include "StudiesDoer.hh"



int RunManager::StartTracking(){

	TreeHandler _handler(_InputTree_Name, _InputFile_Name, _OutputTree_Name, _OutputFile_Name);
	TH = &_handler;
	int events_handled = 0;

//looping over every event in the loop.
	while (TH->Next() >= 0){
		_digitizer->clear();
		_tracker->clear();
		_vertexer->clear();
		_studyer->clear();


		TH->LoadEvent(); //copying the data to the new tree, and loading all the variables, incrementing index


		auto hits_x = *(TH->sim_hit_x);
		auto hits_y = *(TH->sim_hit_y);
		auto hits_z = *(TH->sim_hit_z);
		auto hits_t = *(TH->sim_hit_t);
		auto hits_e = *(TH->sim_hit_e);

		//adding all hits of the tree into the digitizer
		for (int n_hit = 0; n_hit < TH->sim_numhits; n_hit++){
			physics::sim_hit* current = new physics::sim_hit(n_hit, hits_x[n_hit], hits_y[n_hit], hits_z[n_hit], hits_t[n_hit], hits_e[n_hit] );
			_digitizer->AddHit(current);
		}


		std::vector<physics::digi_hit*> digi_list = _digitizer->Digitize();

		TH->ExportDigis(digi_list);

		//digis now finished and stored in tree!!!
		//now, we begin the seeding algorithm

		_tracker->hits = digi_list;
		_tracker->Seed();
		_tracker->FindTracks();
		_tracker->CalculateMissingHits(_digitizer->_geometry);
		TH->ExportTracks(_tracker->tracks);


		_vertexer->tracks = _tracker->tracks;
		_vertexer->Seed();
		_vertexer->FindVertices();

		TH->ExportVertices(_vertexer->vertices);

		//now beginning studies
		_studyer->tracks = _tracker->tracks;
		_studyer->CalculateMuonicfraction(*(TH->sim_hit_particlePdgId));
		_studyer->CalculateAvgEnergyDeposition();

		std::vector<double> muons = _studyer->muonic_fractions;
		int muoncuts = _studyer->muonic_trackcut;
		TH->ExportStudies(_studyer->muonic_fractions, _studyer->muonic_trackcut,
		_studyer->avg_deposited_e, _studyer->muonic_deposited_e, _studyer->nonmuonic_deposited_e);
		TH->Fill();

		events_handled++;

		if (events_handled % 50 == 0) std::cout << "finished " << events_handled << " events" << std::endl;
	}

	TH->Write();
	//delete _tracker;
	//delete _digitizer;


	return 0;
}
