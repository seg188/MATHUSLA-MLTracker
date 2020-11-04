#include<cstdlib>
#include<vector>

#ifndef UNITS_HH
#define UNITS_HH

namespace units{
	const double mm = 10.0;
	const double cm = 1.00;
	const double ns = 1.00;
	const double MeV = 1.00;
};

namespace detector{
	using namespace units;
	//specifies the bottom and top y position of every layer
	const std::vector<std::vector<double>> LAYERS_Y={{5950.0*cm, 6050.0*cm},  //layer 0
 												 	{6060.0*cm, 6150.0*cm}, //layer 1
 													{7900.0*cm, 8050.0*cm}, //layer 2
 													{8050.0*cm, 8150.0*cm}, //layer 3
 													{8400.0*cm, 8550.0*cm}, //layer 4
 													{8560.0*cm, 8650.0*cm}, //layer 5
 													{8660.0*cm, 8750.0*cm}, //layer 6
 													{8760.0*cm, 8850.0*cm}, //layer 7
													{8860.0*cm, 9050.0*cm} };  //layer 8
	const int n_layers = 9;

	
	const std::vector<std::vector<double>> MODULE_X = { 	{-4950.0*cm, -4050.0*cm},
													{-3950.0*cm, -3050.0*cm},
													{-2950.0*cm, -2050.0*cm},
													{-1950.0*cm, -1050.0*cm},
													{-950.0*cm, -50.0*cm},
													{50.0*cm, 950.0*cm},
													{1050.0*cm, 1950.0*cm},
													{2050.0*cm, 2950.0*cm},
													{3050.0*cm,  3950.0*cm},
													{4050.0*cm,  4950.0*cm} };

	const std::vector<std::vector<double>> MODULE_Z = {{7000.0*cm, 7900.0*cm},
													{8000.0*cm, 8900.0*cm},
													{9000.0*cm, 9900.0*cm},
													{10000.0*cm, 10900.0*cm},
													{11000.0*cm, 11900*cm},
													{12000.0*cm, 12900.0*cm},
													{13000.0*cm, 13900.0*cm},
													{14000.0*cm, 14900.0*cm},
													{15000.0*cm, 15900.0*cm},
													{16000.0*cm, 16900.0*cm} };

	const int n_modules = 100;
	const double scintillator_length = 450.0*units::cm;
	const double scintillator_width = 4.50*units::cm;
	const double time_resolution = 1.0*units::ns;

	const double x_min = MODULE_X[0][0];
	const double y_min = LAYERS_Y[0][0];
	const double z_min = MODULE_Z[0][0];

	const double x_max = MODULE_X[MODULE_X.size()-1][1];
	const double y_max = LAYERS_Y[LAYERS_Y.size()-1][1];
	const double z_max = MODULE_Z[MODULE_Z.size()-1][1];



};

namespace constants{

	const double c = 29.97*units::cm/units::ns;

};

namespace cuts{

	const double digi_spacing = 20.0*units::ns;
	const double SiPM_energy_threshold = 0.65*units::MeV;
	const double seed_ds2 = 75.*units::ns;
	const double seed_residual = 100.0*units::cm;
	const double residual_drop = 75.*units::cm;
	const double residual_add = 25.*units::cm;
	const double track_chi2 = 10.0;
	const int track_nlayers = 3;
	const int nseed_hits = 4;

	const double time_difference_drop = 500.0*units::ns;
	const double seed_time_difference = 500.0*units::ns;

};


#endif