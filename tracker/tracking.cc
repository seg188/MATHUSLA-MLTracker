#include <iostream>
#include <TTree.h>

int main(int argc, char *argv[]){
	auto tree = new TTree("my_name", "testing");

	std::cout << "made a tree" << std::endl;

	delete tree;
}