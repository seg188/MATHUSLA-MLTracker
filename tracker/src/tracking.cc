#include <iostream>
#include "RunManager.hh"
#include "units.hh"
#include <dlib/dnn.h>

TString input_name = "/home/stephen/hex/mathusla_all/sept20/data/run0.root";
TString outfile_name = "statistics0.root";


int main(int argc, char *argv[]){

	RunManager RM;

	RM.SetInputFile(input_name);

	RM.SetOutputFile(outfile_name);

	RM.StartTracking();


	return 0;

} //main