import os
from ciscoconfparse import CiscoConfParse
import re
# this is good to go, needs testing

def NewInterfaces(file_directory, parsed_directory):

    files = os.listdir(file_directory)
    
    for file in files: #remove auth statments from interfaces
        with open(os.path.join(file_directory,file), 'r') as inputfile:
            output = open(os.path.join(parsed_directory,file), 'a')
            print('no aaa authorization config-commands', file=output) # take out command auth first, to speed up the config update later
            parse = CiscoConfParse(inputfile, syntax='ios')
            #for interface in parse.find_objects('^interface.[GT](?!e)'): # gig and 2 gig interfaces, exclude 10gig and vlan
            for interface in parse.find_objects('^interface'): # gig and 2 gig interfaces, exclude vlan
                for intf_child in interface.children:
                    portmode = re.match(r' switchport.mode.access+', intf_child.text) # get all the access ports
                    if portmode is not None:
                        print(interface.text.strip(), file=output) # interface name
                        print(" cdp enable", file=output)
                        print(" device-tracking attach-policy IPDT_POLICY", file=output)
                        print(" source template APPLY_ISE", file=output)
            print("aaa accounting update newinfo", file=output)
            print("aaa authentication dot1x _____", file=output)
            print("aaa authorization network _____", file=output)
            print("aaa accounting identity default start-stop group _____", file=output)
            print("aaa authorization config-commands", file=output)
            output.close()