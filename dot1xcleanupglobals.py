import os
from ciscoconfparse import CiscoConfParse
import re


def RemoveGlobalConfigs(file_directory, parsed_directory):
    files = os.listdir(file_directory)
    
    for file in files: #remove radius globals
        with open(os.path.join(file_directory,file), 'r') as inputfile:
            output = open(os.path.join(parsed_directory,file), 'a')
            parse = CiscoConfParse(inputfile, syntax='ios')
            for radservergroup in parse.find_objects('^aaa group server radius'): # grab radius server groups
                print("no " + radservergroup.text, file=output) # need to add print to output file
            for radservers in parse.find_objects('^radius server'):
                print("no " + radservers.text, file=output)
            for aaaserver in parse.find_objects('^aaa server radius dynamic-author'):
                print("no " + aaaserver.text, file=output)
            # now the aaa controls cleanup
            for aaadot1x in parse.find_objects('^aaa a.+ dot1x'):
                print("no " + aaadot1x.text, file=output)
            output.close()