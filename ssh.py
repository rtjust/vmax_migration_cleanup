#from pexpect import pxssh
import paramiko
import csv


def connect(device, user, passwd, command):

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(device, username=user, password=passwd)

    print('Executing command \'' + command + '\'')
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(command, timeout=10000)

    out = ssh_stdout.read()
    ssh.close()

    return out.decode(encoding='UTF-8')