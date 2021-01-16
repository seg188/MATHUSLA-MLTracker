# MATHUSLA-Tracker
Tracking software for MATHUSLA Experiment

## Introduction
This is an updated version of the MATHUSLA Experiment tracking software currently under development. The goal of this software is to implement a simple, highly portable, and easily understandable algorithm for tracking highly relativistic particles.


## Installation

All of the dependencies and necessary libraries for this code are available through the anaconda software. If you do not have anaconda, it can be installed following the directions here: https://docs.anaconda.com/anaconda/install/

Once anaconda is installed, the enviornment can be created using the .yml file available in this repository as follows. From the top directory:

```bash
$ conda env create -f env/environment.yml
$ conda activate tracker
```

Now, the project can be built using cmake:

```bash
$ mkdir build
$ cd build
$ cmake ../tracker 
$ make 
```

At this point, the tracker executable is available in the build directory. 


## Running the Tracker

The tracker requires two command line arguments, the path to an input file, and the path to which the output file should be written. The input file should be the output from a MATHUSLA Mu-Simulation run, a Geant4 based simulation of particle passage through the MATHUSLA detector. 

The Mu-Simulation repository can be found here: https://github.com/MATHUSLA/Mu-Simulation

An example command to run the tracker:

```bash
$ ./tracker path_to_input_file path_to_write_output 
```


# Contact

Please email stephen.greenberg@rutgers.edu with any questions related to this repository. 





