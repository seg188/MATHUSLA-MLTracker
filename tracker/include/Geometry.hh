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
			return { detector::scintillator_width, detector::scintillator_length };
		} 

		return {  detector::scintillator_length, detector::scintillator_width  };
	}
	std::vector<double> uncertainty(){
		if ( (index % 2 ) == 0){
			return { detector::scintillator_width, detector::time_resolution*constants::c };
		} 

		return {  detector::time_resolution*constants::c, detector::scintillator_width  };

	}

	

	Layer(int _index, double _min, double _max){
		index = _index;
		min = _min;
		max = _max;
	}

	bool in_layer(double y){ 
		if (y > min and y < max) return true;
		return false;
	 }
	
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

	bool is_inside(double x, double y, double z){
		if ( !(x > xmin and x < xmax ) ) return false;
		if ( !(y > ymin and y < ymax ) ) return false;
		if ( !(z > zmin and z < zmax ) ) return false;
		return true;
	}
};



class detID{
public:
	int moduleIndex;
	int layerIndex;
	int xIndex;
	int zIndex;
	bool _null;

	detID(){_null = true;}

	void Print(){
		std::cout << "***************Printing DetID*************" << std::endl;
		std::cout << "Module Index: " << moduleIndex << std::endl;
		std::cout << "Layer Index: " << layerIndex << std::endl;
		std::cout << "x Index: " << xIndex << std::endl;
		std::cout << "z Index: " << zIndex << std::endl;
	}

	detID(int _module_index, int _layer_index, int _x_index, int _z_index){
		moduleIndex = _module_index;
		layerIndex = _layer_index;
		xIndex = _x_index;
		zIndex = _z_index;
	}

	bool operator==(const detID &detID2){
		if (_null) return false;
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

		if (module_index == -1){return detID();}

		for (auto layer : layer_list){
			if (layer->in_layer(y)){
				layer_number = layer->index;
				layer_widths = layer->widths();
				break;
			}
		}

		if (layer_number == -1){return detID();}

		std::vector<double> local_position = (module_list[module_index])->LocalPosition(x, y, z);
		layer_widths = layer_list[layer_number]->widths();

		int x_index = static_cast<size_t>(std::floor(local_position[0]/ layer_widths[0]));
		int z_index = static_cast<size_t>(std::floor(local_position[2]/ layer_widths[1]));

		return detID(module_index, layer_number, x_index, z_index);

	} //GetDetID

	template<class Hit>
	detID GetDetID(Hit _hit){
		return GetDetID(_hit->x, _hit->y, _hit->z);
	}

		

	



}; //Geometry Class




#endif