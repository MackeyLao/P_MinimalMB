'''
 sammi.py: Smart Sensor Motor Interface. Modbus Abstraction Layer.

 Project  : SAMMI - Test Toolchain.
 Created  : Tuesday February 25th 2020
 Author   : Diego Asanza <diego.asanza@de.abb.com>
 © 2021 ABB Stotz Kontakt GmbH
'''

import minimalmodbus
import struct
import string

class SammiException(Exception):

  error_codes = {
    0x40: 'Unknown function code',
    0x41: 'Unknown subfunction code',
    0x42: 'Telegram too short',
    0x43: 'Telegram too long',
    0x44: 'Wrong configuration',
    0x45: 'Not configured',
    0x46: 'Wrong data',
    0xCC: 'Bad header',
    0xDD: 'No active header'
  }

  def __init__(self, fcn, message):
    error_code = [int(s) for s in str(message).split() if s.isdigit()]
    if error_code == []:
      self.message = '{0}: {1}'.format(fcn, message)
    else:
      error_code = error_code[0]
      self.message = '{0}: Sammi answered with error code: {1} ({2})'.format(fcn, str(error_code), self.error_codes[error_code]) 

  def __str__(self):
    return self.message

class SammiNoResponseException(Exception):
  def __init__(self, fcn, message):
    self.message = '{0}: {1}'.format(fcn, message)

  def __str__(self):
    return self.message

class SammiInvalidResponseException(SammiNoResponseException):
  """"""


