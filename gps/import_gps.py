# -*- coding: utf-8 -*-
"""
requires gpsbabel installation
http://www.gpsbabel.org/

imports gpx data from usb or com1 connected gps garmin gps device, converts to csv
"""
from subprocess import call
import os
import gpx_to_csv
import pandas

def import_gps(input_type, outfile):
    basedir = os.getcwd()
    if not '.csv' in outfile:   
        outfile += '.csv'
    call("gpsbabel\gpsbabel.exe -t -w -r -i garmin -f %s: -o gpx -F %s" % (input_type, outfile))
    gpx = gpx_to_csv.gpx_to_csv(os.path.join(basedir, outfile))
    gpx.tracks_to_csv()


#Runs the utility in the command line
input_type = raw_input("Specify input type (com1 or usb): ")
outfile = raw_input("Please specify a filename")
while not input_type in ["com1", "usb"]:    
    input_type = raw_input("Please enter correct input type (com1 or usb): ")    

import_gps(input_type, outfile)
