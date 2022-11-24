'''
使用Report Slave ID 0x11来check哪些从机是在线的
'''

import minimalmodbus

# ComPort = 'COM10'
ComPort = 'COM11'

instrument = minimalmodbus.Instrument(ComPort, slaveaddress=1, mode=minimalmodbus.MODE_RTU, close_port_after_each_call=False, debug=False)
instrument.serial.timeout = 0.2

slaveAddrList = range(1,5)

# 以字典方式保存状态
slaveStatus = {}

for slaveAddr in slaveAddrList:
    print("Check Slave {} ...".format(slaveAddr))
    # set the slave address for MB
    instrument.address = slaveAddr
    try:
        # Report Slave ID: 0x11
        RxData = instrument._perform_command(17,'')
        # if no error, means Slaver is online
        print("Slave {} is on-line.".format(slaveAddr))
        slaveStatus['Slave {}'.format(slaveAddr)] = True
    except Exception as err:
        # 将不在线的从机显示为红色
        print("\033[0;31;40mSlave {} is off-line!\033[0m".format(slaveAddr))
        slaveStatus['Slave {}'.format(slaveAddr)] = False

print("Final status is:", slaveStatus)

