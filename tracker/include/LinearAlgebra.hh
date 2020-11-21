#include <cstdlib>

#ifndef LIN_ALG_HH
#define LIN_ALG_HH


namespace vector{

	static double dot(std::vector<double> a, std::vector<double> b){
		double val = 0;
		for (int i = 0; i < a.size(); i++) val += a[i]*b[i];
		return val;

	}

	static std::vector<double> scaler_multiply(double scale, std::vector<double> vec){
		std::vector<double> res = {};
		res.resize(vec.size());
		for (int i = 0; i < vec.size(); i++) res[i] = vec[i]*scale;
		return res;
	}

	static std::vector<double> add(std::vector<double> a, std::vector<double> b){
		std::vector<double> res = {};
		res.resize(a.size());
		for (int i = 0; i < a.size(); i++) res[i] = a[i] + b[i];
		return res;

	}
	
};



#endif