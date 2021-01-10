#include <iostream>
#include "RunManager.hh"
#include "physics.hh"
#include "globals.hh"
#include <dlib/dnn.h>


int main(int argc, char *argv[]){

	if (argc != 3) {
		std::cout << "Need 2 Arguments! \n First argument: input_file_name \n Second argument: output_file_name" << std::endl;
		return 0;
	}

	TString input_name = TString(argv[1]);
	TString outfile_name = TString(argv[2]);


	RunManager RM;

	RM.SetInputFile(input_name);

	RM.SetOutputFile(outfile_name);

	RM.StartTracking();


	return 0;

} //main