#!/usr/bin/env python
import event
import ROOT as root
import analyzer
import sys
import util


if __name__ == "__main__":
	directory = sys.argv[1]
	h_mumu = analyzer.H_mumu_Analyzer(directory)
	h_mumu.Plot()
    #klong = analyzer.K_Long_Analayzer(directory)
    #klong.Plot()
    #ev = event.Event(directory, 16303)
    #ev.ExtractTruthPhysics()
    #ev.Print()
  
  	
    #h_mumu.StudyPassedEvents(0)

