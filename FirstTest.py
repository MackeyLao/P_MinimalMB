import minimalmodbus
import serial

# 如果在使用minimalmodbus之前使用pyserial将串口调用了，即使未使用open()打开，则会导致minimalmodbus无法使用
# 所以使用minimalmobus时，是不需要先打开串口的
# ser = serial.Serial('COM7')
# ser.open()

# ComPort = 'COM10'
ComPort = 'COM11'

instrument = minimalmodbus.Instrument(ComPort,1,debug = True) # port name, slave address (in decimal)

'''
default value:
instrument.serial.port                     # this is the serial port name
instrument.serial.baudrate = 19200         # Baud
instrument.serial.bytesize = 8
instrument.serial.parity   = serial.PARITY_NONE
instrument.serial.stopbits = 1
instrument.serial.timeout  = 0.05          # seconds
'''

#default is 19200
#instrument.serial.baudrate = 9600  
#default is NONE
#instrument.serial.parity = serial.PARITY_EVEN  
#instrument.serial.parity = minimalmodbus.serial.PARITY_EVEN
instrument.serial.timeout = 0.2
#Closing serial port after each call
instrument.close_port_after_each_call = True

#print(instrument)

def test_read_bit():
    try:
        print("Test Function code 0x02")
        print("read 0x02 register value is: ",instrument.read_bit(0))
    except Exception as err:
        print(str(err))
        print("Failed to read from instrument")

def test_write_bit():
    #操作coil output 寄存器
    try:
        print("Test Function code 0x05")
        print("write 0x05 register value is: ",instrument.write_bit(1,1))
        print("read 0x02 register value is: ",instrument.read_bit(1,2)) #这个不能读取
        print("read 0x01 register value is: ",instrument.read_bit(1,1)) #这个才能读取
        print("Test Function code 0x0F")
        print("write 0x0F register value is: ",instrument.write_bit(16,1,functioncode=15))   #操作的寄存器一样
        print("read 0x02 register value is: ",instrument.read_bit(16,2)) #这个不能读取
        print("read 0x01 register value is: ",instrument.read_bit(16,1)) #这个才能读取
    except Exception as err:
        print(str(err))
        print("Failed to read from instrument")

def test_read_reg():
    try:
        print("Test Function code 0x03,0x04")
        print("read 0x03 register value is: ",instrument.read_register(0,1,3))
        instrument.address = 2
        print("read 0x04 register value is: ",instrument.read_register(1,1,4,signed=True))
    except Exception as err:
        print(str(err))
        print("Failed to read from instrument")

def test_write_bits():
    try:
        print("Test Function code 0x0F")
        print("write 0x0F register value is: ",instrument.write_bits(32,[1,1,0,1,0,1,1,1]))
    except Exception as err:
        print(str(err))
        print("Failed to read from instrument")

def test_write_reg():
    try:
        print("Test Function code 0x10")
        instrument.write_register(30,0xABCD,number_of_decimals=0,functioncode=16,signed=False)
        instrument.write_register(31,100,number_of_decimals=1,functioncode=16,signed=False)
        instrument.write_register(32,-100,number_of_decimals=1,functioncode=16,signed=True)
        print("Test Function code 0x06")
        instrument.write_register(40,0xABCD,number_of_decimals=0,functioncode=6,signed=False)
        instrument.write_register(41,100,number_of_decimals=1,functioncode=6,signed=False)
        instrument.write_register(42,-100,number_of_decimals=1,functioncode=6,signed=True)
    except Exception as err:
        print(str(err))
        print("Failed to read from instrument")

def test_write_regs():
    try:
        print("Test Function code 0x10")
        print("write 0x10 registers value is: ",instrument.write_registers(10,[1,2,3,0xffFA]))
    except Exception as err:
        print(str(err))
        print("Failed to read from instrument")


def test_read_write_float():
    try:
        number = 3.14159
        print("write float number: ",number)
        print(instrument.write_float(50,number,number_of_registers=4))
        print("read float")
        print(instrument.read_float(50,functioncode=3,number_of_registers=4))
    except Exception as err:
        print(str(err))
        print("Failed to read from instrument")    

def test_read_write_string():
    try:
        str2write = "1234567890ABCDEF"
        RegLen = int(len(str2write)/2)
        print("write string:",str2write)
        print(instrument.write_string(60,str2write,number_of_registers=RegLen))
        print("read string")
        print(instrument.read_string(60,number_of_registers=RegLen,functioncode=3))
    except Exception as err:
        print(str(err))
        print("Failed to read from instrument")  

def test_ReportID():
    try:
        print(instrument._perform_command(17,''))
    except Exception as err:
        print(str(err))



# export diagnostic string
#print(minimalmodbus._get_diagnostic_string())

if __name__ == '__main__':
    # test_read_bit()
    # test_write_bit()  
    # test_write_bits()
    # test_read_reg()  
    # test_write_reg()
    # test_write_regs()
    # test_read_write_float()
    # test_read_write_string()
    test_ReportID()
