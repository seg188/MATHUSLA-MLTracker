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
	


class Vector {
private:
        int x, y, z;
        // 3D Coordinates of the Vector

public:
        Vector(int x, int y, int z)
        {
                // Constructor
                this->x = x;
                this->y = y;
                this->z = z;
        }
        Vector operator+(Vector v); // ADD 2 Vectors
        Vector operator-(Vector v); // Subtraction
        int operator^(Vector v); // Dot Product
        Vector operator*(Vector v); // Cross Product
        double magnitude()
        {
                return sqrt(pow(x, 2) + pow(y, 2) + pow(z, 2));
        }
        friend std::ostream& operator<<(std::ostream& out, const Vector& v);
        // To output the Vector
};


};


#endif