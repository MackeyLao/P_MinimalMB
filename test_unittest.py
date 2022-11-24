import minimalmodbus
import unittest

# ComPort = 'COM10'
ComPort = 'COM11'

class Test_MB(unittest.TestCase):
    def test_Read_Reg(self):
        instr = minimalmodbus.Instrument(ComPort,1,close_port_after_each_call=True,debug=True)
        instr.serial.timeout = 0.2
        assert(instr.read_register(1,1,3))

if __name__ == '__main__':
    unittest.main()