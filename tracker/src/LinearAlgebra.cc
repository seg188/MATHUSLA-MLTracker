#include <cstdlib>
#include <iostream>
#include <vector>
#include <cmath>
#include "LinearAlgebra.hh"
// ADD 2 Vectors
namespace vector{
using namespace std;
Vector Vector::operator+(Vector v)
{
        int x1, y1, z1;
        x1 = x + v.x;
        y1 = y + v.y;
        z1 = z + v.z;
        return Vector(x1, y1, z1);
}

// Subtract 2 vectors
Vector Vector::operator-(Vector v)
{
        int x1, y1, z1;
        x1 = x - v.x;
        y1 = y - v.y;
        z1 = z - v.z;
        return Vector(x1, y1, z1);
}

// Dot product of 2 vectors
int Vector::operator^(Vector v)
{
        int x1, y1, z1;
        x1 = x * v.x;
        y1 = y * v.y;
        z1 = z * v.z;
        return (x1 + y1 + z1);
}

// Cross product of 2 vectors
Vector Vector::operator*(Vector v)
{
        int x1, y1, z1;
        x1 = y * v.z - z * v.y;
        y1 = z * v.x - x * v.z;
        z1 = x * v.y - y * v.x;
        return Vector(x1, y1, z1);
}

// Display Vector
std::ostream& operator<<(std::ostream& out,
                                        const Vector& v)
{
        out << v.x << "i ";
        if (v.y >= 0)
                out << "+ ";
        out << v.y << "j ";
        if (v.z >= 0)
                out << "+ ";
        out << v.z << "k" << std::endl;
        return out;
}

};