import sys
import ssh
import re
from credentials import Credentials

class FCSwitch():
    def __init__(self, credentials, ip):
        self.ip = ip
        self.username = credentials.switch_user
        self.password = credentials.switch_pass

    def __connect(self, command):
        result = ssh.connect(self.ip, self.username, self.password, command)
        return result

    def get_cfg(self):
        result = self.__connect('cfgshow | grep cfg')
        cfg_re = re.compile(r'(cfg:	)([a-zA-Z0-9_]+)')
        cfg = re.findall(cfg_re, result)[1][1]
        return cfg

    def get_zone(self, host):
        result = self.__connect('zoneshow --alias HBA*_{}'.format(host))
        zone_re = re.compile(r'(zone:	)([a-zA-Z0-9_]+)')
        zones = re.findall(zone_re, result)
        zone_list = []
        for zone in zones:
            zone_list.append(zone[1])
        return zone_list


def main():
    print('FCSwitch Main function')


if __name__ == "__main__":
    main()
