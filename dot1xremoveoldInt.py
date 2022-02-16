import os
from ciscoconfparse import CiscoConfParse
import re



def RemoveInterfaceConfigs(file_directory, parsed_directory):
    files = os.listdir(file_directory)
    
    for file in files: #remove auth statments from interfaces
        with open(os.path.join(file_directory,file), 'r') as inputfile:
            output = open(os.path.join(parsed_directory,file), 'w+')
            print('no aaa authorization config-commands', file=output) # take out command auth first, to speed up the config update later
            parse = CiscoConfParse(inputfile, syntax='ios')
            for interface in parse.find_objects('^interface'): # gig and 2 gig interfaces, exclude 10gig and vlan
                for intf_child in interface.children:
                    portmode = re.match(r' switchport.mode.access+', intf_child.text) # get all the access ports
                    if portmode is not None:
                        print(interface.text, file=output) # interface name
                        print(" no mab", file=output)
                        print(" no dot1x pae authenticator", file=output)
                        print(" no dot1x timeout tx-period 7", file=output)
                        print(" no device-tracking attach-policy IPDT_MAX_10", file=output) # renaming ipdt to align with dnac
                    authmatches = re.match(r' authentication.+', intf_child.text) # get all authentication statements to remove
                    if authmatches is not None:
                        print(' no' + authmatches.group(0), file=output)                    
            output.close()