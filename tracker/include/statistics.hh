#include "TMinuit.h"
#include "physics.hh"

#ifndef STAT_HH
#define STAT_HH



class TrackFitter{
public:
		//pars is x0, y0, z0, t0, vx, vy, vz
	static void chi2_error( int &npar, double *gin, double &f, double *par, int iflag);
	static void timeless_chi2_error( int &npar, double *gin, double &f, double *par, int iflag);
	static std::vector<physics::digi_hit*> digi_list;
	static std::vector<double> parameters;
	static std::vector<double> parameter_errors;
	const static int npar = 7;
	static double cov_matrix[npar][npar];
 
	int fit(std::vector<physics::digi_hit*> _digi_list, std::vector<double> arg_guess = {}){
			digi_list = _digi_list;
			parameters.resize(npar);
			parameter_errors.resize(npar);

			std::vector<double> guess = arg_guess;
			
			TMinuit minimizer(npar);
			int ierflg = 0;
			minimizer.SetFCN(chi2_error);

			double first_step_size = 0.1;
			auto maxcalls = 500000.0;
			auto tolerance = 0.1;
			double arglist[2];
			arglist[0] = maxcalls;
			arglist[1] = tolerance;

			int quiet_mode = -1;
			int normal = 0;

			minimizer.SetPrintLevel(quiet_mode);

			double vel_y_direction = arg_guess[4]; //use the direction of the seed to help fit the track

			//we find the lowest t, and take the associated y-value and fix

			double y0_fix;

			double min_t = 9999999.99;
			for (auto hit: digi_list){
				if (hit->t < min_t){
					min_t = hit->t;
					y0_fix = hit->y;
				}
			}

			minimizer.mnparm(0, "x0", guess[0], first_step_size, detector::x_min,detector::x_max,ierflg);
			minimizer.mnparm(1, "y0", y0_fix, first_step_size, 0,0,ierflg);
			minimizer.mnparm(2, "z0", guess[2], first_step_size, detector::z_min,detector::z_max,ierflg);
			minimizer.mnparm(3, "vx", guess[3], first_step_size, -1.0*constants::c,constants::c,ierflg);
			if (vel_y_direction >= 0) minimizer.mnparm(4, "vy", guess[4], first_step_size, 0.0,constants::c,ierflg);
			if (vel_y_direction  < 0) minimizer.mnparm(4, "vy", guess[4], first_step_size,constants::c,0.0,ierflg);
			minimizer.mnparm(5, "vz", guess[5], first_step_size, -1.0*constants::c,constants::c,ierflg);
			minimizer.mnparm(6, "t0", guess[6], first_step_size,0,0,ierflg);

			minimizer.FixParameter(1);
			
			minimizer.mnexcm("MIGRAD", arglist ,2,ierflg);

			//while (ierflg) minimizer.mnexcm("MIGRAD", arglist ,2,ierflg);

			for (int k = 0; k < npar; k++){
				minimizer.GetParameter(k, parameters[k], parameter_errors[k] );
				//std::cout << parameters[k] << ", ";
			}


			minimizer.mnemat(&cov_matrix[0][0], npar);
			//std::cout << std::endl;




			return minimizer.GetStatus();


	}

	double rand_guess(){
		return 0.0;
	}

}; //class TrackFinder


class VertexFitter{
public:
	static void nll( int &npar, double *gin, double &f, double *par, int iflag ); //NEGATIVE LOG LIKLIHOOD FOR FITTING VERTICES
	static std::vector<physics::track*> track_list;
	static std::vector<double> parameters;
	static std::vector<double> parameter_errors;
	const static int npar = 4;
	static double cov_matrix[npar][npar];

	double merit(){
		double chi2 = 0.0;

		for (auto track : track_list){
			chi2 += track->vertex_residual(parameters);
		}

		double ndof = static_cast<double>(npar*(track_list.size()-1));
		return chi2/ndof;
	}

	int fit(std::vector<physics::track*> _track_list, std::vector<double> arg_guess = {}){
			track_list = _track_list;
			parameters.resize(npar);
			parameter_errors.resize(npar);

			std::vector<double> guess = arg_guess;
			
			TMinuit minimizer(npar);
			int ierflg = 0;
			minimizer.SetFCN(nll);

			double first_step_size = 0.1;
			auto maxcalls = 500000.0;
			auto tolerance = 0.1;
			double arglist[2];
			arglist[0] = maxcalls;
			arglist[1] = tolerance;

			int quiet_mode = -1;
			int normal = 0;

			minimizer.SetPrintLevel(quiet_mode);

			minimizer.mnparm(0, "x", guess[0], first_step_size, 0,0,ierflg);
			minimizer.mnparm(1, "y", guess[1], first_step_size, 0,0,ierflg);
			minimizer.mnparm(2, "z", guess[2], first_step_size, 0,0,ierflg);
			minimizer.mnparm(6, "t", guess[3], first_step_size, 0,0,ierflg);
			
			minimizer.mnexcm("MIGRAD", arglist ,2,ierflg);

			//while (ierflg) minimizer.mnexcm("MIGRAD", arglist ,2,ierflg);

			for (int k = 0; k < npar; k++){
				minimizer.GetParameter(k, parameters[k], parameter_errors[k] );
				//std::cout << parameters[k] << ", ";
			}

			//std::cout << std::endl;


			return minimizer.GetStatus();


	}





}; //class VertexFitter



#endif