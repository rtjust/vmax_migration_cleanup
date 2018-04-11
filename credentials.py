class Credentials():
    def __init__(self, account_number, storage_device, hosts, source_vmax_sid):
        self.account_number = account_number
        self.storage_device = storage_device
        self.hosts = hosts
        self.source_vmax_sid = source_vmax_sid

        self.username = ''
        self.password = ''

        self.symcli_ip = ''

        self.target_vmax_sid = ''

        self.rpa_ip = ''
        self.rpa_user = 'admin'
        self.rpa_pass = ''

        self.switch_user = 'admin'
        self.switch_pass = ''
        self.a_switch_ip = ''
        self.b_switch_ip = ''
