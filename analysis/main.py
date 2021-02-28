#!/usr/bin/env python
import event
import ROOT as root
import analyzer
import sys
import util


if __name__ == "__main__":
    directory = sys.argv[1]
    h_mumu = analyzer.H_mumu_Analayzer(directory)
    h_mumu.Analyze()
  
    #h_mumu.StudyPassedEvents(0)