class  Sammi():

  reset_list = {
    0x00:'Power On Reset',
    0x01:'Power On Reset',
    0x02:'Pin Reset',
    0x03:'Watchdog Reset',
    0x04:'Software Reset',
    0x05:'Brownout Reset',
    0x06:'Hardfault Reset',
    0x07:'Unhandled IRQ Reset',
    0x08:'Lockup Reset'
  }

  sensor_type = {
    1: 'Current and voltage measurements available',
    2: 'Only Current measurements available',
  }

  baudrates = {
    2: 115200,
  }

  cal_status = {
    0x0000: 'Busy',
    0x0001: 'Voltage L1N Error',
    0x0002: 'Voltage L2N Error',
    0x0004: 'Voltage L3N Error',
    0x0008: 'Current L1 Error',
    0x0010: 'Current L2 Error',
    0x0020: 'Current L3 Error',
    0x0040: 'Frequency Error',
    0x0080: 'Phase Error L1',
    0x0100: 'Phase Error L2',
    0x0200: 'Phase Error L3',
    0x0400: 'Phase Sequence Error I',
    0x0800: 'Phase Sequence Error V',
    0x8000: 'Calibration OK',
  }

  def __init__(self, port, baudrate=115200, timeout=0.1):
    self.sammi = minimalmodbus.Instrument(port, 7, debug=False)
    self.sammi.serial.baudrate = baudrate
    self.sammi.serial.timeout = timeout

  def _write(self, f, args):
    try:
      r = self.sammi._perform_command(43, args)
    except minimalmodbus.InvalidResponseError as err:
      raise SammiInvalidResponseException(f.__name__, str(err))
    except minimalmodbus.NoResponseError as err:
      raise SammiNoResponseException(f.__name__, str(err))
    except Exception as err:
      raise SammiException(f.__name__, str(err))
    return r

  def set_config(self, timeout=0, inom=1, gfreq=0, trip_class=0, cool_mode=0, cool_time=1, restart_level=80, num_phases=1, thermal_off=0, curr_level=20):
    r = struct.pack('<BHBBHBBBBBBB', int(timeout), int(inom * 100), int(gfreq), int(trip_class), int(cool_time), int(cool_mode), int(restart_level), int(num_phases), int(thermal_off), int(curr_level), 0, 0)
    r = self._write(self.set_config,'\x12' + r.decode('latin1'))

    r = bytes(r, encoding='latin1')
    r = struct.unpack('<BB', r)
    if r[1] == 0xAA:
      return 'OK'
    else:
      return 'Error'

  def _swap16(self, i):
    return struct.unpack("<H", struct.pack(">H", i))[0]

  def get_device_header(self):
    r = struct.pack('<BHBBBHBHBHBBB', 0x02, 0x0100, 0x01, 0x02, 0x02, 0x0102, 0x02, 0x0100, 0x02, 0x0232, 0x02, 0x00, 0x01)
    r = self._write(self.get_device_header, '\x77' + r.decode('latin1'))

    r = bytes(r, encoding='latin1')
    r = struct.unpack('<BBHBBBHBHBHBBB', r)

    data = {}
    data['header_version'] = self._swap16(r[2])
    data['baudrate'] = self.baudrates[r[4]]
    data['sw_version'] = self._swap16(r[6])
    data['prot_version'] = self._swap16(r[8])
    data['hw_version'] = self._swap16(r[10])
    data['sensor_type'] = self.sensor_type[r[13]]

    return data

  def get_config(self):
    r = self._write(self.get_config, '\x11')

  def get_info(self):
    r = self._write(self.get_info, '\xD5')

    r = bytes(r, encoding='latin1')
    r = struct.unpack('<BBBBBBBBBBBBBH', r)
    info = {}
    info['swversion'] = bytes(r[1:12]).decode('utf-8')
    info['port'] = self.sammi.serial.name      
    return info

  def get_cyclic_data(self):
    r = self._write(self.get_cyclic_data, '\x10\x00\x00')

    r = bytes(r, encoding='latin1')
    r = struct.unpack('<BIIIIIIHHHHHHHbbbBBBHHHH', r)
    data = {}
    data['i'] = [r[1]/1000.0, r[2]/1000.0, r[3]/1000.0]
    data['imean'] = r[4]/1000.0
    # data['imaxatstartup'] = r[5]/1000
    data['ilasttrip'] = r[6] / 1000
    data['ull'] = [r[7]/10.0, r[8]/10.0, r[9]/10.0]
    data['uln'] = [r[10]/10.0, r[11]/10.0, r[12]/10.0]
    data['freq'] = r[13]/10.0
    data['cosphi'] = [r[14]/100.0, r[15]/100.0, r[16]/100.0]
    data['ithd'] = r[17] / 10
    data['uthd'] = r[18] / 10
    data['iearthfault'] = r[19]
    data['thermalload'] = r[20]
    data['timetotrip'] = r[21]
    data['timetocool'] = r[22]
    data['motorrunning'] = (r[23] & 0x01) == 0x01
    data['overloadtrip'] = (r[23] & 0x02) == 0x02
    data['erroriphaseseq'] = (r[23] & 0x04) == 0x04
    data['errorvphaseseq'] = (r[23] & 0x08) == 0x08
    data['ready'] = (r[23] & 0x10) == 0x10
    data['hwerror'] = (r[23] & 0x20) == 0x20
    data['freqerr'] = (r[23] & 0x40) == 0x40
  
    return data

  def reset(self):
    r = self._write(self.reset, '\x10\x01\x00')

  def calibration_start( self ):
    r = self._write(self.calibration_start, '\xD7\x01')
    r = bytes(r, encoding='latin1')
    r = struct.unpack('<BH', r)
    if r[1] == 0x0000:
      return 'Cal Started'
    else:
      return 'Cal Busy'

  def calibration_status( self ):
    r = self._write(self.calibration_start, '\xD7\x02')
    r = bytes(r, encoding='latin1')
    print(r)
    r = struct.unpack('<BH', r)

    if r[1] == 0x0000:
      return self.cal_status[r[1]]
    t = [self.cal_status[r[1] & 0x0001], 
        self.cal_status[r[1] & 0x0002],
        self.cal_status[r[1] & 0x0004],
        self.cal_status[r[1] & 0x0008],
        self.cal_status[r[1] & 0x0010],
        self.cal_status[r[1] & 0x0020],
        self.cal_status[r[1] & 0x0040],
        self.cal_status[r[1] & 0x0080],
        self.cal_status[r[1] & 0x0100],
        self.cal_status[r[1] & 0x0200],
        self.cal_status[r[1] & 0x0400],
        self.cal_status[r[1] & 0x0800],
        self.cal_status[r[1] & 0x8000]]

    t = [ x for x in t if x != 'Busy' ]

    return t

  def write_serial_number(self, sn):
    r = self._write(self.write_serial_number, '\xD8' + sn)
    r = bytes(r, encoding='latin1')
    r = struct.unpack('<B16s', r)
    return r[1].decode('latin1')

  def get_error_counters(self):
    r = self._write(self.get_error_counters, '\xD9')
    r = bytes(r, encoding='latin1')
    r = struct.unpack('<BhhhIII', r)

    data = {}
    data['angle'] = [r[1] / 100, r[2] / 100, r[3] / 100]
    data['mb_chk_err'] = r[4]
    data['afe_overflow_err'] = r[5]
    data['unknown_error'] = 0# r[6]

    return data

  def get_diagnostics(self):
    r = self._write(self.get_error_counters, '\xD6')
    print(r)
    r = bytes(r, encoding='latin1')
    r = struct.unpack('<Bh8I6II40s', r)

    data = {}
    
    if r[1] in self.reset_list:
      reason = self.reset_list[r[1]]
    else:
      reason = 'Unknown'

    data['reset_cause'] = '({0}) {1}'.format(str(r[1]), reason)
    data['r0'] =  hex(r[2])
    data['r1'] =  hex(r[3])
    data['r2'] =  hex(r[4])
    data['r3'] =  hex(r[5])
    data['r12'] =  hex(r[6])
    data['lr'] =  hex(r[7])
    data['pc'] =  hex(r[8])
    data['psr'] =  hex(r[9])

    data['cfsr'] =  hex(r[10])
    data['hfsr'] =  hex(r[11])
    data['dfsr'] =  hex(r[12])
    data['afsr'] =  hex(r[13])
    data['mmar'] =  hex(r[14])
    data['bfar'] =  hex(r[15])

    data['irqn'] =  hex(r[16])

    s = r[17:][0].decode('latin1')
    printable = set(string.printable)

    data['info'] = ''.join(filter(lambda x: x in printable, s))

    return data

if __name__ == "__main__":

  s = Sammi('COM13')
  
  print(s.get_info())
  print(s.get_device_header())
