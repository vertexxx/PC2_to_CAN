
from PCANBasic import *
import os
import sys
import threading
import urllib
import urllib.request
import json

debug_readfromfile = 1

class TimerRepeater(object):
    def __init__(self, name, interval, target):
        self._name = name
        self._thread = None
        self._event = None
        self._target = target
        self._interval = interval
    def _run(self):
        while not self._event.wait(self._interval):
            self._target()
        print("Timer stopped.")
    def start(self):
        if (self._thread == None):
            self._event = threading.Event()
            self._thread = threading.Thread(None, self._run, self._name)
            self._thread.start()
    def stop(self):
        if (self._thread != None):
            self._event.set()
            self._thread.join() 
            self._thread = None

class TimerWrite():
    PcanHandle = PCAN_USBBUS1
    Bitrate = PCAN_BAUD_1M
    TimerInterval = 10
    m_DLLFound = False
    sendcounter = 0
    jsondata = []

    def __init__(self):
        self.ShowConfigurationHelp()
        self.ShowCurrentConfiguration()
        try:
            self.m_objPCANBasic = PCANBasic()        
            self.m_DLLFound = self.CheckForLibrary()
        except:
            print("Unable to find the library: PCANBasic.dll !")
            self.getInput("Press <Enter> to quit...")
            self.m_DLLFound = False
            return

        stsResult = self.m_objPCANBasic.Initialize(self.PcanHandle,self.Bitrate)

        if stsResult != PCAN_ERROR_OK:
            print("Can not initialize. Please check the defines in the code.")
            self.ShowStatus(stsResult)
            print("")
            print("Press enter to close")
            input()
            return

        print("Successfully initialized.")
        self.m_objTimer = TimerRepeater("WriteMessages",float(self.TimerInterval)/1000, self.WriteMessages)
        self.m_objTimer.start()
        print("Started writing messages...")
        print("")
        self.getInput("Press <Enter> to stop timer...")
        self.m_objTimer.stop()
        self.getInput("Press <Enter> to exit...")

    def __del__(self):
        if self.m_DLLFound:
            self.m_objPCANBasic.Uninitialize(PCAN_NONEBUS)

    def getInput(self, msg="Press <Enter> to continue...", default=""):
        res = default
        if sys.version_info[0] >= 3:
            res = input(msg + " ")
        else:
            res = raw_input(msg + " ")
        if len(res) == 0:
            res = default
        return res

    def updateJson(self):
        url='http://127.0.0.1:8180/crest2/v1/api'
        fileurl='api.json'
        if 1:#try:
            if debug_readfromfile:
                with open(fileurl, mode="rb") as fileasbytes:
                    jsonbytes = fileasbytes.read()
            else:
                r = urllib.request.urlopen(url)
                jsonbytes = r.read().decode(r.info().get_param('charset') or 'utf-8')
            self.jsondata = json.loads(jsonbytes)
            print(self.jsondata['carState']['mRpm'])
        #except:
        #    print('nope')

    def WriteMessages(self):
        self.updateJson()
        stsResult = self.WriteMessage(0x50)
        stsResult = self.WriteMessage(0x51)
        stsResult = self.WriteMessage(0x52)
        stsResult = self.WriteMessage(0x53)
        stsResult = self.WriteMessage(0x54)
        stsResult = self.WriteMessage(0x55)
        self.sendcounter = self.sendcounter+1
        #if (stsResult != PCAN_ERROR_OK):
        #    self.ShowStatus(stsResult)
        #else:
        #    print("Message was successfully SENT")

    def WriteMessage(self, hexid):
        msgCanMessage = TPCANMsg()
        msgCanMessage.ID = hexid
        msgCanMessage.LEN = 8
        msgCanMessage.MSGTYPE = PCAN_MESSAGE_EXTENDED.value
        if hexid==0x50:
            for i in range(8):
                msgCanMessage.DATA[i] = i
                pass
        return self.m_objPCANBasic.Write(self.PcanHandle, msgCanMessage)

    def clear(self):
        if os.name=='nt':
            os.system('cls')
        else:
            os.system('clear')

    def CheckForLibrary(self):
        try:
            self.m_objPCANBasic.Uninitialize(PCAN_NONEBUS)
            return True
        except :
            return False 

    def ShowConfigurationHelp(self):
        print("")

    def ShowCurrentConfiguration(self):
        print("Parameter values used")
        print("----------------------")
        print("* PCANHandle= " + self.FormatChannelName(self.PcanHandle))
        print("* Bitrate= " + self.ConvertBitrateToString(self.Bitrate))
        print("* TimerInterval: " + str(self.TimerInterval))
        print("")

    def ShowStatus(self,status):
        print("=========================================================================================")
        print(self.GetFormattedError(status))
        print("=========================================================================================")
    
    def FormatChannelName(self, handle):
        handleValue = handle.value
        if handleValue < 0x100:
            devDevice = TPCANDevice(handleValue >> 4)
            byChannel = handleValue & 0xF
        else:
            devDevice = TPCANDevice(handleValue >> 8)
            byChannel = handleValue & 0xFF
        return ('%s: %s (%.2Xh)' % (self.GetDeviceName(devDevice.value), byChannel, handleValue))

    def GetFormattedError(self, error):
        stsReturn = self.m_objPCANBasic.GetErrorText(error,0x09)
        if stsReturn[0] != PCAN_ERROR_OK:
            return "An error occurred. Error-code's text ({0:X}h) couldn't be retrieved".format(error)
        else:
            message = str(stsReturn[1])
            return message.replace("'","",2).replace("b","",1)

    def GetDeviceName(self, handle):
        switcher = {
            PCAN_NONEBUS.value: "PCAN_NONEBUS",
            PCAN_PEAKCAN.value: "PCAN_PEAKCAN",
            PCAN_ISA.value: "PCAN_ISA",
            PCAN_DNG.value: "PCAN_DNG",
            PCAN_PCI.value: "PCAN_PCI",
            PCAN_USB.value: "PCAN_USB",
            PCAN_PCC.value: "PCAN_PCC",
            PCAN_VIRTUAL.value: "PCAN_VIRTUAL",
            PCAN_LAN.value: "PCAN_LAN"
        }
        return switcher.get(handle,"UNKNOWN")   

    def ConvertBitrateToString(self, bitrate):
        m_BAUDRATES = {PCAN_BAUD_1M.value:'1 MBit/sec', PCAN_BAUD_800K.value:'800 kBit/sec', PCAN_BAUD_500K.value:'500 kBit/sec', PCAN_BAUD_250K.value:'250 kBit/sec',
                       PCAN_BAUD_125K.value:'125 kBit/sec', PCAN_BAUD_100K.value:'100 kBit/sec', PCAN_BAUD_95K.value:'95,238 kBit/sec', PCAN_BAUD_83K.value:'83,333 kBit/sec',
                       PCAN_BAUD_50K.value:'50 kBit/sec', PCAN_BAUD_47K.value:'47,619 kBit/sec', PCAN_BAUD_33K.value:'33,333 kBit/sec', PCAN_BAUD_20K.value:'20 kBit/sec',
                       PCAN_BAUD_10K.value:'10 kBit/sec', PCAN_BAUD_5K.value:'5 kBit/sec'}
        return m_BAUDRATES[bitrate.value]

TimerWrite()
