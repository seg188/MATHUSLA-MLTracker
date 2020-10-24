#include "units.hh"
#include <cmath>
#include <iostream>

#ifndef GEOMETRY_HH
#define GEOMETRY_HH

class Layer  {
public:
	int index;
	double min;
	double max;
	double center;

	//the uncertainty along each directiion in the layer
	std::vector<double> widths(){
		if ( (index % 2 ) == 0){
			return { detector::time_resolution*constants::c, detector::scintillator_length };
		} 

		return {  detector::scintillator_length, detector::time_resolution*constants::c };
	}

	Layer(int _index, double _min, double _max){
		index = _index;
		min = _min;
		max = _max;
	}

	bool in_layer(double y){return (y < min and y < max);}
	
};

class Module{
public:
	double cx, cy, cz; //center point
	double xmin, ymin, zmin;
	double xmax, ymax, zmax;
	int index;
	std::vector<Layer*> layers;
	void SetLayers(std::vector<Layer*> _layers){layers = _layers;}
	void SetIndex(int _index){index = _index;}

	std::vector<double> LocalPosition(double x, double y, double z){
		return {x-cx, y-cy, z-cz};
	}


	Module(double _xmin, double _xmax, double _ymin, double _ymax, double _zmin, double _zmax){
		xmin = _xmin;
		xmax = _xmax;
		ymin = _ymin;
		ymax = _ymax;
		zmin = _zmin;
		zmax = _zmax;

		cx = (xmin + xmax)/2.00;
		cy = (ymin + ymax)/2.00;
		cz = (zmin + zmax)/2.00;

	}

	int is_inside(double x, double y, double z){
		if ( !(x > xmin and x < xmax ) ) return -1;
		if ( !(y > ymin and y < ymax ) ) return -1;
		if ( !(z > zmin and z < zmax ) ) return -1;
		return 1;
	}
};



class detID{
public:
	int moduleIndex;
	int layerIndex;
	int xIndex;
	int zIndex;

	detID(int _module_index, int _layer_index, int _x_index, int _z_index){
		moduleIndex = _module_index;
		layerIndex = layerIndex;
		xIndex = _x_index;
		zIndex = _z_index;
	}

	bool operator==(const detID &detID2){
		if (moduleIndex != detID2.moduleIndex) return false;
		if (layerIndex != detID2.layerIndex) return false;
		if (xIndex != detID2.xIndex) return false;
		if (zIndex != detID2.zIndex) return false;
		return true;
	}
};

class Geometry{
public:

	std::vector<Module*> module_list{};
	std::vector<Layer*> layer_list{};

	Geometry(){
	
		for (int _index = 0; _index < detector::n_layers; _index++ ){
			layer_list.push_back(new Layer(_index, detector::LAYERS_Y[_index][0], detector::LAYERS_Y[_index][1])); 
		}
	

		//CONSTRUCT MODULE LIST
		auto min_y = detector::LAYERS_Y[0][0];
	
		auto max_y = detector::LAYERS_Y[detector::n_layers-1][1];

		for (int _index = 0; _index < detector::n_modules; _index++){
			int _x = _index % 10;
			int _z = (_index - _x)/10;
			module_list.push_back(new Module(detector::MODULE_X[_x][0], detector::MODULE_X[_x][1], min_y, max_y, detector::MODULE_Z[_z][0], detector::MODULE_Z[_z][1]));
			module_list[_index]->SetIndex(_index);
		}

	} //Geometry Constructor

	~Geometry(){
		for (auto p : module_list){delete p;}
		for (auto p : layer_list){delete p;}
	}

	detID GetDetID(double x, double y, double z){
		int module_index = -1;
		int layer_number = -1;
		std::vector<double> layer_widths = {-1, -1};

		for (auto module : module_list){ 

			if (module->is_inside(x, y, z)){
				module_index = module->index;
				break;
			}
		}

		for (auto layer : layer_list){
			if (layer->in_layer(y)){
				layer_number = layer->index;
				layer_widths = layer->widths();
				break;
			}
		}

		std::vector<double> local_position = (module_list[module_index])->LocalPosition(x, y, z);
		layer_widths = layer_list[layer_number]->widths();

		int x_index = static_cast<size_t>(std::floor(local_position[0]/ layer_widths[0]));
		int z_index = static_cast<size_t>(std::floor(local_position[2]/ layer_widths[1]));

		return detID(module_index, layer_number, x_index, z_index);

	} //GetDetID

		

	



}; //Geometry Class




#endif