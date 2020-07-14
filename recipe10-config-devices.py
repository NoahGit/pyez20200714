from jnpr.junos import Device
from jnpr.junos.utils.config import Config

USER = "lab"
PW = "lab@123"
CONFIG_FILE = './config.txt'
CONFIG_DATA = {
    'systime': '202007141126:00'
}


def config_devices(devices='./inventory.txt'):
    with open(devices) as f:
        inventorys = f.read().splitlines()

        for inventory in inventorys:
            dev = Device(host=inventory, user=USER, password=PW).open()
            with Config(dev) as cu:
                cu.load(template_path=CONFIG_FILE, template_vars=CONFIG_DATA, format='set', merge=True)
                cu.commit(timeout=30)
                print("Committing the configuration on device:{}".format(inventory))
                dev.close()


if __name__ == "__main__":
    config_devices()
