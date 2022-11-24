### introduction
- Minimal Modbus python library test and project repository. 
- Documentation: https://minimalmodbus.readthedocs.io 
- Source code on GitHub: https://github.com/pyhys/minimalmodbus 
- Python package index (PyPI) with download: https://pypi.org/project/MinimalModbus/ 


### files/folder list
- FirstTest.py  
  第一个测试Minimal modbus的程序
  包括常用的功能码测试
    test_read_bit()  
    test_write_bit()  
    test_write_bits()  
    test_read_reg()  
    test_write_reg()  
    test_write_regs()  
    test_read_write_float()  
    test_read_write_string()  
    test_ReportID()

- docstring_test.py  
  docstring插件测试，与Minimal Modbus无关

- Extending_Func_code_test.py  
  测试使用._perform_command()来发送MB数据，可以扩展功能码的使用。

- minimalModbus_GUI_Public.py  
  结合tkinter库，制作使用minimalModbus的GUI测试程序。
  可用作制作相关工程的例程。

- preview_test.py  
  list, tuple, set, dict四种数据类型的测试。
  不记得有什么用

- ReportSlaveID_Find_Test.py  
  使用._perform_command()发送0x11指令，循环测试哪些从机在线。

- sammi.py  
  DESTO Diago发给我的一个使用minimalModbus的实例

- test_unittest.py  
  使用unittest测试minimalmodbus.


