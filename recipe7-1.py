import time
from getpass import getpass
from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException, NetMikoAuthenticationException


# Juniper switch batch change password
def enable_netconf(net_device):
    print("{} Connecting to {}".format(time.asctime(), net_device['ip']))
    junos_device = ConnectHandler(**net_device)

    configure = junos_device.config_mode()
    print(configure)
    print("{} Applying configuration to {}".format(time.asctime(), net_device['ip']))

    junos_device.send_command("set system login user lab authentication"
                              " encrypted-password $5$6XvXp.HH$qS7SIb4NouDqGWBiRWhbROK1U02mqb7Q4pk0Qhsajm5")

    print("{} Committing configuration to {}".format(time.asctime(), net_device['ip']))
    junos_device.commit(comment='batch change password', and_quit=True)

    print("{} Closing connecting to {}".format(time.asctime(), net_device['ip']))
    junos_device.disconnect()


def main():
    user_login = input('Username:')
    user_pass = 'lab@123'
    with open('./inventory.txt') as f:
        device_list = f.read().splitlines()
        for device in device_list:
            net_device = {
                'device_type': 'juniper',
                'ip': device,
                'username': user_login,
                'password': user_pass,
            }
            enable_netconf(net_device)


if __name__ == '__main__':
    main()
