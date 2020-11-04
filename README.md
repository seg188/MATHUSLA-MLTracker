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

## Visualization and Understanding the Output

There is a small python module made for visualization of the output of the tracker, i.e. visualization the spatial and timing information of the track and the hits. This can be accessed by:

```bash
$ mkdir plots
$ cd visualization
$ python main.py 
```

The main.py script is designed to be highly customizable.

## Example Visualization Script

```python

import visualization
import physics
import ROOT as root 


tracking_file_name = "../build/statistics0.root" ##CHANGE ME TO THE PATH TO YOUR TRACKER OUTPUT FILE

tracking_file = root.TFile.Open(tracking_file_name)
tree = tracking_file.Get("integral_tree")


for event_number in range(int(tree.GetEntries())): #looping over events in the tree
	
	tree.GetEntry(event_number)
	#we can add some cuts here if we would like

	#for example, we add below a cut on the number of tracks-- we only want events with exactly 2 tracks
	if not (tree.NumTracks == 2):
		continue 
	####################################################################################################3
	
	#now we do the visualization using the Display class
	event_display = visualization.Display()

	for k in range(int(tree.Digi_numHits)):
		#points can be added to the display using the AddPoint function
		#a point, in this case, is a list of [x, y, z, t]. In this case, it is used to draw the digitized Mu-Simulation output
		event_display.AddPoint( [tree.Digi_x[k], tree.Digi_y[k], tree.Digi_z[k], tree.Digi_time[k]] )


	for k in range(int(tree.NumTracks)):
		#tracks can be added using the AddTrack function, that takes the arguments (x0, y0, z0, vx, vy, vz, t0) which define a track
		x0, y0, z0, t0 = tree.Track_x0[k], tree.Track_y0[k], tree.Track_z0[k], tree.Track_t0[k]
		vx, vy, vz = tree.Track_velX[k], tree.Track_velY[k], tree.Track_velZ[k]
		event_display.AddTrack(x0, y0, z0, vx, vy, vz, t0)


	plot_title = "event " + str(event_number)
	png_file_name = "event" + str(event_number) + ".png"
	
	#the display is written to an output file using the method Display.Draw(title, file_name)
	event_display.Draw( plot_title , png_file_name )



```


# Contact

Please email stephen.greenberg@rutgers.edu with any questions related to this repository. 





