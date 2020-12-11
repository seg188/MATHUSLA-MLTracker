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
	const double ip_x = 0.0;
	const double ip_y = 0.0;
	const double ip_z = 0.0;
	//specifies the bottom and top y position of every layer
	const std::vector<std::vector<double>> LAYERS_Y={{6001.0*cm, 6004.0*cm},  //layer 0
 												 	{6104.0*cm, 6107.0*cm}, //layer 1
 													{8001.0*cm, 8004.0*cm}, //layer 2
 													{8104.0*cm, 8107.0*cm}, //layer 3
 													{8501.0*cm, 8504.0*cm}, //layer 4
 													{8604.0*cm, 8607.0*cm}, //layer 5
 													{8707.0*cm, 8710.0*cm}, //layer 6
 													{8810.0*cm, 8813.0*cm}, //layer 7
													{8913.0*cm, 8916.0*cm} };  //layer 8
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
	const double scintillator_height = 3.0*units::cm;
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

	//digi cuts and constants
	const double digi_spacing = 20.0*units::ns;
	const double SiPM_energy_threshold = 0.65*units::MeV;
	
	//seeding
	const double seed_ds2 = 5.0; //sigma
	const double seed_residual = 10.0; //sigma
	
	//tracking
	const double residual_drop = 12.0; //sigma
	const double residual_add = 12.0; //sigma
	const double track_chi2 = 5.0;
	const int track_nlayers = 3;
	const int nseed_hits = 4;
	const double time_difference_drop = 12.0; //sigma
	const double seed_time_difference = 10.0; //sigma
	const int ntrack_hits = 4;
	const double distance_to_hit = 75.0*units::cm;

	//merging
	const double merge_cos_theta = 0.85; 
	const double merge_distance = 150*units::cm;

	//cleaning step
	const double chi2_add = 10.0;
	const double chi2_drop = 16.0;
	const int cleaning_nhits = 6;

	//vertexing
	const double seed_closest_approach = 100*units::cm;
	const double vertex_chi2 = 11.0;
	const double closest_approach_add = 100*units::cm;


};


#endif