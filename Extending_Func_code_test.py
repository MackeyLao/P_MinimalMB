'''

https://minimalmodbus.readthedocs.io/en/stable/develop.html#extending-minimalmodbus

使用._perform_command()返回的数据是会删除前面的两字节，即slave add, function code， 和后面两字节，即CRC的

'''

import minimalmodbus

# ComPort = 'COM10'
ComPort = 'COM11'

instrument = minimalmodbus.Instrument(ComPort, slaveaddress=1, mode=minimalmodbus.MODE_RTU, close_port_after_each_call=False, debug=True)
instrument.serial.timeout  = 0.5    #若不设置timeout, 某些命令会无法接收到数据

# 使用0x03功能码做测试
# RxData1 = instrument.read_register(1,1)
# 测试发送的数据是一样的， 但是接收到的数据不正确，RxData2并没有完整接收到所有数据，似乎都是没有接收前两字节，即slave add, function code.
# debug显示的数据是正确的。

try:
    RxData2 = instrument._perform_command(3, '\x00\x01\x00\x01')
    RxData = instrument._perform_command(17,'') #返回的数据为class 'str'

    print(bytes(RxData,'Latin1').hex())

    strRxData = []
    strRxData2 = ''
    for byte in bytes(RxData,'Latin1'): 
        strRxData.append(hex(byte))
        strRxData2 = strRxData2 + hex(byte) + '\t'
        print("0x{0:02X}".format(byte))
    print(strRxData)
    print(strRxData2)
except Exception as e:
    print("Communication Error:")
    print(str(e))