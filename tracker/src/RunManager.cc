#include <iostream>
#include "RunManager.hh"
#include "TreeHandler.hh"
#include "TrackFinder.hh"


int RunManager::StartTracking(){
	
	TreeHandler _handler(_InputTree_Name, _InputFile_Name, _OutputTree_Name, _OutputFile_Name);
	TH = &_handler;
	for (int k =0; k < 25; k++){
		TH->LoadEvent(k);
		TH->Fill();
	}
	
	TH->Write();


	return 0;
}

