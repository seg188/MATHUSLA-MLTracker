#include<cstdlib>
#include<vector>

#ifndef UNITS_HH
#define UNITS_HH

namespace units{
	const double cm = 1.00;
	const double ns = 1.00;
	const double MeV = 1.00;
};

namespace detector{

	//specifies the bottom and top y position of every layer
	const std::vector<std::vector<double>> LAYERS_Y = {{5950.0, 6050.0},  //layer 0
 												 	{6060.0, 6150.0}, //layer 1
 													{7900.0, 8050.0}, //layer 2
 													{8050.0, 8150.0}, //layer 3
 													{8400.0, 8550.0}, //layer 4
 													{8560.0, 8650.0}, //layer 5
 													{8660.0, 8750.0}, //layer 6
 													{8760.0, 8850.0}, //layer 7
													{8860.0, 9050.0} };  //layer 8
	const int n_layers = 9;

	using namespace units;
	const std::vector<std::vector<double>> MODULE_X = { 	{-4950.0*cm, -4050.0*cm},
													{-3950.0*cm, -3050.0*cm},
													{-2950.0*cm, -2050.0*cm},
													{-1950.0*cm, -1050.0*cm},
													{-950.0*cm, -50.0*cm},
													{50.0*cm, 950.0*cm},
													{050.0*cm, 1950.0*cm},
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

};

namespace constants{

	const double c = 29.97*units::cm/units::ns;

};

namespace cuts{

	const double digi_spacing = 20.0*units::ns;
	const double SiPM_energy_threshold = 0.65*units::MeV;


};


#endif