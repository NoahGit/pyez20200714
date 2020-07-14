import time
from getpass import getpass
from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException, NetMikoAuthenticationException


# Juniper switch interfaces disable
def enable_netconf(net_device):
    print("{} Connecting to {}".format(time.asctime(), net_device['ip']))
    junos_device = ConnectHandler(**net_device)

    configure = junos_device.config_mode()
    print("{} Applying configuration to {}".format(time.asctime(), net_device['ip']))

    junos_device.send_command("run set date "+time.strftime('%Y%m%d%H%M.%S',time.localtime(time.time())))

    print("{} Committing configuration to {}".format(time.asctime(), net_device['ip']))
    junos_device.commit(comment='set date', and_quit=True)

    print("{} Closing connecting to {}".format(time.asctime(), net_device['ip']))
    junos_device.disconnect()


def main():
    user_login = 'lab'
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
