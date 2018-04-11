import ssh
from credentials import Credentials


class VMAXDevice():

    def __init__(self, credentials):
        self.ip = credentials.symcli_ip
        self.username = credentials.username
        self.password = credentials.password

    def get_sg(self, sid, account):
        # Get storage group name from target VMAX
        print('Connect to SYMCLI server')
        command = 'export SYMCLI_CONNECT=VMAX' + sid + '; symaccess -sid ' + sid + ' list view -v | grep ' + account + ' | grep \'Storage Group Name\' | awk \'{print $NF}\' | awk \'!seen[$1]++\''
        sg = ssh.connect(self.ip, self.username, self.password, command).strip()
        for each in str(sg).split('\n'):
            print('\t' + each)


        return sg

    def untag_sg(self, sid, sg):
        # Untag target SG for RPA
        command = ''
        print('Untag LUNs to RPA')
        for each_sg in str(sg).split('\n'):
            command = '\tsymrpi -sid ' + sid + ' -cluster DFW3MIG unprotect -sg ' + each_sg + ' -nop;'

            print(command)
        # output = ssh.connect(cr.symcli_ip, cr.username, cr.password, command)
        # print(output)

    def get_luns(self, sid, sg):
        command = ''
        print('List volumes for each SG')
        for each_sg in str(sg).split('\n'):
            command = 'export SYMCLI_CONNECT=VMAX' + sid + ';symdev -sid ' + sid + ' list -sg ' + each_sg
            luns = ssh.connect(self.ip, self.username, self.password, command).strip()
            print(luns)

        #return luns

    def get_initiators(self, sid, account):
        command = ''
        print('List initiators for this account')
        command = 'symaccess -sid ' + sid + ' list -type initiator | grep ' + account
        print('\t' + command)

def main():
    account_number = ''
    storage_device = ''
    hosts = ['1', '2', '3']
    source_vmax_sid = ''

    cr = Credentials(account_number, storage_device, hosts, source_vmax_sid)
    vmax = VMAXDevice(cr)

    # Get storage group for this account on the VMAX3
    # sg = vmax.get_sg(cr.target_vmax_sid, cr.account_number)

    # Untag target SG for RPA
    # vmax.untag_sg(cr.target_vmax_sid, sg)

    # Get storage group from source VMAX
    sg = vmax.get_sg(cr.source_vmax_sid, cr.account_number)

    # vmax.untag_sg(cr.source_vmax_sid, sg)

    vmax.get_luns(cr.source_vmax_sid, sg)

    # vmax.get_initiators(cr.source_vmax_sid, cr.account_number)

if __name__ == '__main__':
    main()
