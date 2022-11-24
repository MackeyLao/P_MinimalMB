'''

COM口界面来自：
\PythonCode\Q_pySerial\Serial_Port_GUI_Public.py

'''


from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import serial
import io
from serial.serialutil import EIGHTBITS, STOPBITS_ONE, unicode
import serial.tools.list_ports
import time
import minimalmodbus

IsPortAvailable = False



# 使用minimalModbus库时，串口是不能使用serial占用的
def fucBtnCheckPort():
    global IsPortAvailable
    PortNo = cmbPortNo.get()
    BaudRate = int(cmbBaudRate.get())
    Parity = cmbParity.get()
    ByteSize = int(cmbByteSize.get())
    StopBits = int(cmbStopBits.get())
    try:
        ser = serial.Serial(PortNo)
        ser.close()
        messagebox.showinfo("Information","Port {} is available!".format(PortNo))
        IsPortAvailable = True
    except Exception as err:
        print(str(err))
        messagebox.showwarning("Warning","Port {} is Not Available!".format(PortNo))
        IsPortAvailable = False

def funcUpdateMsgBox(RxTx, msg, lbComData):
    AddMsg = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + '   ' + RxTx + str(':    ') + msg
    lbComData.insert(END, str(AddMsg))

# Port设置控件状态变更
def PortSettingStatusCtrl(IsPortOpen):
    if IsPortOpen:
        cmbPortNo["state"] = DISABLED
        cmbBaudRate["state"] = DISABLED
        cmbByteSize["state"] = DISABLED
        cmbParity["state"] = DISABLED
        cmbStopBits["state"] = DISABLED
    else:
        cmbPortNo["state"] = NORMAL
        cmbBaudRate["state"] = NORMAL
        cmbByteSize["state"] = NORMAL
        cmbParity["state"] = NORMAL
        cmbStopBits["state"] = NORMAL

master = Tk()
master.geometry("600x400")

# Port No
# Get the Available Port Name/获取可用的串口号
PortNoList = list(serial.tools.list_ports.comports())
PortNoNameList = []
if len(PortNoList) > 0:
    for i in range(len(PortNoList)):
        ComName = str(PortNoList[i]).split(' -')[0]
        PortNoNameList.append(ComName)

Label(master, text = "PortNo").grid(row=0,column=0,sticky=W)
cmbPortNo = ttk.Combobox(master, values=PortNoNameList, width=8)
cmbPortNo.grid(row=0, column=1, sticky=W, pady=10)
cmbPortNo.set(PortNoNameList[0])

# BaudRate
BaudRateList =  ["1200", "2400", "4800", "9600", "14400", "19200", "38400","43000", "57600", "76800", "115200", "128000", "256000"]
Label(master, text = "BaudRate").grid(row=0, column=2, sticky=W)
cmbBaudRate = ttk.Combobox(master, values=BaudRateList, width=8)
cmbBaudRate.grid(row=0, column=3, sticky=W)
cmbBaudRate.set(BaudRateList[3])

# Parity
ParityList = ["N", "E", "O", "M", "S"]
Label(master, text="Parity").grid(row=0, column=4, sticky=W)
cmbParity = ttk.Combobox(master, values=ParityList, width=5)
cmbParity.grid(row=0, column=5, sticky=W)
cmbParity.set(ParityList[0])

# DataBits
ByteSizeList = ["5", "6", "7", "8"]
Label(master, text="ByteSize").grid(row=0, column=6, sticky=W)
cmbByteSize = ttk.Combobox(master, values=ByteSizeList, width=5)
cmbByteSize.grid(row=0, column=7, sticky=W)
cmbByteSize.set(ByteSizeList[3])

# StopBits
StopBitslist = ["1", "1.5", "2"]
Label(master, text="StopBits").grid(row=0, column=8, sticky=W)
cmbStopBits = ttk.Combobox(master, values=StopBitslist, width=5)
cmbStopBits.grid(row=0, column=9, sticky=W)
cmbStopBits.set(StopBitslist[0])

# Port control button
btnPort = Button(master, text="Check Port", command= fucBtnCheckPort)
btnPort.grid(row=1, column=0, columnspan=2, padx = 10, pady = 10, sticky=W)

# list box to show the communication message
lbScrollbar = Scrollbar(master)
lbScrollbar.grid(row=2, column = 9, rowspan= 10, sticky=N+S)
lbComData = Listbox(master, yscrollcommand= lbScrollbar.set)
lbComData.grid(row=2, column = 0, rowspan = 10, columnspan=9, padx = 10, pady = 10, sticky=N+S+W+E)
lbScrollbar.config(command= lbComData.yview)

'''
Following code are for communication
'''

# Set up and init Modbus 
def funcSetupMB():
    PortNo = cmbPortNo.get()
    BaudRate = int(cmbBaudRate.get())
    Parity = cmbParity.get()
    ByteSize = int(cmbByteSize.get())
    StopBits = int(cmbStopBits.get())

    # create MB and set up serial port
    instrument = minimalmodbus.Instrument(port = PortNo, slaveaddress=1, mode=minimalmodbus.MODE_RTU, close_port_after_each_call=True, debug=True)
    instrument.serial.baudrate = BaudRate
    instrument.serial.parity = Parity
    instrument.serial.bytesize = ByteSize
    instrument.serial.stopbits = StopBits
    instrument.serial.timeout = 0.2

    return instrument

def fucBtnSendData():
    global IsPortAvailable
    if IsPortAvailable == True:
        mbInstrument = funcSetupMB()
        # 通信内容
        RxData = mbInstrument.read_register(0x64, 0x08)
        print(RxData)

        # 显示：
        AddMsg = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + "received data: {}".format(RxData)
        lbComData.insert(END, str(AddMsg))
    else:
        messagebox.showwarning("Warning","Please check the COM Port first!")

def funcCleanListBox():
    lbComData.delete(0, END)

# Send data button
btnSendData = Button(master, text="Send Data", command= fucBtnSendData)
btnSendData.grid(row=1, column=2, columnspan=2)


# clean listbox
btnClean = Button(master, text= 'Clean ListBox', command=funcCleanListBox)
btnClean.grid(row=1, column = 4, columnspan=2)

master.title("Serial Port Communication")
master.mainloop()

