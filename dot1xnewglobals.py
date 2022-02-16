import os
from ciscoconfparse import CiscoConfParse
import re


def NewGlobals(file_directory, parsed_directory):
    files = os.listdir(file_directory) # get the file names from the input directory
    

    for inputname in files: # prepping the outputfile
        globalsfile = open('globals_template.txt', 'r')
        #print("filename = ", inputname)
        outputfile = os.path.join(parsed_directory, inputname)
        #print("outputfile = ", outputfile)
        # line by line merge template with outputfile
        with open(outputfile, 'a+') as outputnew:
            for i in globalsfile.readlines():
                print(i.strip("\n"), file=outputnew)
        globalsfile.close()