import getpass
import os

import login
import dot1xremoveoldInt
import dot1xcleanupglobals
import dot1xnewglobals
import dot1xnewinterfaces


def main():
    destinationip = "_____" # address of tftp server
    file_directory = './output/'
    parsed_directory = './parsed/'

    sshuser = input("Enter session username: ")
    sshpass = getpass.getpass(prompt='Enter session password: ', stream=None)   # securely stores password temporarily

    with open('inputips.txt', 'r') as connectips: #all the switches in scope
        for ip in connectips:
            ip = ip.replace('\n', '') # get rid of the newline character
            print("connecting to: " + str(ip))
            try:
                login.Login(ip, destinationip, sshuser, sshpass)
            except:
                print("login failed: " + str(ip))
                continue

        # remove port config from working file
    dot1xremoveoldInt.RemoveInterfaceConfigs(file_directory, parsed_directory)
        # remove global config from working file
    dot1xcleanupglobals.RemoveGlobalConfigs(file_directory, parsed_directory)
        # add global config to working file
    dot1xnewglobals.NewGlobals(file_directory, parsed_directory)
        # add port config to working file
    dot1xnewinterfaces.NewInterfaces(file_directory, parsed_directory)

if __name__ == "__main__":
    main()