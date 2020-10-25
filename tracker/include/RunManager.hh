#include <TString.h>
#include "TrackFinder.hh"
#include "TreeHandler.hh"
#include "Digitizer.hh"
#include "units.hh"


#ifndef RUN_MANAGER_DEFINE
#define RUN_MANAGER_DEFINE

class RunManager{


public:

	// called in main function to start algorithm
	int StartTracking();
	void SetInputFile(TString name){_InputFile_Name = name;}
	void SetOutputFile(TString name){_OutputFile_Name = name;}

	RunManager(){
		
		_digitizer = new Digitizer();
		_tracker = new TrackFinder();
	} 

	~RunManager(){
		delete _digitizer;
		delete _tracker;
	}


private:

	//DATA AND TRACKING VARIABLES
	int LoadEvent(int);
	TreeHandler* TH;

	Digitizer* _digitizer;
	TrackFinder* _tracker;

	//DATA IO NAMES AND FILES
	TString _InputFile_Name;
	TString _OutputFile_Name;

	TString _InputTree_Name = TString("box_run");
	TString _OutputTree_Name = TString("integral_tree");



};


#endif