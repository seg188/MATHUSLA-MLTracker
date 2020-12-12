#include <iostream>
#include "RunManager.hh"
#include "TreeHandler.hh"
#include "TrackFinder.hh"
#include "Digitizer.hh"
#include "globals.hh"



int RunManager::StartTracking(){
	
	TreeHandler _handler(_InputTree_Name, _InputFile_Name, _OutputTree_Name, _OutputFile_Name);
	TH = &_handler;
	int events_handled = 0;

//looping over every event in the loop.
	while (TH->Next() >= 0){ 
		_digitizer->clear();
		_tracker->clear();
		_vertexer->clear();

		TH->LoadEvent(); //copying the data to the new tree, and loading all the variables, incrementing index
		
		//adding all hits of the tree into the digitizer
		for (int n_hit = 0; n_hit < TH->sim_numhits; n_hit++){
			physics::sim_hit* current = new physics::sim_hit(TH, n_hit);
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
		_tracker->MergeTracks();
		_tracker->CalculateMissingHits(_digitizer->_geometry);
		TH->ExportTracks(_tracker->tracks);
		


		_vertexer->tracks = _tracker->tracks;
		_vertexer->Seed();
		_vertexer->FindVertices();

		TH->ExportVertices(_vertexer->vertices);

		TH->Fill();

		events_handled++;

		if (events_handled % 50 == 0) std::cout << "finished " << events_handled << " events" << std::endl;
	}
	
	TH->Write();
	//delete _tracker;
	//delete _digitizer;


	return 0;
}

