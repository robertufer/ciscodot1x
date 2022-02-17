import paramiko
import os
import time


def Login(deviceip, destination, sshuser, sshpass):

    ssh = paramiko.SSHClient()                                # turns on paramiko for ssh
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy()) # automatically adds new ssh host keys

    # connection management
    commands = 'show run | redir tftp://' + destination +"/" + deviceip +'.txt'
    ssh.connect(deviceip, username=sshuser, password=sshpass)
    stdin,stdout,stderr = ssh.exec_command(commands)
    time.sleep(8) # wait 8 seconds fot the tftp to finish before closing channel
    ssh.close()