from jnpr.junos import Device
from jnpr.junos.utils.config import Config

dev = Device(host='172.16.100.57', user='lab', password='lab@123', gather_facts=False)
dev.open()

cu = Config(dev)
# diff = cu.diff()
cu.commit()
# if diff:
#     cu.rollback()
dev.close()
