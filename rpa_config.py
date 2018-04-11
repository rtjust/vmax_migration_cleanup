import sys
import ssh
import re
from credentials import Credentials

class RPADevice():
    def __init__(self, credentials):
        self.ip = credentials.rpa_ip
        self.username = credentials.rpa_user
        self.password = credentials.rpa_pass

    def get_group(self, account, storage_device):
        groups_output = self.__connect('get_groups')
        groups_re = r'(MG[0-9]+[_][0-9]+[_][0-9]+)'
        groups_list = re.findall(groups_re, groups_output)
        for group in groups_list:
            if account in group and storage_device in group:
                return group

    def remove_group(self, group):
        print('Please run this command on RPA {}:'.format(self.ip))
        print('\tremove_group group={} -f;'.format(group))

    def __connect(self, command):
        result = ssh.connect(self.ip, self.username, self.password, command)
        return result

    def get_group_state(self, group):
        print('Getting group state for group: {}'.format(group))
        result = self.__connect('get_group_state group={}'.format(group))
        enabled_re = r'(Enabled: )([A-Z]+)'
        enabled_list = re.findall(enabled_re, result)
        if len(enabled_list) == 3:
            if 'NO' in enabled_list[0][1] and 'NO' in enabled_list[1][1] and 'NO' in enabled_list[2][1]:
                print('Group {} is ready for removal.'.format(group))


def main():
    print('RPADevice Main function')

if __name__ == "__main__":
    main()
