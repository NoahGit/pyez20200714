from pprint import pprint
from jnpr.junos import Device

dev = Device(host='172.16.100.57', user='lab', password='lab@123')
dev.open()
pprint(dev.facts)
dev.close()
