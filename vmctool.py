from rpa_config import RPADevice
from vmax_config import VMAXDevice
from credentials import Credentials
from fcswitch_config import FCSwitch


def main():
    print('''Test data:
    \taccount_number = 1234124
    \tstorage_device = 12341234
    \thosts = [1234124,12341234,12341234]
    \tsource_vmax_sid = 1243''')
    print()
    credentials = get_credentials()
    print()
    print('Beginning RPA work...')
    print()
    check_rpa_group(credentials)
    print()
    print('Beginning VMAX work...')
    print()
    check_vmax(credentials)
    print()
    print('Beginning Fibre Channel Switch work...')
    check_zones(credentials)
    print()


def get_credentials():
    valid = False

    while (valid == False):
        account_number = input('Account number: ')
        storage_device = input('Storage Device number: ')
        number_of_hosts = input('Number of hosts (default: 1): ')
        hosts = []
        if number_of_hosts == '' or number_of_hosts is None:
            number_of_hosts = 1
        for host in range(int(number_of_hosts)):
            hosts.append(input('Host {} device number: '.format(host)))
        source_vmax_sid = input('Source VMAX SID: ')
        print('Verify the following input is correct: ')
        print('\tAccount: {}'.format(account_number))
        print('\tStorage Device: {}'.format(storage_device))
        print('\tHosts: {}'.format(hosts))
        print('\tSource VMAX SID: {}'.format(source_vmax_sid))
        is_valid = input('Valid Y or N: ')
        if is_valid.lower() == 'y' or is_valid.lower() == 'yes':
            break
    return Credentials(account_number, storage_device, hosts, source_vmax_sid)


def check_rpa_group(credentials):
    rpa = RPADevice(credentials)
    group = rpa.get_group(credentials.account_number, credentials.storage_device)
    rpa.get_group_state(group)
    rpa.remove_group(group)

def check_zones(credentials):
    a_switch = FCSwitch(credentials, credentials.a_switch_ip)
    b_switch = FCSwitch(credentials, credentials.b_switch_ip)
    a_cfg = a_switch.get_cfg()
    b_cfg = b_switch.get_cfg()
    a_zones = []
    b_zones = []
    for host in credentials.hosts:
        a_zones.append(a_switch.get_zone(host))
        b_zones.append(b_switch.get_zone(host))
    print()
    print('Run the following commands on the A side switch:')
    print()
    count = 0
    for host in credentials.hosts:
        print('\tzonedelete {}'.format(a_zones[count][0]))
        print('\talidelete HBA0_{}'.format(host))
        count += 1
    print('\tfgenable {}'.format(a_cfg))
    print('\tcfgsave {}'.format(a_cfg))
    print()
    print('Run the following commands on the B side switch:')
    print()
    count = 0
    for host in credentials.hosts:
        print('\tzonedelete {}'.format(b_zones[count][0]))
        print('\talidelete HBA1_{}'.format(host))
        count += 1
    print('\tcfgenable {}'.format(b_cfg))
    print('\tcfgsave {}'.format(b_cfg))

def check_vmax(credentials):
    vmax = VMAXDevice(credentials)

    # Get storage group for this account on the VMAX3
    sg = vmax.get_sg(credentials.target_vmax_sid, credentials.account_number)

    # Untag target SG for RPA
    vmax.untag_sg(credentials.target_vmax_sid, sg)

    # Get storage group from source VMAX
    sg = vmax.get_sg(credentials.source_vmax_sid, credentials.account_number)

    vmax.untag_sg(credentials.source_vmax_sid, sg)

    vmax.get_luns(credentials.source_vmax_sid, sg)

    vmax.get_initiators(credentials.source_vmax_sid, credentials.account_number)


if __name__ == "__main__":
    main()
